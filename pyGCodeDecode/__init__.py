"""Generate time dependent boundary conditions from a .gcode file."""

from importlib import metadata

try:
    __version__ = metadata.version("pyGCodeDecode")
except Exception:
    __version__ = "unknown"
