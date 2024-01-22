# -*- coding: utf-8 -*-
"""Simulating the G-code of a 3DBenchy from PrusaSlicer on a Prusa MINI."""
import pathlib

from pyGCodeDecode.abaqus_file_generator import generate_abaqus_event_series
from pyGCodeDecode.gcode_interpreter import setup, simulation

if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent.resolve()

    # setting up the printer
    printer_setup = setup(
        presets_file=pathlib.Path(script_dir) / "data" / "printer_presets.yaml",
        printer="prusa_mini",
    )

    # set the start position of the extruder
    printer_setup.set_initial_position(initial_position={"X": 0.0, "Y": 0.0, "Z": 0.0, "E": 0.0})

    # running the simulation by creating a simulation object
    benchy_simulation = simulation(
        filename=pathlib.Path(script_dir) / "data" / "benchy.gcode",
        initial_machine_setup=printer_setup,
        output_unit_system="SImm",
    )

    # create an event series to use as input for an ABAQUS-simulation
    generate_abaqus_event_series(
        simulation=benchy_simulation,
        filepath=pathlib.Path(script_dir) / "output" / "benchy_prusa_mini_event_series.csv",
    )

    # create a 3D-plot
    benchy_simulation.plot_3d(extrusion_only=True)
