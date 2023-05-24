# -*- coding: utf-8 -*-
from typing import List

import numpy as np

from .utils import position, velocity


class state:
    class p_settings:
        """Store Printing Settings
        Supports
            str,repr
        Class method
            new:            returns an updated p_settings from given old p_settings and optional changing values
        """

        def __init__(self, p_acc, jerk, Vx, Vy, Vz, Ve, speed, absMode=True):
            self.p_acc = p_acc  # printing acceleration
            self.jerk = jerk  # jerk settings
            self.Vx = Vx  # max axis speed X
            self.Vy = Vy  # max axis speed Y
            self.Vz = Vz  # max axis speed Z
            self.Ve = Ve  # max axis speed E
            self.speed = speed  # travel speed for move
            self.absMode = absMode  # abs extrusion mode, default = True

        def __str__(self) -> str:
            return (
                ">>> Print Settings:\nJerk: "
                + str(self.jerk)
                + "\nPrinting Acceleration: "
                + str(self.p_acc)
                + "\nMaximum Axis Speeds: [Vx:"
                + str(self.Vx)
                + ", Vy:"
                + str(self.Vy)
                + ", Vz:"
                + str(self.Vz)
                + ", Ve:"
                + str(self.Ve)
                + "]\n"
                + "Printing speed: "
                + str(self.speed)
                + "\n"
                + "Abs Extr: "
                + str(self.absMode)
                + "\n"
            )

        def __repr__(self) -> str:
            return self.__str__()

        @classmethod
        def new(
            cls,
            old_settings: "state.p_settings",
            p_acc: float = None,
            jerk: float = None,
            Vx: float = None,
            Vy: float = None,
            Vz: float = None,
            Ve: float = None,
            speed: float = None,
            absMode: bool = None,
        ):
            if p_acc is None:
                p_acc = old_settings.p_acc
            if jerk is None:
                jerk = old_settings.jerk
            if Vx is None:
                Vx = old_settings.Vx
            if Vy is None:
                Vy = old_settings.Vy
            if Vz is None:
                Vz = old_settings.Vz
            if Ve is None:
                Ve = old_settings.Ve
            if speed is None:
                speed = old_settings.speed
            if absMode is None:
                absMode = old_settings.absMode
            return cls(p_acc=p_acc, jerk=jerk, Vx=Vx, Vy=Vy, Vz=Vz, Ve=Ve, speed=speed, absMode=absMode)

    """State contains a Position and the gcode-defined Printing Settings (p_settings) to apply for the corresponding move to the Position
    Supports
        str
    Class method
        new: returns new State from old State and given optional changing Position and/or Print Settings
    """

    def __init__(self, state_position: position = None, state_p_settings: p_settings = None):
        self.state_position = state_position
        self.state_p_settings = state_p_settings
        self.next_state = None
        self.prev_state = None
        self.line_nmbr = None
        self.comment = None

    @property
    def state_position(self):
        return self._state_position

    @state_position.setter
    def state_position(self, set_position: position):
        self._state_position = set_position

    @property
    def state_p_settings(self):
        return self._state_p_settings

    @state_p_settings.setter
    def state_p_settings(self, set_p_settings: p_settings):
        self._state_p_settings = set_p_settings

    @property
    def line_nmbr(self):
        return self._line_nmbr

    @line_nmbr.setter
    def line_nmbr(self, nmbr):
        self._line_nmbr = nmbr

    # Neighbor list
    @property
    def next_state(self):
        return self._next_state

    @next_state.setter
    def next_state(self, state: "state"):
        self._next_state = state

    @property
    def prev_state(self):
        return self._prev_state

    @prev_state.setter
    def prev_state(self, state: "state"):
        self._prev_state = state

    def __str__(self) -> str:
        return f"<state: line({self.line_nmbr}), comment({self.comment}) pos({self.state_position}), settings({self.state_p_settings})>"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def new(cls, old_state: "state", position: position = None, p_settings: p_settings = None):
        if position is None:
            position = old_state.position
        if p_settings is None:
            p_settings = old_state.p_settings
        return cls(state_position=position, state_p_settings=p_settings)


class segment:
    """stores Segment data for linear 4D Velocity function segment, contains: time,position,velocity
    Supports
        str
    Additional methods
        move_segment_time:      moves Segment in time by a specified interval
        get_velocity:           returns the calculated Velocity for all axis at a given point in time
        get_position:           returns the calculated Position for all axis at a given point in time
    Class method
        create_initial:         returns the artificial initial segment where everything is at standstill, intervall length = 0
        self_check:             returns True if all self checks have been successfull
    """

    def __init__(
        self,
        t_begin: float,
        t_end: float,
        pos_begin: position,
        vel_begin: velocity,
        pos_end: position = None,
        vel_end: velocity = None,
    ):
        self.t_begin = t_begin
        self.t_end = t_end
        self.pos_begin = pos_begin
        self.pos_end = pos_end
        self.vel_begin = vel_begin
        self.vel_end = vel_end
        self.self_check()

    def __str__(self) -> str:
        # distance = self.pos_end.get_t_distance(old_position=self.pos_begin) if not self.pos_end is None else 0
        # return f"Segment length: {distance} mm from {self.t_begin}s to {self.t_end}s\nv_begin: {self.vel_begin}\tv_end: {self.vel_end}\n"
        return f"\nSegment from: \n{self.pos_begin} to \n{self.pos_end} Self check: {self.self_check()}.\n"

    def __repr__(self):
        return self.__str__()

    def move_segment_time(self, delta_t: float):
        self.t_begin = self.t_begin + delta_t
        self.t_end = self.t_end + delta_t

    def get_velocity(self, t):
        if t < self.t_begin or t > self.t_end:
            raise ValueError("Segment not defined for this point in time.")
        else:
            # linear interpolation of velocity in Segment
            delt_vel = self.vel_end - self.vel_begin
            delt_t = self.t_end - self.t_begin
            slope = delt_vel / delt_t if delt_t > 0 else velocity(0, 0, 0, 0)
            current_vel = self.vel_begin + slope * (t - self.t_begin)
            return current_vel

    def get_position(self, t):
        if t < self.t_begin or t > self.t_end:
            raise ValueError("Segment not defined for this point in time.")
        else:
            current_vel = self.get_velocity(t=t)
            position = self.pos_begin + ((self.vel_begin + current_vel) * (t - self.t_begin) / 2.0).get_vec(
                withExtrusion=True
            )
            return position

    def self_check(self):  # ,tolerance=float("e-13"), state:state=None):
        # WIP, check for self consistency
        # > travel distance
        position = self.pos_begin + ((self.vel_begin + self.vel_end) * (self.t_end - self.t_begin) / 2.0).get_vec(
            withExtrusion=True
        )
        pos_check = self.pos_end == position
        if pos_check:
            return pos_check
        else:
            error_distance = np.linalg.norm(np.asarray(self.pos_end.get_vec()) - np.asarray(position.get_vec()))
            return "Error distance: " + str(error_distance)
        # > max acceleration
        # > max velocity
        # ..more?

    @classmethod
    def create_initial(cls, initial_position: position = None):
        velocity_0 = velocity(0, 0, 0, 0)
        pos_0 = position(x=0, y=0, z=0, e=0) if initial_position is None else initial_position
        return cls(t_begin=0, t_end=0, pos_begin=pos_0, vel_begin=velocity_0, pos_end=pos_0, vel_end=velocity_0)
