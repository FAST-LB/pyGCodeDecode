# -*- coding: utf-8 -*-
"""Module for generating Abaqus .inp files for AMSIM."""

import pathlib

from . import gcode_interpreter as gi

"""
This script is to convert gcode into an event series as abaqus input

An example output looks like this:

time    x       y       z       extrusion bool -> 1 = extrusion moving to next step, 0 = no extrusion
0.0,    1.0,    0.0,    2.0,    1
0.44,   1.0,    22.0,   2.0,    0

time points generated are always at segment beginnings / endings, so interpolation linearly is the exact solution

"""


def generate_abaqus_event_series(
    simulation: gi.simulation,
    filepath: str = "pyGcodeDecode_abaqus_events.inp",
    tolerance: float = 1e-12,
    output_unit_system: str = None,
) -> tuple:
    """Generate abaqus event series.

    Args:
        simulation (gi.simulation): simulation instance
        filepath (string, default = "pyGcodeDecode_abaqus_events.inp"): output file path
        tolerance (float, default = 1e-12): tolerance to determine whether extrusion is happening
        output_unit_system (str, optional): Unit system for the output.
                The one from the simulation is used, in None is specified.

    Returns:
        tuple: the event series as a tuple for use in ABAQUS-Python
    """
    unpacked = gi.unpack_blocklist(simulation.blocklist)
    pos = [unpacked[0].pos_begin.get_vec(withExtrusion=True)]
    time = [0]
    for segment in unpacked:
        pos.append(segment.pos_end.get_vec(withExtrusion=True))
        time.append(segment.t_end)

    # figure out if extrusion happens from this to the next step, if yes -> 1, if no -> 0
    for id in range(len(pos) - 1):
        if pos[id + 1][3] - pos[id][3] > tolerance:
            pos[id][3] = 1
        else:
            pos[id][3] = 0
    pos[-1][3] = 0

    event_series_list = []

    # create directory if necessary
    pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    scaling = simulation.get_scaling_factor(output_unit_system=output_unit_system)

    # write to file
    with open(filepath, "w") as outfile:
        for time, pos in zip(time, pos):
            outfile.write(f"{time},{scaling*pos[0]},{scaling*pos[1]},{scaling*pos[2]},{pos[3]}\n")
            event_series_list.append((time, scaling * pos[0], scaling * pos[1], scaling * pos[2], pos[3]))

        print(f"ABAQUS event series written to: \n{outfile.name}")

    return tuple(event_series_list)
