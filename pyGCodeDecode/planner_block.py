# -*- coding: utf-8 -*-
"""Planner block Module."""
from typing import List

import numpy as np

from .junction_handling import (
    junction_handling,
    junction_handling_klipper,
    junction_handling_marlin_jd,
    junction_handling_marlin_jerk,
    junction_handling_MKA,
)
from .state import state
from .utils import segment, velocity


class planner_block:
    """Planner Block Class."""

    def move_maker2(self, v_end):
        """
        Calculate the correct move type (trapezoidal,triangular or singular) and generate the corresponding segments.

        Args:
            vel_end: (velocity) target velocity for end of move
        """

        def trapezoid(extrusion_only=False):
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
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin, ignore_retract=False):
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
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin, ignore_retract=False):
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
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin, ignore_retract=False):
                self.segments.append(segment_C)

            self.blocktype = "trapezoid"

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
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin, ignore_retract=False):
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
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin, ignore_retract=False):
                self.segments.append(segment_C)

            self.blocktype = "triangle"

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
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin, ignore_retract=False):
                self.segments.append(segment_A)

            self.blocktype = "single"

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
            if pos_end.is_travel(pos_begin) or pos_end.is_extruding(pos_begin, ignore_retract=False):
                self.segments.append(segment_C)

            self.blocktype = "single"

        extrusion_only = False  # flag
        self.segments = []  # clear segments
        if self.state_A is not None:
            distance = self.state_B.state_position.get_t_distance(other=self.state_A.state_position)
            if distance == 0:  # no travel, extrusion possible
                distance = self.state_B.state_position.get_t_distance(
                    other=self.state_A.state_position, withExtrusion=True
                )
                extrusion_only = True
        else:
            distance = 0
        previous_segment = (
            self.prev_block.get_segments()[-1]
            if self.prev_block is not None
            else segment.create_initial(initial_position=self.state_A.state_position)
        )
        settings = self.state_B.state_p_settings

        # convert Velocities (vel: Object) to travel speeds (v: mm/s)
        acc = settings.p_acc
        v_target = settings.speed
        v_begin = previous_segment.vel_end.get_norm()
        v_begin = v_begin if v_begin < v_target else v_target

        # calculate min travel for trapezoidal shape, if sum larger than distance, regular movement pattern is possible
        travel_ramp_up = (v_target - v_begin) * (v_begin + v_target) / (2 * acc)
        travel_ramp_down = (v_end - v_target) * (v_end + v_target) / (2 * -acc)
        vel_const = velocity(self.direction * v_target)
        v_peak_tri = np.sqrt(acc * distance + v_begin * v_begin / 2 + v_end * v_end / 2)

        if v_begin > v_end:
            v_end_sing_sqr = v_begin * v_begin - 2 * acc * distance
        else:
            v_end_sing_sqr = v_begin * v_begin + 2 * acc * distance
        v_end_sing = np.sqrt(v_end_sing_sqr) if v_end_sing_sqr >= 0 else 0
        v_begin_sing = np.sqrt(2 * acc * distance + v_end * v_end)

        # select case for planner block and calculate segment vertices
        try:
            if (
                (travel_ramp_up + travel_ramp_down) < distance
                and (travel_ramp_up > 0 or np.isclose(travel_ramp_up, 0.0))
                and (travel_ramp_down > 0 or np.isclose(travel_ramp_down, 0.0))
            ):
                trapezoid(extrusion_only=extrusion_only)
            elif (
                v_peak_tri > v_end
                and v_peak_tri > v_begin
                and (v_peak_tri < v_target or np.isclose(v_peak_tri, v_target))
            ):
                triang(extrusion_only=extrusion_only)
            elif v_end_sing > v_begin and (v_end_sing < v_target or np.isclose(v_end_sing, v_target)):
                singl_up()
            elif v_end_sing < v_begin:
                singl_dwn()
            else:
                raise NameError(
                    "Segment could not be modeled: \n"
                    + str(self.state_A)
                    + "\n"
                    + str(self.state_B)
                    + f"\nv-begin {v_begin} / v-target {v_target} / v-end {v_end} "
                )

        except ValueError as ve:
            print(f"Segments to state: {str(self.state_B)} could not be modeled.\n {ve}")
            raise RuntimeError()

    def self_correction(self, tolerance=float("1e-12")):
        """Check for interfacing vel and self correct."""
        flag_correct = False
        if self.next_block is not None:
            same_vel = (
                self.get_segments()[-1].vel_end.get_norm() == self.next_block.get_segments()[0].vel_begin.get_norm()
            )
            if not same_vel:
                error_vel = abs(
                    self.get_segments()[-1].vel_end.get_norm() - self.next_block.get_segments()[0].vel_begin.get_norm()
                )
                if error_vel > tolerance:
                    flag_correct = True

        # Correct error by recalculating velocitys with new vel_end
        if self.next_block is not None and flag_correct:
            vel_end = self.next_block.get_segments()[0].vel_begin.get_norm()
            self.move_maker2(v_end=vel_end)
            if self.blocktype == "single":
                self.prev_block.self_correction()  # forward correction?

        # Timeshift the corrected blocks
        if self.next_block is not None:
            delta_t = self.get_segments()[-1].t_end - self.next_block.get_segments()[0].t_begin
            self.next_block.timeshift(delta_t=delta_t)

        # Check continuity in Position
        if self.next_block is not None:
            same_position = self.get_segments()[-1].pos_end == self.next_block.get_segments()[0].pos_begin
            if not same_position:
                error_position = self.get_segments()[-1].pos_end - self.next_block.get_segments()[0].pos_begin
                dist = error_position.get_t_distance()
                if dist > tolerance:
                    raise NameError(f"Disconinuity of {dist} in segments detected")

        # Check if segment adheres to settings
        try:
            for segm in self.segments:
                segm.self_check(p_settings=self.state_B.state_p_settings)
        except ValueError as ve:
            print(f"Segment for {self.state_B} does not adhere to machine limits: {ve}")

        return flag_correct

    def timeshift(self, delta_t: float):
        """Shift planner block in time.

        Args:
            delta_t: (float) time to be shifted
        """
        if len(self.segments) > 0:
            for segm in self.segments:
                segm.move_segment_time(delta_t)

    def extrusion_block_max_vel(self):
        """Return max vel from planner block while extruding.

        Returns:
            block_max_vel: (np.ndarray 1x4) maximum axis velocity while extruding in block
        """
        if self.is_extruding:
            all_vel_extruding = np.asarray(
                [
                    [
                        [abs(ax_vel) for ax_vel in segm.vel_begin.get_vec(withExtrusion=True)],
                        [abs(ax_vel) for ax_vel in segm.vel_end.get_vec(withExtrusion=True)],
                    ]
                    for segm in self.segments
                ]
            )
            all_vel_extruding = np.reshape(all_vel_extruding, (-1, 4))
            # print("all_vel:", all_vel_extruding)
            block_max_vel = np.amax(all_vel_extruding, axis=0)
            # print("maxvel", block_max_vel)
            return block_max_vel
        else:
            pass

    def __init__(self, state: state, prev_block: "planner_block", firmware=None):
        """Calculate and store planner block consisting of one or multiple segments.

        Args:
            state: (state) the current state
            prev_block: (planner_block) previous planner block
            firmware: (string, default = None) firmware selection for junction
        """
        # neighbor list
        self.state_A = state.prev_state  # from state A
        self.state_B = state  # to state B
        self.prev_block = prev_block  # nb list prev
        self.next_block = None  # nb list next
        self.is_extruding = False  # default Value

        self.segments: List[segment] = []  # store segments here
        self.blocktype = None

        if firmware == "marlin_jd":
            junction = junction_handling_marlin_jd(state_A=self.state_A, state_B=self.state_B)
        elif firmware == "klipper":
            junction = junction_handling_klipper(state_A=self.state_A, state_B=self.state_B)
        elif firmware == "marlin_jerk":
            junction = junction_handling_marlin_jerk(state_A=self.state_A, state_B=self.state_B)
        elif firmware == "MKA":
            junction = junction_handling_MKA(state_A=self.state_A, state_B=self.state_B)
        else:
            junction = junction_handling(state_A=self.state_A, state_B=self.state_B)

        # planner block calculation
        target_vel = junction.get_target_vel()  # target velocity for this planner block

        v_JD = junction.get_junction_vel()

        self.direction = target_vel.get_norm_dir(withExtrusion=True)  # direction vector of pb

        self.valid = target_vel.not_zero()  # valid planner block

        # standard move maker
        if self.valid:
            self.JD = v_JD * self.direction  # jd writeout for debugging plot
            self.move_maker2(v_end=v_JD)
            self.is_extruding = self.state_A.state_position.is_extruding(
                self.state_B.state_position
            )  # store extrusion flag

        # dwell functionality
        if self.state_B.pause is not None:
            self.JD = [0, 0, 0, 0]
            self.segments = [
                segment(
                    t_begin=self.prev_block.segments[-1].t_end,
                    t_end=self.prev_block.segments[-1].t_end + self.state_B.pause,
                    pos_begin=self.prev_block.segments[-1].pos_end,
                    pos_end=self.prev_block.segments[-1].pos_end,
                    vel_begin=velocity(0, 0, 0, 0),
                    vel_end=velocity(0, 0, 0, 0),
                )
            ]

    @property
    def prev_block(self):
        """Define prev_block as property."""
        return self._prev_block

    @prev_block.setter
    def prev_block(self, block: "planner_block"):
        self._prev_block = block

    @property
    def next_block(self):
        """Define next_block as property."""
        return self._next_block

    @next_block.setter
    def next_block(self, block: "planner_block"):
        self._next_block = block

    def __str__(self) -> str:
        """Create string from planner block."""
        if len(self.segments) == 3:
            return "{:-^40}".format("Trapezoid Planner Block")
        elif len(self.segments) == 2:
            return "{:-^40}".format("Triangular Planner Block")
        elif len(self.segments) == 1:
            return "{:-^40}".format("Singular Planner Block")
        else:
            return "{:#^40}".format("Invalid Planner Block")

    def __repr__(self) -> str:
        """Represent planner block."""
        return self.__str__()

    def get_segments(self):
        """Return segments, contained by the planner block."""
        return self.segments

    def get_block_travel(self):
        """Return the travel length of the planner block."""
        return self.state_A.state_position.get_t_distance(self.state_B.state_position)
