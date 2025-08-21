"""End to end test for the package."""

import pathlib

import numpy as np

from pyGCodeDecode.plotter import plot_vel


def test_end_to_end_compact():
    """Testing the simulation functionality with automatic setup, similarly to the brace example."""
    from pyGCodeDecode.gcode_interpreter import simulation

    simulation(
        gcode_path=pathlib.Path("./tests/data/test_state_generator.gcode"),
        machine_name="anisoprint_a4",
    )


def test_end_to_end_volumetr():
    """Testing the simulation functionality with automatic setup, using volumetric or distance based extrusion."""
    from pyGCodeDecode.gcode_interpreter import setup, simulation

    preset = setup(pathlib.Path("./tests/data/test_printer_setups.yaml"), "test")
    preset.set_property({"volumetric_extrusion": False})

    sim = simulation(
        gcode_path=pathlib.Path("./tests/data/test_state_generator.gcode"),
        initial_machine_setup=preset,
    )

    end_extrusion = sim.blocklist[-1].segments[-1].pos_end.e
    expected_extrusion = 14.0
    assert np.isclose(
        end_extrusion, expected_extrusion, rtol=1e-4
    ), f"Expected {expected_extrusion}, but got {end_extrusion}"
    preset = setup(pathlib.Path("./tests/data/test_printer_setups.yaml"), "test")
    preset.set_property({"volumetric_extrusion": True})

    sim = simulation(
        gcode_path=pathlib.Path("./tests/data/test_state_generator.gcode"),
        initial_machine_setup=preset,
    )

    end_extrusion = sim.blocklist[-1].segments[-1].pos_end.e
    expected_extrusion = 14.0 / ((1.75 / 2) ** 2 * np.pi)

    assert np.isclose(
        end_extrusion, expected_extrusion, rtol=1e-4
    ), f"Expected {expected_extrusion}, but got {end_extrusion}"


def test_end_to_end_extensive():
    """Testing the simulation functionality as well as the various outputs, similarly to the benchy example."""
    from pyGCodeDecode.abaqus_file_generator import generate_abaqus_event_series
    from pyGCodeDecode.gcode_interpreter import setup, simulation
    from pyGCodeDecode.plotter import plot_2d, plot_3d
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
        input_unit_system="SI (mm)",
    )

    # running the simulation by creating a simulation object
    end_to_end_simulation = simulation(
        gcode_path=data_dir / "test_state_generator.gcode",
        initial_machine_setup=printer_setup,
        output_unit_system="SI (mm)",
        verbosity_level=3,
    )

    # save a short summary of the simulation
    end_to_end_simulation.save_summary(filepath=output_dir / "test_end_to_end_summary.yaml")

    # print a file containing some metrics for each layer
    save_layer_metrics(
        simulation=end_to_end_simulation,
        filepath=output_dir / "layer_metrics.csv",
        delimiter=",",
    )

    # create an event series to use as input for an ABAQUS-simulation
    generate_abaqus_event_series(
        simulation=end_to_end_simulation,
        filepath=output_dir / "test_end_to_end_event_series.csv",
        tolerance=1.0e-12,
        output_unit_system="SI (mm)",
    )

    # create a 3D-plot
    plot_3d(
        sim=end_to_end_simulation,
        screenshot_path=output_dir / "test_end_to_end_3d.png",
        vtk_path=output_dir / "test_end_to_end.vtk",
        camera_settings={"camera_position": "xy"},
    )

    # 3D-plot with matplotlib
    plot_3d(
        sim=end_to_end_simulation,
        screenshot_path=output_dir / "test_end_to_end_3d_mpl.png",
        vtk_path=output_dir / "test_end_to_end.vtk",
        camera_settings={"camera_position": "xy"},
        mpl_subplot=True,
    )

    # create a 2D-plot with matplotlib
    plot_2d(
        sim=end_to_end_simulation,
        show=False,
        filepath=output_dir / "test_end_to_end_2d.png",
    )
    # end_to_end_simulation.plot_2d_position(filepath=output_dir / "test_end_to_end_2d.png", show=False)

    # plotting velocities with matplotlib
    plot_vel(
        sim=end_to_end_simulation,
        show=False,
        filepath=output_dir / "velocities.png",
    )

    # assert that the output files exists (pyvista screenshot cannot be created without a display)
    output_files = [
        "layer_metrics.csv",
        "test_end_to_end_event_series.csv",
        "test_end_to_end_summary.yaml",
        "test_end_to_end_2d.png",
        "test_end_to_end.vtk",
        "velocities.png",
    ]
    for file in output_files:
        assert (output_dir / file).exists()
