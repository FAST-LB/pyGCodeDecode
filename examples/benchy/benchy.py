# -*- coding: utf-8 -*-
"""Simulating the G-code of a 3DBenchy from PrusaSlicer on a Prusa MINI."""
import pathlib

from pyGCodeDecode.abaqus_file_generator import generate_abaqus_event_series
from pyGCodeDecode.gcode_interpreter import setup, simulation
from pyGCodeDecode.tools import print_layer_metrics

if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent.resolve()
    data_dir = script_dir / "data"
    output_dir = script_dir / "output"

    # setting up the printer
    printer_setup = setup(
        presets_file=data_dir / "printer_presets.yaml",
        printer="prusa_mini",
        layer_cue="LAYER_CHANGE",
    )

    # set the start position of the extruder
    printer_setup.set_initial_position(initial_position={"X": 0.0, "Y": 0.0, "Z": 0.0, "E": 0.0})

    # running the simulation by creating a simulation object
    benchy_simulation = simulation(
        gcode_path=data_dir / "benchy.gcode",
        initial_machine_setup=printer_setup,
        output_unit_system="SImm",
    )

    # save a short summary of the simulation
    benchy_simulation.save_summary(filepath=output_dir / "benchy_summary.yaml")

    # print a file containing some metrics for each layer
    print_layer_metrics(
        simulation=benchy_simulation,
        filepath=output_dir / "layer_metrics.csv",
        locale="en_us",
        delimiter=",",
    )

    # create an event series to use as input for an ABAQUS-simulation
    generate_abaqus_event_series(
        simulation=benchy_simulation,
        filepath=output_dir / "benchy_prusa_mini_event_series.csv",
    )

    # create a 3D-plot
    benchy_simulation.plot_3d(extrusion_only=True)
