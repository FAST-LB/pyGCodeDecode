# -*- coding: utf-8 -*-
"""Minimal example simulating the G-code of a brace from Aura-slicer on an Anisoprint Composer A4."""
import pathlib

from pyGCodeDecode.gcode_interpreter import simulation

if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent.resolve()

    # running the simulation by creating a simulation object using default machine parameters
    brace_simulation = simulation(
        gcode_path=pathlib.Path(script_dir) / "data" / "brace.gcode", machine_name="anisoprint_a4"
    )

    # create a 3D-plot
    brace_simulation.plot_3d(extrusion_only=True)
