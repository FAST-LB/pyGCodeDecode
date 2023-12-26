# -*- coding: utf-8 -*-
"""Generate time dependent boundary conditions from a .gcode file."""

try:
    # Python 3.8+
    from importlib import metadata
except ImportError:
    # compatibility with older python versions
    try:
        import importlib_metadata as metadata
    except ImportError:
        __version__ = "unknown"

try:
    __version__ = metadata.version("pyGCodeDecode")
except Exception:
    __version__ = "unknown"
