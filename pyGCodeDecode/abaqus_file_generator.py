# -*- coding: utf-8 -*-
"""Module for generating Abaqus .inp files for AMSIM."""
from pyGCodeDecode import gcode_interpreter as gi

"""
This script is to convert gcode into an event series as abaqus input

An example output looks like this:

time    x       y       z       extrusion bool -> 1 = extrusion moving to next step, 0 = no extrusion
0.0,    1.0,    0.0,    2.0,    1
0.44,   1.0,    22.0,   2.0,    0

timepoints generated are always at segment beginnings / endings, so interpolation linearly is the exact solution

"""
tolerance = float("1e-12")


def generate_abaqus_events(trajectory, output_filename="pyGcodeDecode_abaqus_events.inp"):
    """Generate abaqus event series."""
    # get all positions and timings
    unpacked = gi.unpack_blocklist(trajectory.blocklist)
    pos = [unpacked[0].pos_begin.get_vec(withExtrusion=True)]
    time = [0]
    for segm in unpacked:
        pos.append(segm.pos_end.get_vec(withExtrusion=True))
        time.append(segm.t_end)

    # figure out if extrusion happens from this to the next step, if yes -> 1, if no -> 0
    for id in range(len(pos) - 1):
        if pos[id + 1][3] - pos[id][3] > tolerance:
            pos[id][3] = 1
        else:
            pos[id][3] = 0
    pos[-1][3] = 0

    # writeout to file
    f = open(output_filename, "w")
    for time, pos in zip(time, pos):
        f.write(str(time) + "," + str(pos[0]) + "," + str(pos[1]) + "," + str(pos[2]) + "," + str(pos[3]) + "\n")
    f.close()
