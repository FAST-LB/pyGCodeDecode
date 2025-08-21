"""State module with state."""

from .utils import position


class state:
    """State contains a Position and Printing Settings (p_settings) to apply for the corresponding move to this State."""

    class p_settings:
        """Store Printing Settings."""

        def __init__(self, p_acc, jerk, vX, vY, vZ, vE, speed, units="SI (mm)"):
            """Initialize printing settings.

            Args:
                p_acc: (float) printing acceleration
                jerk: (float) jerk or similar
                vX: (float) max x velocity
                vY: (float) max y velocity
                vZ: (float) max z velocity
                vE: (float) max e velocity
                speed: (float) default target velocity
                units: (string, default = "SI (mm)") unit settings
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
                f"Settings:\n"
                f"    jerk: {self.jerk}\n"
                f"    acceleration: {self.p_acc}\n"
                f"    max_velocities: [X: {self.vX}, Y: {self.vY}, Z: {self.vZ}, E: {self.vE}]\n"
                f"    speed: {self.speed}\n"
                f"    units: {self.units}"
                f""
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
        """Define property line_number."""
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
        # Format the basic state info
        state_info = f"State(line: {self.line_number or 'N/A'})"

        # Add layer if available
        if self.layer is not None:
            state_info += f" [Layer: {self.layer}]"

        # Add pause status if set
        if self.pause:
            state_info += " [PAUSED]"

        # Build the complete representation
        result = f"{state_info}\n"

        # Add position information
        if self.state_position:
            result += f"\t{self.state_position}\n"
        else:
            result += "Position: Not set\n"

        # Add settings information with indentation
        if self.state_p_settings:
            settings_str = str(self.state_p_settings)
            # Indent each line of settings
            indented_settings = "\n".join(f"\t{line}" for line in settings_str.split("\n"))
            result += f"  {indented_settings}"
        else:
            result += "Settings: Not set"

        # Add comment if available
        if self.comment:
            result += f"Comment: {self.comment}"

        return result

    def __repr__(self) -> str:
        """Call __str__() for representation."""
        return self.__str__()
