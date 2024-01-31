# -*- coding: utf-8 -*-
"""State module with state."""
from .utils import position


class state:
    """State contains a Position and Printing Settings (p_settings) to apply for the corresponding move to this State."""

    class p_settings:
        """Store Printing Settings."""

        def __init__(self, p_acc, jerk, vX, vY, vZ, vE, speed, units="SImm"):
            """Initialize printing settings.

            Args:
                p_acc: (float) printing acceleration
                jerk: (float) jerk or similar
                vX: (float) max x velocity
                vY: (float) max y velocity
                vZ: (float) max z velocity
                vE: (float) max e velocity
                speed: (float) default target velocity
                units: (string, default = "SImm") unit settings
            """
            self.p_acc = p_acc  # printing acceleration
            self.jerk = jerk  # jerk settings
            self.vX = vX  # max axis speed X
            self.vY = vY  # max axis speed Y
            self.vZ = vZ  # max axis speed Z
            self.vE = vE  # max axis speed E
            self.speed = speed  # travel speed for move
            self.units = units  # unit system used

        def __str__(self) -> str:
            """Create summary string for p_settings."""
            return (
                "jerk: "
                + str(self.jerk)
                + ", p_acc: "
                + str(self.p_acc)
                + ", max_ax_vel: ["
                + str(self.vX)
                + ", "
                + str(self.vY)
                + ", "
                + str(self.vZ)
                + ", "
                + str(self.vE)
                + "]"
                + ", p_vel: "
                + str(self.speed)
                + ", units: "
                + str(self.units)
            )

        def __repr__(self) -> str:
            """Define representation."""
            return self.__str__()

    def __init__(self, state_position: position = None, state_p_settings: p_settings = None):
        """Initialize a state.

        Args:
            state_position: (position) state position
            state_p_settings: (p_settings) state printing settings
        """
        self.state_position = state_position
        self.state_p_settings = state_p_settings
        self.next_state = None
        self.prev_state = None
        self.line_number = None
        self.comment = None
        self.layer = None
        self.pause = None

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
    def line_number(self):
        """Define property line_nmbr."""
        return self._line_nmbr

    @line_number.setter
    def line_number(self, nmbr):
        """Set line number.

        Args:
            nmbr: (int) line number
        """
        self._line_nmbr = nmbr

    # Neighbor list
    @property
    def next_state(self):
        """Define property next_state."""
        return self._next_state

    @next_state.setter
    def next_state(self, state: "state"):
        """Set next state.

        Args:
            state: (state) next state
        """
        self._next_state = state

    @property
    def prev_state(self):
        """Define property prev_state."""
        return self._prev_state

    @prev_state.setter
    def prev_state(self, state: "state"):
        """Set previous state.

        Args:
            state: (state) previous state
        """
        self._prev_state = state

    def __str__(self) -> str:
        """Generate string for representation."""
        if self.layer is not None:
            return f"<state: line: {str(self.line_number)}, layer: {self.layer}, {self.state_position}, settings: {self.state_p_settings}, comment: {self.comment}, pause: {str(self.pause)}>\n"  # noqa E501
        else:
            return f"<state: line: {str(self.line_number)}, {self.state_position}, settings: {self.state_p_settings}, comment: {self.comment}, pause: {str(self.pause)}>\n"  # noqa E501

    def __repr__(self) -> str:
        """Call __str__() for representation."""
        return self.__str__()
