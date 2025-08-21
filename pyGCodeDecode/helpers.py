"""Helper functions."""

import sys
from typing import Optional

# global flags
# check if program is running in ABAQUS-Python
if "ABQcaeK.exe" in sys.executable:
    FLAG_USING_ABAQUS = True
else:
    FLAG_USING_ABAQUS = False

# global verbosity level
VERBOSITY_LEVEL = 2  # default to INFO

# global progress bar state
_active_progress_bar = None


# Define verbosity levels for custom_print
# _levels = {
#     3: "[ DEBUG ]",
#     2: "[  INFO ]",
#     1: "[WARNING]",
# }

_levels = {
    3: "[DEBU]",
    2: "[INFO]",
    1: "[WARN]",
}


def set_verbosity_level(level: Optional[int]) -> None:
    """Set the global verbosity level."""
    global VERBOSITY_LEVEL
    if level is not None:
        VERBOSITY_LEVEL = level


def get_verbosity_level() -> int:
    """Get the current global verbosity level."""
    return VERBOSITY_LEVEL


def custom_print(*args, lvl=2, **kwargs) -> None:
    """Sanitize outputs for ABAQUS and print them if the log level is high enough. Takes all arguments for print.

    Args:
        *args: arguments to be printed
        lvl: verbosity level of the print (1 = WARNING, 2 = INFO, 3 = DEBUG)
        **kwargs: keyword arguments to be passed to print

    """
    # global _active_progress_bar

    sanitized_args = []
    if FLAG_USING_ABAQUS:
        # remove non-ascii characters like emojis as ABAQUS can't handle them
        for arg in args:
            sanitized_args.append(arg.encode("ascii", "ignore").decode())
    else:
        sanitized_args = args

    # print with verbosity level
    if lvl <= VERBOSITY_LEVEL:
        # If there's an active progress bar, clear the line first
        if _active_progress_bar is not None:
            # Clear the current line
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.flush()

        prefix = _levels.get(lvl, "")

        # Process arguments to handle newline alignment
        processed_args = []
        for arg in sanitized_args:
            if isinstance(arg, str) and "\n" in arg:
                # Split by newlines and add appropriate spacing after each newline
                lines = arg.split("\n")
                # Join with newline followed by spacing to align with prefix
                spacing = " " * len(prefix + " ")  # +1 for the space after prefix
                processed_arg = ("\n" + spacing).join(lines)
                processed_args.append(processed_arg)
            else:
                processed_args.append(arg)

        # Print the message
        if _active_progress_bar is not None:
            # When progress bar is active, print without extra newlines
            print(prefix, *processed_args, **kwargs)
            # Redraw the progress bar immediately
            _active_progress_bar._redraw_current_state()
        else:
            # Normal print when no progress bar is active
            print(prefix, *processed_args, **kwargs)


class ProgressBar:
    """A simple progress bar for the console."""

    def __init__(self, name: str = "Percent", barLength: int = 4, verbosity_level: int = 2):
        """Initialize a progress bar."""
        self.name = name
        self.barLength = barLength
        self.last_progress_update = -1
        self.last_text = ""  # Store the last progress bar text
        self.verbosity_level = verbosity_level

    def _redraw_current_state(self) -> None:
        """Redraw the current progress bar state."""
        if self.last_text and VERBOSITY_LEVEL >= 2:
            # Remove any existing \r from the stored text and add it fresh
            clean_text = self.last_text.lstrip("\r")
            sys.stdout.write("\r" + clean_text)
            sys.stdout.flush()

    def update(self, progress: float) -> None:
        """Display or update a console progress bar.

        Args:
            progress: float between 0 and 1 for percentage, < 0 represents a 'halt', > 1 represents 100%
        """
        global _active_progress_bar

        barLength = self.barLength
        status = ""

        if VERBOSITY_LEVEL >= self.verbosity_level:  # only print if verbosity level is high enough
            # Register this progress bar as active
            _active_progress_bar = self

            # check whether the input is valid
            if progress is int:
                progress = float(progress)
            if not isinstance(progress, float):
                progress = 0.0
                status = "error: progress var must be float\r\n"

            # progress outside [0, 1]
            if progress < 0.0:
                progress = 0.0
                status = "- Waiting \r\n"
            if progress >= 1.0:
                progress = 1.0
                status = "- Done ✅"

            progress_percent = round(progress * 100, ndigits=1)

            # check whether the progress has changed
            if self.last_progress_update != progress_percent or status != "":
                block = int(round(barLength * progress, ndigits=0))
                if progress < 1.0:
                    text = f"\r[{'#' * block + '-' * (barLength - block)}] {progress_percent} % of {self.name} {status}"
                else:
                    text = f"\r{_levels.get(self.verbosity_level, '')} ✅ Done with {self.name}"
                    # text = f"\r[{'#' * block + '-' * (barLength - block)}] ✅ Done with {self.name}"
                self.last_text = text
                sys.stdout.write(text)
                sys.stdout.flush()
                self.last_progress_update = progress_percent

                # If we're done, add a newline and unregister
                if progress >= 1.0:
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    self.last_text = ""
                    _active_progress_bar = None
