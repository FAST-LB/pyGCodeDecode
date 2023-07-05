# -*- coding: utf-8 -*-
"""State module with state."""
from .utils import position


class state:
    """State contains a Position and Printing Settings (p_settings) to apply for the corresponding move to this State."""

    class p_settings:
        """
        Store Printing Settings.

        Supports
            str,repr
        Class method
            new:            returns an updated p_settings from given old p_settings and optional changing values
        """

        def __init__(self, p_acc, jerk, Vx, Vy, Vz, Ve, speed, absMode=True, units="SImm"):
            """Initialize printing settings with p_acc, jerk, Vx, Vy, Vz, Ve, speed, absMode=True, units="SImm"."""
            self.p_acc = p_acc  # printing acceleration
            self.jerk = jerk  # jerk settings
            self.Vx = Vx  # max axis speed X
            self.Vy = Vy  # max axis speed Y
            self.Vz = Vz  # max axis speed Z
            self.Ve = Ve  # max axis speed E
            self.speed = speed  # travel speed for move
            self.absMode = absMode  # abs extrusion mode, default = True [deprecated]
            self.units = units  # unit system used

        def __str__(self) -> str:
            """Create summary string for p_settings."""
            return (
                "jerk: "
                + str(self.jerk)
                + ", p_acc: "
                + str(self.p_acc)
                + ", max_ax_vel: ["
                + str(self.Vx)
                + ", "
                + str(self.Vy)
                + ", "
                + str(self.Vz)
                + ", "
                + str(self.Ve)
                + "]"
                + ", p_vel: "
                + str(self.speed)
                + " Abs Extr: "
                + str(self.absMode)
                + ", units: "
                + str(self.units)
            )

        def __repr__(self) -> str:
            """Define representation."""
            return self.__str__()

    def __init__(self, state_position: position = None, state_p_settings: p_settings = None):
        """Initialize a state."""
        self.state_position = state_position
        self.state_p_settings = state_p_settings
        self.next_state = None
        self.prev_state = None
        self.line_nmbr = None
        self.comment = None
        self.layer = None

    @property
    def state_position(self):
        """Define property state_position."""
        return self._state_position

    @state_position.setter
    def state_position(self, set_position: position):
        self._state_position = set_position

    @property
    def state_p_settings(self):
        """Define property state_p_settings."""
        return self._state_p_settings

    @state_p_settings.setter
    def state_p_settings(self, set_p_settings: p_settings):
        self._state_p_settings = set_p_settings

    @property
    def line_nmbr(self):
        """Define property line_nmbr."""
        return self._line_nmbr

    @line_nmbr.setter
    def line_nmbr(self, nmbr):
        self._line_nmbr = nmbr

    # Neighbor list
    @property
    def next_state(self):
        """Define property next_state."""
        return self._next_state

    @next_state.setter
    def next_state(self, state: "state"):
        self._next_state = state

    @property
    def prev_state(self):
        """Define property prev_state."""
        return self._prev_state

    @prev_state.setter
    def prev_state(self, state: "state"):
        self._prev_state = state

    def __str__(self) -> str:
        """Generate string for representation."""
        if self.layer is not None:
            return f"<state: line: {str(self.line_nmbr)}, layer: {self.layer}, {self.state_position}, settings: {self.state_p_settings}, comment: {self.comment}>\n"  # noqa E501
        else:
            return f"<state: line: {str(self.line_nmbr)}, {self.state_position}, settings: {self.state_p_settings}, comment: {self.comment}>\n"

    def __repr__(self) -> str:
        """Call __str__() for representation."""
        return self.__str__()
