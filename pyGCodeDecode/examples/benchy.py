"""Simulating the G-code of a 3DBenchy from PrusaSlicer on a Prusa MINI."""

import importlib.resources
import pathlib

from pyGCodeDecode.abaqus_file_generator import generate_abaqus_event_series
from pyGCodeDecode.gcode_interpreter import setup, simulation
from pyGCodeDecode.tools import save_layer_metrics


def benchy_example():
    """Extensive example for the usage of pyGCodeDecode simulating G-code for the famous 3DBenchy."""
    # setting the paths to the input and output directories
    data_dir = importlib.resources.files("pyGCodeDecode").joinpath("examples/data/")
    output_dir = pathlib.Path.cwd() / "output_benchy_example"

    print(
        "Running pyGCD's benchy example! 🛥️"
        "\nThis example illustrates an extensive use of the package: A gcode is simulated with default presets from a "
        "file provided alongside this example. After the simulation, an interactive 3D-plot is shown."
        "\nThe following files are saved to a new folder in your current directory: 💾\n",
        output_dir.__str__(),
        "\n   - a screenshot of the 3D-plot 📸"
        "\n   - a .vtk of the mesh 🕸️"
        "\n   - a summary of the simulation 📝"
        "\n   - some metrics for each layer 📊"
        "\n   - an event series to use with ABAQUS. 📄",
    )

    # setting up the printer
    printer_setup = setup(
        presets_file=data_dir / "printer_presets.yaml",
        printer="prusa_mini",
        layer_cue="LAYER_CHANGE",
    )

    # set the start position of the extruder
    printer_setup.set_initial_position(
        initial_position={"X": 0.0, "Y": 0.0, "Z": 0.0, "E": 0.0},
        input_unit_system="SImm",
    )

    # running the simulation by creating a simulation object
    benchy_simulation = simulation(
        gcode_path=data_dir / "benchy.gcode",
        initial_machine_setup=printer_setup,
        output_unit_system="SImm",
    )

    # save a short summary of the simulation
    benchy_simulation.save_summary(filepath=output_dir / "benchy_summary.yaml")

    # print a file containing some metrics for each layer
    save_layer_metrics(
        simulation=benchy_simulation,
        filepath=output_dir / "benchy_layer_metrics.csv",
        locale="en_US.utf8",
        delimiter=",",
    )

    # create an event series to use as input for an ABAQUS-simulation
    generate_abaqus_event_series(
        simulation=benchy_simulation,
        filepath=output_dir / "benchy_prusa_mini_event_series.csv",
        tolerance=1.0e-12,
        output_unit_system="SImm",
    )

    # create a 3D-plot and save a VTK as well as a screenshot
    benchy_mesh = benchy_simulation.plot_3d(
        extrusion_only=True,
        screenshot_path=output_dir / "benchy.png",
        vtk_path=output_dir / "benchy.vtk",
    )

    # create an interactive 3D-plot
    # the mesh from the previous run can be used to avoid generating a mesh again
    benchy_simulation.plot_3d(mesh=benchy_mesh)


if __name__ == "__main__":
    benchy_example()
