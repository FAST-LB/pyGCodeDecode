# -*- coding: utf-8 -*-
"""Tools for pyGCD."""
import locale as loc
import pathlib
from typing import Union

from .gcode_interpreter import simulation


def save_layer_metrics(
    simulation: simulation,
    filepath: Union[pathlib.Path, str] = "./layer_metrics.csv",
    locale: str = None,
    delimiter: str = ";",
):
    """Print out print times, distance traveled and the average travel speed to a csv-file.

    Args:
        simulation: (simulation) simulation instance
        filepath: (Path | string, default = "./layer_metrics.csv") file name
        locale: (string, default = None) select locale settings, e.g. "en_us" "de_de", None = use system locale
        delimiter: (string, default = ";") select delimiter

    Layers are detected using the given layer cue.
    """
    if locale is None:
        loc.setlocale(loc.LC_ALL, "")
    else:
        loc.setlocale(loc.LC_ALL, locale)

    delimiter = delimiter + " "  # add space after delimiter

    # create directory if necessary
    pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    with open(file=filepath, mode="w") as p_log:
        p_log.write(f"layer{delimiter}layer time in s{delimiter}travel distance in mm{delimiter}avg speed in mm/s\n")

        next_layer = 0
        current_layer = 0
        last_layer_time = 0
        travel = 0
        for block in simulation.blocklist:
            next_layer = block.state_B.layer

            if next_layer > current_layer:
                block_begin = block.segments[0].t_begin
                duration = block_begin - last_layer_time
                p_log.write(
                    str(current_layer)
                    + delimiter
                    + loc.str(duration)
                    + delimiter
                    + loc.str(travel)
                    + delimiter
                    + (loc.str((travel / duration)) if duration != 0 else "NaN")
                    + "\n"
                )
                travel = 0
                last_layer_time = block_begin
                current_layer = next_layer

            if block.next_block is None:
                block_end = block.segments[-1].t_end
                duration = block_end - last_layer_time

                p_log.write(
                    str(current_layer)
                    + delimiter
                    + loc.str(duration)
                    + delimiter
                    + loc.str(travel)
                    + delimiter
                    + loc.str((travel / duration) if duration > 0 else "NaN")
                    + "\n"
                )
            travel += block.get_block_travel()

    print(f"Layer metrics written to:\n{str(filepath)}")
