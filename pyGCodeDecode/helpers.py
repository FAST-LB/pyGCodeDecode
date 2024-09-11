"""Helper functions."""

import sys

# global flags
# check if program is running in ABAQUS-Python
if "ABQcaeK.exe" in sys.executable:
    FLAG_USING_ABAQUS = True
else:
    FLAG_USING_ABAQUS = False


def custom_print(*args, **kwargs) -> None:
    """Sanitize outputs for ABAQUS and print them. Takes regular arguments for print."""
    sanitized_args = []
    if FLAG_USING_ABAQUS:
        # remove non-ascii characters like emojis as ABAQUS can't handle them
        for arg in args:
            sanitized_args.append(arg.encode("ascii", "ignore").decode())
    else:
        sanitized_args = args

    print(*sanitized_args, **kwargs)
