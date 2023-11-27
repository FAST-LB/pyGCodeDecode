# -*- coding: utf-8 -*-
"""Tools for pyGCD."""
from .gcode_interpreter import simulate


def print_layertimes(simulation: simulate, filename="layertimes.csv"):
    """Print out all layertimes to a file."""
    p_log = open(filename, "w")
    next_layer = 0
    current_layer = 0
    last_layer_time = 0
    travel = 0
    p_log.write("layer, layer time in s, travel distance in mm, avg speed in mm/s\n")

    for block in simulation.blocklist:
        next_layer = block.state_B.layer

        if next_layer > current_layer:
            block_begin = block.segments[0].t_begin
            duration = block_begin - last_layer_time
            p_log.write(
                # "Layertime layer "
                str(current_layer)
                + ", "
                + str(duration)
                + ", "
                + str(travel)
                + ", "
                + str((travel / duration) if duration > 0 else None)
                + "\n"
            )
            travel = 0
            last_layer_time = block_begin
            current_layer = next_layer

        if block.next_blck is None:
            block_end = block.segments[-1].t_end
            duration = block_end - last_layer_time

            p_log.write(
                # "Layertime layer "
                str(current_layer)
                + ", "
                + str(duration)
                + ", "
                + str(travel)
                + ", "
                + str((travel / duration) if duration > 0 else None)
                + "\n"
                # + "---end---"
            )
        travel += block.get_block_travel()

    p_log.close()
