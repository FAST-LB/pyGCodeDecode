"""Module for generating Abaqus .inp files for AMSIM."""

from pathlib import Path

from pyGCodeDecode.helpers import custom_print

from . import gcode_interpreter

"""
This script is to convert gcode into an event series as abaqus input

An example output looks like this:

time    x       y       z       extrusion bool -> 1 = extrusion moving to next step, 0 = no extrusion
0.0,    1.0,    0.0,    2.0,    1
0.44,   1.0,    22.0,   2.0,    0

time points generated are always at segment beginnings / endings, so interpolation linearly is the exact solution

"""


def generate_abaqus_event_series(
    simulation: gcode_interpreter.simulation,
    filepath: str | Path = "pyGcodeDecode_abaqus_events.inp",
    tolerance: float = 1e-12,
    output_unit_system: str | None = None,
    return_tuple: bool = False,
) -> tuple:
    """Generate abaqus event series.

    Args:
        simulation (gcode_interpreter.simulation): simulation instance
        filepath (string, default = "pyGcodeDecode_abaqus_events.inp"): output file path
        tolerance (float, default = 1e-12): tolerance to determine whether extrusion is happening
        output_unit_system (str, optional): Unit system for the output.
                The one from the simulation is used, in None is specified.
        return_tuple (bool, default = False): return the event series as tuple.

    Returns:
        (optional) tuple: the event series as a tuple for use in ABAQUS-Python
    """
    # convert filepath if necessary
    if isinstance(filepath, str):
        filepath = Path(filepath)

    unpacked = gcode_interpreter.unpack_blocklist(simulation.blocklist)
    positions = [unpacked[0].pos_begin.get_vec(withExtrusion=True)]
    times = [0]
    for segment in unpacked:
        positions.append(segment.pos_end.get_vec(withExtrusion=True))
        times.append(segment.t_end)

    # figure out if extrusion happens from this to the next step, if yes -> 1, if no -> 0
    for number in range(len(positions) - 1):
        if positions[number + 1][3] - positions[number][3] > tolerance:
            positions[number][3] = 1
        else:
            positions[number][3] = 0
    positions[-1][3] = 0

    event_series_list = []

    # create directory if necessary
    filepath.parent.mkdir(parents=True, exist_ok=True)

    scaling = simulation.get_scaling_factor(output_unit_system=output_unit_system)

    # write to file
    round_to = 8
    with filepath.open("w") as outfile:
        for time, position in zip(times, positions, strict=True):
            outfile.write(
                f"{float(time)},{round(scaling * position[0], round_to)},{round(scaling * position[1], round_to)},"
                f"{round(scaling * position[2], round_to)},{position[3]}\n"
            )
            event_series_list.append((float(time), scaling * position[0], scaling * position[1], scaling * position[2], position[3]))

        custom_print(f"💾 ABAQUS event series written to 👉 {outfile.name}")

    if return_tuple:
        return tuple(event_series_list)
