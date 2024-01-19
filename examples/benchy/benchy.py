# -*- coding: utf-8 -*-
"""Simulating the print of a 3DBenchy on a Prusa MINI."""
import pathlib

from pyGCodeDecode.gcode_interpreter import setup, simulation

if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent.resolve()

    printer_setup = setup(
        filename=pathlib.Path(script_dir) / "data" / "printer_presets.yaml",
        printer="prusa_mini",
        layer_cue="LAYER_CHANGE",
    )

    simulation = simulation(
        filename=pathlib.Path(script_dir) / "data" / "Benchy.gcode",
        initial_machine_setup=printer_setup,
    )

    # creating a 3D-plot
    simulation.plot_3d(extrusion_only=True)
