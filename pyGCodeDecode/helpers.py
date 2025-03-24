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
    sanitized_args = []
    if FLAG_USING_ABAQUS:
        # remove non-ascii characters like emojis as ABAQUS can't handle them
        for arg in args:
            sanitized_args.append(arg.encode("ascii", "ignore").decode())
    else:
        sanitized_args = args

    # print with verbosity level
    if lvl <= VERBOSITY_LEVEL:
        levels = {3: "[DEBUG]:", 2: "[INFO]:", 1: "[WARNING]:"}
        prefix = levels.get(lvl, "")
        print(prefix, *sanitized_args, **kwargs)


class ProgressBar:
    """A simple progress bar for the console."""

    def __init__(self, name: str = "Percent", barLength: int = 10):
        """Initialize a progress bar."""
        self.name = name
        self.barLength = barLength
        self.last_progress_update = -1

    def update(self, progress: float) -> None:
        """Display or update a console progress bar.

        Args:
            progress: float between 0 and 1 for percentage, < 0 represents a 'halt', > 1 represents 100%
        """
        barLength = self.barLength
        status = ""

        if VERBOSITY_LEVEL >= 2:  # only print if verbosity level is high enough
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
                status = "- Done\r\n"

            progress_percent = round(progress * 100, ndigits=1)

            # check whether the progress has changed
            if self.last_progress_update != progress_percent or status != "":
                block = int(round(barLength * progress, ndigits=0))
                text = f"\r[{'#' * block + '-' * (barLength - block)}] {progress_percent} % of {self.name} {status}"
                sys.stdout.write(text)
                sys.stdout.flush()
                self.last_progress_update = progress_percent
