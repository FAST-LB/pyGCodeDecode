"""Minimal example simulating the G-code of a brace from Aura-slicer on an Anisoprint Composer A4."""

import importlib.resources

from pyGCodeDecode.gcode_interpreter import simulation


def brace_example():
    """Minimal example for the usage of pyGCodeDecode simulating the G-code of a brace."""
    print(
        "Running pyGCD's brace example! 📎"
        "\nThis example illustrates the simplest use of the package: A gcode is simulated with default presets "
        "provided by the package. After the simulation, an interactive 3D-plot is shown. No output is saved."
    )

    gcode_path = importlib.resources.files("pyGCodeDecode").joinpath("examples/data/brace.gcode")

    # running the simulation by creating a simulation object using default machine parameters
    brace_simulation = simulation(gcode_path=gcode_path, machine_name="anisoprint_a4")

    # create a 3D-plot
    brace_simulation.plot_3d(extrusion_only=True)


if __name__ == "__main__":
    brace_example()
