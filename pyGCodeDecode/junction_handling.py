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

        Args:
            state_A: (state) start state
            state_B: (state)   end state

        Returns:
            velocity: (float) the target velocity for that travel move
        """
        if state_A is None or state_B is None:
            return velocity(0, 0, 0, 0)

        travel_direction = np.asarray((state_B.state_position - state_A.state_position).get_vec(withExtrusion=True))
        self.t_distance = np.linalg.norm(travel_direction[:3])
        e_len = travel_direction[3]
        if abs(self.t_distance) > 0:  # regular travel mixed move
            travel_direction = travel_direction / self.t_distance
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
                )  # target velocity for next planner block
                break
            else:
                next_next_state = next_next_state.next_state
        return vel_next

    def get_target_vel(self):
        """Return target velocity."""
        return self.target_vel

    def __init__(self, state_A: state, state_B: state):
        """Initialize the junction handling.

        Args:
            state_A: (state) start state
            state_B: (state)   end state
        """
        self.state_A = state_A
        self.state_B = state_B
        self.target_vel = self.connect_state(state_A=state_A, state_B=state_B)
        self.vel_next = self.calc_vel_next()

    def get_junction_vel(self):
        """Return default junction velocity of zero.

        Returns:
            0: zero for default full stop junction handling
        """
        return 0


class junction_handling_marlin_jd(junction_handling):
    """Marlin specific junction handling with Junction Deviation."""

    def calc_JD(self, vel_0: velocity, vel_1: velocity, p_settings: state.p_settings):
        """
        Calculate junction deviation velocity from 2 velocitys.

        **Reference:**

        [https://onehossshay.wordpress.com/2011/09/24/improving_grbl_cornering_algorithm/](https://onehossshay.wordpress.com/2011/09/24/improving_grbl_cornering_algorithm/)
        [http://blog.kyneticcnc.com/2018/10/computing-junction-deviation-for-marlin.html](http://blog.kyneticcnc.com/2018/10/computing-junction-deviation-for-marlin.html)


        Args:
            vel_0: (velocity) entry
            vel_1: (velocity) exit
            p_settings: (state.p_settings) print settings

        Returns:
            velocity: (float) velocity abs value
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
        """Marlin specific junction velocity calculation with Junction Deviation.

        Args:
            state_A: (state) start state
            state_B: (state)   end state
        """
        super().__init__(state_A, state_B)
        self.junction_vel = self.calc_JD(
            vel_0=self.target_vel, vel_1=self.vel_next, p_settings=self.state_B.state_p_settings
        )

    def get_junction_vel(self):
        """Return junction velocity.

        Returns:
            junction_vel: (float) junction velocity
        """
        return self.junction_vel


class junction_handling_marlin_jerk(junction_handling):
    """Marlin classic jerk specific junction handling.

    **Reference**
    [https://github.com/MarlinFirmware/Marlin/pull/8887](https://github.com/MarlinFirmware/Marlin/pull/8887)
    [https://github.com/MarlinFirmware/Marlin/pull/8888](https://github.com/MarlinFirmware/Marlin/pull/8888)
    [https://github.com/MarlinFirmware/Marlin/issues/367#issuecomment-12505768](https://github.com/MarlinFirmware/Marlin/issues/367#issuecomment-12505768)
    """

    def __init__(self, state_A: state, state_B: state):
        """Marlin classic jerk specific junction velocity calculation.

        Args:
            state_A: (state) start state
            state_B: (state)   end state
        """
        super().__init__(state_A, state_B)

        self.calc_j_vel()

    def calc_j_vel(self):
        """Calculate the junction velocity."""
        vel_0 = self.target_vel
        vel_1 = self.vel_next
        self.jerk = self.state_B.state_p_settings.jerk * 2

        vel_diff = vel_0 - vel_1
        jerk_move = vel_diff.get_norm()
        scale = jerk_move / self.jerk if self.jerk > 0 else 0

        if scale >= 1:
            self.junction_vel = (vel_0 / scale).get_norm()
        else:
            self.junction_vel = vel_0.get_norm()

    def get_junction_vel(self):
        """Return the calculated junction velocity.

        Returns:
            junction_vel: (float) junction velocity
        """
        return self.junction_vel


class junction_handling_klipper(junction_handling):
    """Klipper specific junction handling.

    - similar junction deviation calc
    - corner vel set by: square_corner_velocity
        end_velocity^2 = start_velocity^2 + 2*accel*move_distance
      for 90deg turn
    - todo: smoothed look ahead

    **Reference:**
    [https://www.klipper3d.org/Kinematics.html](https://www.klipper3d.org/Kinematics.html)
    [https://github.com/Klipper3d/klipper/blob/ea2f6bc0f544132738c7f052ffcc586fa884a19a/klippy/toolhead.py](https://github.com/Klipper3d/klipper/blob/ea2f6bc0f544132738c7f052ffcc586fa884a19a/klippy/toolhead.py)
    """

    def __init__(self, state_A: state, state_B: state):
        """Klipper specific junction velocity calculation.

        Args:
            state_A: (state) start state
            state_B: (state)   end state
        """
        super().__init__(state_A, state_B)

        self.calc_j_delta()
        self.calc_j_vel()

    def calc_j_delta(self):
        """Calculate the junction deviation with klipper specific values.

        The jerk value represents the square_corner_velocity!
        """
        sc_vel = (self.state_B.state_p_settings.jerk) ** 2
        self.j_delta = sc_vel * (math.sqrt(2.0) - 1.0) / self.state_B.state_p_settings.p_acc

    def calc_j_vel(self):
        """Calculate the junction velocity."""
        vel_0 = self.target_vel
        vel_1 = self.vel_next

        if vel_0.get_norm() == 0 or vel_1.get_norm() == 0:
            self.junction_vel = 0
            return

        # calculate junction angle
        dir0 = vel_0.get_norm_dir()
        dir1 = vel_1.get_norm_dir()
        j_cos_theta = -(
            dir0[0] * dir1[0] + dir0[1] * dir1[1] + dir0[2] * dir1[2]
        )  # cos of theta, theta: small angle between velocity vectors

        j_cos_theta = max(j_cos_theta, -0.999999)  # limit
        if j_cos_theta > 0.999999:
            self.junction_vel = 0  # self.target_vel.get_norm()  # if self.target_vel.get_norm() is not None else 0
            return
        j_sin_theta_d2 = math.sqrt(0.5 * (1.0 - j_cos_theta))

        j_R = self.j_delta * j_sin_theta_d2 / (1.0 - j_sin_theta_d2)

        # [from klipper]: Approximated circle must contact moves no further away than mid-move
        j_tan_theta_d2 = j_sin_theta_d2 / math.sqrt(0.5 * (1.0 + j_cos_theta))

        move_centripetal_v2 = 0.5 * self.t_distance * j_tan_theta_d2 * self.state_B.state_p_settings.p_acc

        self.junction_vel = math.sqrt(
            min(self.state_B.state_p_settings.p_acc * j_R, move_centripetal_v2, self.state_B.state_p_settings.speed**2)
        )

    def get_junction_vel(self):
        """Return the calculated junction velocity.

        Returns:
            junction_vel: (float) junction velocity
        """
        return self.junction_vel


class junction_handling_MKA(junction_handling):
    """Anisoprint A4 like junction handling.

    **Reference:**
    [https://github.com/anisoprint/MKA-firmware/blob/6e02973b1b8f325040cc3dbf66ac545ffc5c06b3/src/core/planner/planner.cpp#L1830](https://github.com/anisoprint/MKA-firmware/blob/6e02973b1b8f325040cc3dbf66ac545ffc5c06b3/src/core/planner/planner.cpp#L1830)
    """

    def __init__(self, state_A: state, state_B: state):
        """Marlin classic jerk specific junction velocity calculation.

        Args:
            state_A: (state) start state
            state_B: (state)   end state
        """
        super().__init__(state_A, state_B)

        self.calc_j_vel()

    def calc_j_vel(self):
        """Calculate the junction velocity."""
        vel_0 = self.target_vel
        vel_1 = self.vel_next
        self.jerk = self.state_B.state_p_settings.jerk

        v_max_junc = min(vel_0.get_norm(), vel_1.get_norm())
        small_speed_fac = v_max_junc / vel_0.get_norm() if v_max_junc > 0 else 0

        v_factor = 1
        lim_flag = False

        for v_entry, v_exit in zip(vel_0.get_vec(withExtrusion=True), vel_1.get_vec(withExtrusion=True)):
            v_exit *= small_speed_fac

            if lim_flag:
                v_entry *= v_factor
                v_exit *= v_factor

            jerk = (
                ((v_exit - v_entry) if (v_entry > 0 or v_exit < 0) else max(v_exit, -v_entry))
                if (v_exit > v_entry)
                else (v_entry - v_exit if (v_entry < 0 or v_exit > 0) else max(-v_exit, v_entry))
            )  # calc logic taken from MKA firmware

            if jerk > self.jerk:
                v_factor *= self.jerk / jerk
                lim_flag = True

            if lim_flag:
                v_max_junc *= v_factor

            self.junction_vel = v_max_junc

    def get_junction_vel(self):
        """Return the calculated junction velocity.

        Returns:
            junction_vel: (float) junction velocity
        """
        return self.junction_vel
