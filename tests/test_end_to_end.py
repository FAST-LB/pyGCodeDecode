"""End to end test for the package."""

import pathlib


def test_end_to_end_compact():
    """Testing the simulation functionality with automatic setup, similarly to the brace example."""
    from pyGCodeDecode.gcode_interpreter import simulation

    simulation(
        gcode_path=pathlib.Path("./tests/data/test_state_generator.gcode"),
        machine_name="anisoprint_a4",
    )


def test_end_to_end_extensive():
    """Testing the simulation functionality as well as the various outputs, similarly to the benchy example."""
    from pyGCodeDecode.abaqus_file_generator import generate_abaqus_event_series
    from pyGCodeDecode.gcode_interpreter import setup, simulation
    from pyGCodeDecode.tools import save_layer_metrics

    data_dir = pathlib.Path("./tests/data/")
    output_dir = pathlib.Path("./tests/output/end_to_end_extensive")

    # setting up the printer
    printer_setup = setup(
        presets_file=data_dir / "test_printer_setups.yaml",
        printer="test",
        layer_cue="LAYER_CHANGE",
    )

    # set the start position of the extruder
    printer_setup.set_initial_position(
        initial_position={"X": 0.0, "Y": 0.0, "Z": 0.0, "E": 0.0},
        input_unit_system="SImm",
    )

    # running the simulation by creating a simulation object
    end_to_end_simulation = simulation(
        gcode_path=data_dir / "test_state_generator.gcode",
        initial_machine_setup=printer_setup,
        output_unit_system="SImm",
    )

    # save a short summary of the simulation
    end_to_end_simulation.save_summary(filepath=output_dir / "test_end_to_end_summary.yaml")

    # print a file containing some metrics for each layer
    save_layer_metrics(
        simulation=end_to_end_simulation,
        filepath=output_dir / "layer_metrics.csv",
        locale="en_US.utf8",
        delimiter=",",
    )

    # create an event series to use as input for an ABAQUS-simulation
    generate_abaqus_event_series(
        simulation=end_to_end_simulation,
        filepath=output_dir / "test_end_to_end_event_series.csv",
        tolerance=1.0e-12,
        output_unit_system="SImm",
    )

    # create a 3D-plot and save a VTK as well as a screenshot
    end_to_end_simulation.plot_3d(
        extrusion_only=True,
        screenshot_path=output_dir / "test_end_to_end.png",
        vtk_path=output_dir / "test_end_to_end.vtk",
    )

    output_files = [
        "layer_metrics.csv",
        "test_end_to_end_event_series.csv",
        "test_end_to_end_summary.yaml",
        "test_end_to_end.png",
        "test_end_to_end.vtk",
    ]
    for file in output_files:
        assert (output_dir / file).exists()
