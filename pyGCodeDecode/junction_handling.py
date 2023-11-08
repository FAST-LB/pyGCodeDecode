# -*- coding: utf-8 -*-
"""Junction handling module."""

import math

import numpy as np

from .state import state
from .utils import velocity


class junction_handling:
    """Junction handling super class."""

    def connect_state(self, state_A: state, state_B: state):
        """
        Connect two states and generates the velocity for the move from state_A to state_B.

        **Parameters**

            state_A, state_B  :   state
                two consecutive states

        **Returns**

            velocity
                the target velocity for that travel move
        """
        if state_A is None or state_B is None:
            return velocity(0, 0, 0, 0)

        travel_direction = np.asarray((state_B.state_position - state_A.state_position).get_vec(withExtrusion=True))
        t_distance = np.linalg.norm(travel_direction[:3])
        e_len = travel_direction[3]
        if abs(t_distance) > 0:  # regular travel mixed move
            travel_direction = travel_direction / t_distance
        elif abs(e_len) > 0:  # for extrusion only move
            travel_direction = travel_direction / abs(e_len)
        else:  # no move at all
            travel_direction = np.asarray([0, 0, 0, 0])
        target_vel = velocity(state_B.state_p_settings.speed * travel_direction)
        return target_vel

    def calc_vel_next(self):
        """Return the target velocity for the following move."""
        next_next_state = self.state_B.next_state if self.state_B.next_state is not None else self.state_B
        while True:
            if (
                next_next_state.next_state is None
                or self.state_B.state_position.get_t_distance(next_next_state.state_position, withExtrusion=True) > 0
            ):
                vel_next = self.connect_state(
                    state_A=self.state_B, state_B=next_next_state
                )  # target velocity for next plannerblock
                break
            else:
                next_next_state = next_next_state.next_state
        return vel_next

    def get_target_vel(self):
        """Return target velocity."""
        return self.target_vel

    def __init__(self, state_A: state, state_B: state):
        """Initialize the junction handling."""
        self.state_A = state_A
        self.state_B = state_B
        self.target_vel = self.connect_state(state_A=state_A, state_B=state_B)
        self.vel_next = self.calc_vel_next()

    def get_junction_vel(self):
        """Return default junction velocity of zero."""
        return 0


class junction_handling_marlin(junction_handling):
    """Marlin specific junction handling."""

    def calc_JD(self, vel_0: velocity, vel_1: velocity, p_settings: state.p_settings):
        """
        Calculate junction deviation velocity from 2 velocitys.

        **Parameters**

            vel_0,vel_1 : velocity
                velocity objects
            p_settings  : state.p_settings
                print settings, containing acceleration settings

        **Returns**

            velocity
                velocity abs value

        **Reference**

        [https://onehossshay.wordpress.com/2011/09/24/improving_grbl_cornering_algorithm/](https://onehossshay.wordpress.com/2011/09/24/improving_grbl_cornering_algorithm/)
        [http://blog.kyneticcnc.com/2018/10/computing-junction-deviation-for-marlin.html](http://blog.kyneticcnc.com/2018/10/computing-junction-deviation-for-marlin.html)

        """
        # Junction deviation settings
        JD_acc = p_settings.p_acc
        if p_settings.jerk == 0:
            return 0
        JD_delta = 0.4 * p_settings.jerk * p_settings.jerk / JD_acc  # [2]
        JD_minAngle = 18
        JD_maxAngle = 180 - 18
        vel_0_vec = vel_0.get_vec()
        vel_1_vec = vel_1.get_vec()
        if vel_0.get_norm() == 0 or vel_1.get_norm() == 0:
            return 0
        # calculate junction angle
        JD_cos_theta = np.dot(-np.asarray(vel_0_vec), np.asarray(vel_1_vec)) / (
            np.linalg.norm(vel_0_vec) * np.linalg.norm(vel_1_vec)
        )  # cos of theta, theta: small angle between velocity vectors
        if JD_cos_theta < 1:  # catch numerical errors where cos theta is slightly larger than one
            JD_sin_theta_half = np.sqrt((1 - JD_cos_theta) / 2)
        else:
            JD_sin_theta_half = 0
        if JD_sin_theta_half < np.sin(JD_maxAngle * np.pi / (2 * 180)):  # smaller than max angle
            if JD_sin_theta_half > np.sin(
                JD_minAngle * np.pi / (2 * 180)
            ):  # and larger than min angle --> apply Junction Deviation Calculation
                # calculate scalar junction velocity
                JD_Radius = JD_delta * JD_sin_theta_half / (1 - JD_sin_theta_half)
                JD_velocity_scalar = np.sqrt(JD_acc * JD_Radius)

                # return JD_velocity_scalar if JD_velocity_scalar < vel_0.get_norm() else vel_0.get_norm()
                return JD_velocity_scalar if JD_velocity_scalar < p_settings.speed else p_settings.speed
            else:
                return 0  # angle smaller than min angle, stop completely
        else:
            return p_settings.speed  # angle larger than max angle, full speed pass

    def __init__(self, state_A: state, state_B: state):
        """Marlin specific junction velocity calculation."""
        super().__init__(state_A, state_B)
        self.junction_vel = self.calc_JD(
            vel_0=self.target_vel, vel_1=self.vel_next, p_settings=self.state_B.state_p_settings
        )

    def get_junction_vel(self):
        """Return junction velocity."""
        return self.junction_vel


