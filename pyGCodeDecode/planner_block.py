# -*- coding: utf-8 -*-
from typing import List

import numpy as np

from .state import segment, state
from .utils import velocity


class planner_block:
    def calc_JD(self, vel_0: velocity, vel_next: velocity, p_settings: state.p_settings):
        """
        Calculates junction deviation velocity from 2 velocitys.

        Parameters
        ----------
        vel_0,vel_1 : velocity
            velocity objects
        p_settings  : state.p_settings
            print settings, containing acceleration settings
        Returns
        ----------
        velocity
            velocity abs value

        Reference
        ----------
        [1]: https://onehossshay.wordpress.com/2011/09/24/improving_grbl_cornering_algorithm/
        [2]: http://blog.kyneticcnc.com/2018/10/computing-junction-deviation-for-marlin.html

        """
        # Junction deviation settings
        JD_acc = p_settings.p_acc
        if p_settings.jerk == 0:
            return 0
        JD_delta = 0.4 * p_settings.jerk * p_settings.jerk / JD_acc  # [2]
        JD_minAngle = 18
        JD_maxAngle = 180 - 18
        vel_0_vec = vel_0.get_vec()
        vel_1_vec = vel_next.get_vec()
        if vel_0.get_norm() == 0 or vel_next.get_norm() == 0:
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

                return JD_velocity_scalar if JD_velocity_scalar < vel_0.get_norm() else vel_0.get_norm()
            else:
                return 0  # angle smaller than min angle, stop completely
        else:
            return vel_0.get_norm()  # angle larger than max angle, full speed pass

    def connect_state(self, state_0: state, state_next: state):
        """
        Connects two states and generates the velocity for the move from state_0 to state_next

        Parameters
        ----------
        state_0, state_next  :   state
            two consecutive states

        Returns
        ----------
        velocity
            the target velocity for that travel move
        """
        if state_0 is None or state_next is None:
            return velocity(0, 0, 0, 0)
        travel_direction = np.subtract(
            state_next.state_position.get_vec(withExtrusion=True), state_0.state_position.get_vec(withExtrusion=True)
        )  # outdated todo
        t_distance = np.linalg.norm(travel_direction[:3])
        e_len = travel_direction[3]
        if abs(t_distance) > 0:  # regular travel mixed move
            travel_direction = travel_direction / t_distance
        elif abs(e_len) > 0:  # for extrusion only move
            travel_direction = travel_direction / abs(e_len)
        else:  # no move at all
            travel_direction = np.asarray([0, 0, 0, 0])
        speed = velocity(state_next.state_p_settings.speed * travel_direction)
        return speed

    def move_maker2(self, v_end):
        """
        WIP Method that ignores the beginning velocity if end velocity is not reachable
        Calculates the correct move type (trapezoidal,triangular or singular) and generates the corresponding Segments

        Parameters
        ----------
        direction   :   float list 1x4
            travel direction, vectorial
        mov_vel_end :   velocity
            target velocity for end of move (currently not guaranteed to be met, however a warning will be spit)
        settings    :   p_settings
            printing settings for corresponding move
        distance    :   float
            travel distance for move
        previous_segment:   segment
            the previous segment, used to apply JD-Velocity at begin of move

        Returns
        ----------
        segment list
            list of Segments for move
        """

        def trapez(extrusion_only=False):
            # A /
            t0 = previous_segment.t_end
            t1 = t0 + (v_target - v_begin) / acc
            pos_begin = previous_segment.pos_end
            pos_end = pos_begin + self.direction * travel_ramp_up
            vel_begin = velocity(self.direction * v_begin)
            vel_end = vel_const
            segment_A = segment(
                t_begin=t0, t_end=t1, pos_begin=pos_begin, pos_end=pos_end, vel_begin=vel_begin, vel_end=vel_end
            )
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin):
                self.segments.append(segment_A)
            # B --
            travel_const = distance - travel_ramp_down - travel_ramp_up
            v_const = vel_const.get_norm(withExtrusion=extrusion_only)  # abs of vel const
            t2 = t1 + travel_const / v_const  # time it takes to travel the remaining distance
            pos_begin = segment_A.pos_end
            pos_end = pos_begin + self.direction * travel_const
            vel_begin = vel_const
            vel_end = vel_const
            segment_B = segment(
                t_begin=t1, t_end=t2, pos_begin=pos_begin, vel_begin=vel_begin, pos_end=pos_end, vel_end=vel_end
            )
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin):
                self.segments.append(segment_B)
            # C \
            t2 = segment_B.t_end
            t3 = t2 + (v_target - v_end) / acc
            pos_begin = segment_B.pos_end
            pos_end = pos_begin + self.direction * travel_ramp_down
            vel_begin = segment_B.vel_end
            vel_end = velocity(self.direction * v_end)
            segment_C = segment(
                t_begin=t2, t_end=t3, pos_begin=pos_begin, pos_end=pos_end, vel_begin=vel_begin, vel_end=vel_end
            )
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin):
                self.segments.append(segment_C)

            self.blcktype = "trapez"

        def triang(extrusion_only=False):
            # A /
            t0 = previous_segment.t_end
            t1 = t0 + (v_peak_tri - v_begin) / acc
            pos_begin = previous_segment.pos_end
            travel_ramp_up = (v_peak_tri - v_begin) * (v_begin + v_peak_tri) / (2 * acc)
            pos_end = pos_begin + self.direction * travel_ramp_up
            vel_begin = velocity(self.direction * v_begin)
            vel_end = velocity(self.direction * v_peak_tri)
            segment_A = segment(
                t_begin=t0, t_end=t1, pos_begin=pos_begin, pos_end=pos_end, vel_begin=vel_begin, vel_end=vel_end
            )
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin):
                self.segments.append(segment_A)
            # C \
            t2 = segment_A.t_end
            t3 = t2 + (v_peak_tri - v_end) / acc
            pos_begin = segment_A.pos_end
            travel_ramp_down = (v_peak_tri - v_end) * (v_end + v_peak_tri) / (2 * acc)
            pos_end = pos_begin + self.direction * travel_ramp_down
            vel_begin = segment_A.vel_end
            vel_end = velocity(self.direction * v_end)
            segment_C = segment(
                t_begin=t2, t_end=t3, pos_begin=pos_begin, pos_end=pos_end, vel_begin=vel_begin, vel_end=vel_end
            )
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin):
                self.segments.append(segment_C)

            self.blcktype = "triangle"

        def singl_up():
            # A /
            t0 = previous_segment.t_end
            t1 = t0 + (v_end_sing - v_begin) / acc
            pos_begin = previous_segment.pos_end
            travel_ramp_up = (v_end_sing - v_begin) * (v_begin + v_end_sing) / (2 * acc)
            pos_end = pos_begin + self.direction * travel_ramp_up
            vel_begin = velocity(self.direction * v_begin)
            vel_end = velocity(self.direction * v_end_sing)
            segment_A = segment(
                t_begin=t0, t_end=t1, pos_begin=pos_begin, pos_end=pos_end, vel_begin=vel_begin, vel_end=vel_end
            )
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin):
                self.segments.append(segment_A)

            self.blcktype = "single"

        def singl_dwn():
            # C \ with forced end point met
            t0 = previous_segment.t_end
            t1 = t0 + (v_begin_sing - v_end) / acc
            pos_begin = previous_segment.pos_end
            travel_ramp_up = (v_begin_sing - v_end) * (v_begin_sing + v_end) / (2 * acc)
            pos_end = pos_begin + self.direction * travel_ramp_up
            vel_begin = velocity(self.direction * v_begin_sing)
            vel_end = velocity(self.direction * v_end)
            segment_C = segment(
                t_begin=t0, t_end=t1, pos_begin=pos_begin, pos_end=pos_end, vel_begin=vel_begin, vel_end=vel_end
            )
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin):
                self.segments.append(segment_C)

            self.blcktype = "single"

        extrusion_only = False  # flag
        self.segments = []  # clear segments
        if self.state_A is not None:
            distance = self.state_B.state_position.get_t_distance(old_position=self.state_A.state_position)
            if distance == 0:  # no travel, extrusion possible
                distance = self.state_B.state_position.get_t_distance(
                    old_position=self.state_A.state_position, withExtrusion=True
                )
                extrusion_only = True
        else:
            distance = 0
        previous_segment = (
            self.prev_blck.get_segments()[-1]
            if self.prev_blck is not None
            else segment.create_initial(initial_position=self.state_A.state_position)
        )
        settings = self.state_B.state_p_settings

        # convert Velocities (vel: Object) to travel speeds (v: mm/s)
        acc = settings.p_acc
        v_target = settings.speed
        v_begin = previous_segment.vel_end.get_norm()

        # calculate min travel for trapezoidal shape, if sum larger than distance, regular movement pattern is possible
        travel_ramp_up = (v_target - v_begin) * (v_begin + v_target) / (2 * acc)
        travel_ramp_down = (v_end - v_target) * (v_end + v_target) / (2 * -acc)
        vel_const = velocity(self.direction * v_target)
        v_peak_tri = np.sqrt(acc * distance + v_begin * v_begin / 2 + v_end * v_end / 2)

        if v_begin > v_end:
            v_end_sing_sqr = v_begin * v_begin - 2 * acc * distance
        else:
            v_end_sing_sqr = v_begin * v_begin + 2 * acc * distance
        v_end_sing = np.sqrt(v_end_sing_sqr) if v_end_sing_sqr >= 0 else None
        v_begin_sing = np.sqrt(2 * acc * distance + v_end * v_end)

        # select case for planner block and calculate segment vertices
        if (travel_ramp_down + travel_ramp_up) < distance:
            trapez(extrusion_only=extrusion_only)
        elif v_peak_tri > v_end and v_peak_tri > v_begin:
            triang()
        elif v_end_sing > v_begin:
            singl_up()
        elif v_end_sing < v_begin:
            singl_dwn()
        else:
            raise NameError("Segment could not be modeled.")

    def self_correction(self, tolerance=float("1e-12")):
        # Check interface points
        flag_correct = False
        if self.next_blck is not None:
            same_vel = (
                self.get_segments()[-1].vel_end.get_norm() == self.next_blck.get_segments()[0].vel_begin.get_norm()
            )
            if not same_vel:
                error_vel = (
                    self.get_segments()[-1].vel_end.get_norm() - self.next_blck.get_segments()[0].vel_begin.get_norm()
                )
                if error_vel > tolerance:
                    # print("Velocity error: ", error_vel)
                    flag_correct = True

        # Correct error by recalculating velocitys with new vel_end
        if self.next_blck is not None and flag_correct:
            vel_end = self.next_blck.get_segments()[0].vel_begin.get_norm()
            self.move_maker2(v_end=vel_end)
            if self.blcktype == "single":
                self.prev_blck.self_correction()  # forward correction?

        # Timeshift the corrected blocks
        if self.next_blck is not None:
            delta_t = self.get_segments()[-1].t_end - self.next_blck.get_segments()[0].t_begin
            self.next_blck.timeshift(delta_t=delta_t)

        # Check continuity in Position
        if self.next_blck is not None:
            same_position = self.get_segments()[-1].pos_end == self.next_blck.get_segments()[0].pos_begin
            if not same_position:
                error_position = self.get_segments()[-1].pos_end - self.next_blck.get_segments()[0].pos_begin
                dist = error_position.get_t_distance()
                if dist > tolerance:
                    print(dist)
                    raise NameError("disconinuity in segments detected")
        return flag_correct

    def timeshift(self, delta_t: float):
        pass
        if len(self.segments) > 0:
            for segm in self.segments:
                segm.move_segment_time(delta_t)

    def __init__(self, state: state, prev_blck: "planner_block"):
        """calculates and stores Single Planner Block consisting of multiple Segments
        move is from previous to the current state
        """
        # neighbor list
        self.state_A = state.prev_state  # from state A
        self.state_B = state  # to state B
        self.prev_blck = prev_blck  # nb list prev
        self.next_blck = None  # nb list next

        self.segments: List[segment] = []  # store segments here
        self.blcktype = None

        # planner block calculation
        vel_blck = self.connect_state(
            state_0=self.state_A, state_next=self.state_B
        )  # target velocity for this plannerblock
        vel_next = self.connect_state(
            state_0=self.state_B, state_next=self.state_B.next_state
        )  # target velocity for next plannerblock
        v_JD = self.calc_JD(
            vel_0=vel_blck, vel_next=vel_next, p_settings=state.state_p_settings
        )  # junction deviation speed for end of block

        self.direction = vel_blck.get_norm_dir(withExtrusion=True)  # direction vector of pb
        self.valid = vel_blck.not_zero()  # valid planner block

        if self.valid:
            self.JD = v_JD * self.direction  # jd writeout for debugging plot
            self.move_maker2(v_end=v_JD)

    @property
    def prev_blck(self):
        return self._prev_blck

    @prev_blck.setter
    def prev_blck(self, blck: "planner_block"):
        self._prev_blck = blck

    @property
    def next_blck(self):
        return self._next_blck

    @next_blck.setter
    def next_blck(self, blck: "planner_block"):
        self._next_blck = blck

    def __str__(self) -> str:
        if len(self.segments) == 3:
            return "{:-^40}".format("Trapez Planner Block")
        elif len(self.segments) == 2:
            return "{:-^40}".format("Triangular Planner Block")
        elif len(self.segments) == 1:
            return "{:-^40}".format("Singular Planner Block")
        else:
            return "{:#^40}".format("Invalid Planner Block")

    def __repr__(self) -> str:
        return self.__str__()

    def get_segments(self):
        return self.segments
