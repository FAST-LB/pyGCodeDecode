"""Test for gcode interpreter."""

import pathlib


def test_setup():
    """Test for the simulation setup class."""
    from pyGCodeDecode.gcode_interpreter import setup

    simulation_setup = setup(
        presets_file=pathlib.Path("./tests/data/test_printer_setups.yaml"),
        printer="debugging",
        layer_cue="LAYER CHANGE",
    )

    simulation_setup.set_property({"custom_property": 5})
    sim_dict = simulation_setup.get_dict()

    assert sim_dict["p_vel"] == 85
    assert sim_dict["p_acc"] == 100
    assert sim_dict["jerk"] == 8

    assert sim_dict["vX"] == 180
    assert sim_dict["vY"] == 170
    assert sim_dict["vZ"] == 12
    assert sim_dict["vE"] == 80

    assert sim_dict["nozzle_diam"] == 0.4
    assert sim_dict["filament_diam"] == 1.75

    assert sim_dict["custom_property"] == 5

    assert sim_dict["X"] == 0
    assert sim_dict["Y"] == 0
    assert sim_dict["Z"] == 0
    assert sim_dict["E"] == 0

    simulation_setup.set_initial_position((1, 2, 3, 4))
    sim_dict = simulation_setup.get_dict()
    assert sim_dict["X"] == 1
    assert sim_dict["Y"] == 2
    assert sim_dict["Z"] == 3
    assert sim_dict["E"] == 4


def test_setup_extended():
    """Test for the simulation setup class."""
    from pyGCodeDecode.gcode_interpreter import setup

    # test for specific printer is selected
    simulation_setup = setup(presets_file=pathlib.Path("./tests/data/test_printer_setups.yaml"), printer="test")
    assert simulation_setup.printer == "test"
    assert simulation_setup.firmware == "junction_deviation"

    # test for multiple printers in file and none has been selected -> error expected
    try:
        simulation_setup = setup(
            presets_file=pathlib.Path("./tests/data/test_printer_setups.yaml"),
        )
        assert False, "Expected ValueError was not raised."
    except ValueError as e:
        assert str(e) == "Multiple printers found but none has been selected."

    # test for single printer in file and none has been selected -> auto select
    simulation_setup = setup(
        presets_file=pathlib.Path("./tests/data/test_printer_setup_single.yaml"), verbosity_level=4
    )
    assert simulation_setup.printer == "debugging"

    # test for custom properties setting
    simulation_setup = setup(
        presets_file=pathlib.Path("./tests/data/test_printer_setup_single.yaml"),
        verbosity_level=4,
        extra_property=12,
    )
    assert simulation_setup.printer == "debugging"

    # test the accessors
    assert simulation_setup.extra_property == 12
    assert simulation_setup.get_dict()["extra_property"] == 12

    # test the setters
    simulation_setup.extra_property = 14
    simulation_setup.set_property({"special_property": 9})

    assert simulation_setup.extra_property == 14
    assert simulation_setup.get_dict()["extra_property"] == 14
    assert simulation_setup.get_dict()["special_property"] == 9
    assert simulation_setup.special_property == 9

    # test if printer settings are correctly loaded
    sim_dict = simulation_setup.get_dict()
    assert sim_dict["p_vel"] == 85
    assert sim_dict["p_acc"] == 100
    assert sim_dict["jerk"] == 8

    assert sim_dict["vX"] == 180
    assert sim_dict["vY"] == 170
    assert sim_dict["vZ"] == 12
    assert sim_dict["vE"] == 80

    assert sim_dict["nozzle_diam"] == 0.4
    assert sim_dict["filament_diam"] == 1.75

    assert sim_dict["X"] == 0
    assert sim_dict["Y"] == 0
    assert sim_dict["Z"] == 0
    assert sim_dict["E"] == 0

    simulation_setup.set_initial_position((1, 2, 3, 4))
    sim_dict = simulation_setup.get_dict()
    assert sim_dict["X"] == 1
    assert sim_dict["Y"] == 2
    assert sim_dict["Z"] == 3
    assert sim_dict["E"] == 4


def test_simulation_class():
    """Test for simulation class."""
    from pyGCodeDecode.gcode_interpreter import setup, simulation

    simulation_setup = setup(
        presets_file=pathlib.Path("./tests/data/test_printer_setups.yaml"),
        printer="debugging",
        layer_cue="LAYER CHANGE",
    )
    simulation_setup.set_property({"jerk": 0})
    simulation_setup.set_property({"p_acc": 50})

    simulation = simulation(
        gcode_path=pathlib.Path("./tests/data/test_gcode_interpreter.gcode"),
        initial_machine_setup=simulation_setup,
    )

    # from analytical calculation with given parameters
    t_100mm = 3.93333
    t_10mm = 0.89442
    t_02mm = 0.12649

    t_ges = t_100mm * 2 + t_10mm * 4 + t_02mm
    t_end_sim = simulation.blocklist[-1].get_segments()[-1].t_end
    assert abs(t_ges - t_end_sim) < 0.001