class junction_handling_klipper(junction_handling):
    """Klipper specific junction handling.

    - similar junction deviation calc
    - corner vel set by: square_corner_velocity
        end_velocity^2 = start_velocity^2 + 2*accel*move_distance
      for 90° turn
    - smoothed look ahead
    https://www.klipper3d.org/Kinematics.html
    """

    def __init__(self, state_A: state, state_B: state):
        """Klipper specific junction velocity calculation."""
        super().__init__(state_A, state_B)

        self.calc_j_delta()
        self.calc_j_vel()

    def calc_j_delta(self):
        """Calculate the junction deviation with klipper specific values.

        - jerk value represents the square_corner_velocity
        """
        sc_vel = (self.state_B.state_p_settings.jerk) ** 2
        self.j_delta = sc_vel * (math.sqrt(2.0) - 1.0) / self.state_B.state_p_settings.p_acc

    def calc_j_vel(self):
        """Calculate the junction velocity."""
        vel_0 = self.target_vel
        vel_1 = self.vel_next

        vel_0_vec = vel_0.get_vec()
        vel_1_vec = vel_1.get_vec()
        if vel_0.get_norm() == 0 or vel_1.get_norm() == 0:
            self.j_vel = 0
            return

        # calculate junction angle
        j_cos_theta = np.dot(-np.asarray(vel_0_vec), np.asarray(vel_1_vec)) / (
            np.linalg.norm(vel_0_vec) * np.linalg.norm(vel_1_vec)
        )  # cos of theta, theta: small angle between velocity vectors

        j_cos_theta = max(j_cos_theta, -0.999999)  # limit
        if j_cos_theta > 0.999999:
            self.j_vel = self.target_vel.get_norm()  # if self.target_vel.get_norm() is not None else 0
            return

        j_sin_theta_d2 = math.sqrt(0.5 * (1.0 - j_cos_theta))
        j_R = self.j_delta * j_sin_theta_d2 / (1.0 - j_sin_theta_d2)

        # [from klipper]: Approximated circle must contact moves no further away than mid-move
        j_tan_theta_d2 = j_sin_theta_d2 / math.sqrt(0.5 * (1.0 + j_cos_theta))

        move_centripetal_v2 = (
            0.5
            * self.state_A.state_position.get_t_distance(self.state_B.state_position)
            * j_tan_theta_d2
            * self.state_B.state_p_settings.p_acc
        )

        self.j_vel = math.sqrt(
            min(self.state_B.state_p_settings.p_acc * j_R, move_centripetal_v2, self.state_B.state_p_settings.speed)
        )

    def get_junction_vel(self):
        """Return the calculated junction velocity."""
        return self.j_vel
