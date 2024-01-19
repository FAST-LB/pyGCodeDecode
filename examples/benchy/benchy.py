# -*- coding: utf-8 -*-
"""Simulating the print of a 3DBenchy on a Prusa MINI."""
import pathlib

from pyGCodeDecode.abaqus_file_generator import generate_abaqus_event_series
from pyGCodeDecode.gcode_interpreter import setup, simulation

if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent.resolve()

    # setting up the printer
    printer_setup = setup(
        filename=pathlib.Path(script_dir) / "data" / "printer_presets.yaml",
        printer="prusa_mini",
        layer_cue="LAYER_CHANGE",
    )

    # running the simulation by creating a simulation object
    benchy_simulation = simulation(
        filename=pathlib.Path(script_dir) / "data" / "benchy.gcode",
        initial_machine_setup=printer_setup,
    )

    # create an event series to use as input for an ABAQUS-simulation
    generate_abaqus_event_series(
        simulation=benchy_simulation,
        filepath=pathlib.Path(script_dir) / "output" / "benchy_prusa_mini_event_series.csv",
    )

    # create a 3D-plot
    benchy_simulation.plot_3d(extrusion_only=True)
