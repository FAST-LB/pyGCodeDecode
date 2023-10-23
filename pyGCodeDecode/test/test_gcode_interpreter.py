# -*- coding: utf-8 -*-
"""Test for gcode interpreter."""


def test_setup():
    """Test for the simulation setup class."""
    import os

    from pyGCodeDecode.gcode_interpreter import setup

    simulation_setup = setup(
        filename=os.path.abspath("pyGCodeDecode/test/test_gcode_interpreter_setup_printers.yaml"),
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

    simulation_setup.set_initial_position(1, 2, 3, 4)
    sim_dict = simulation_setup.get_dict()
    assert sim_dict["X"] == 1
    assert sim_dict["Y"] == 2
    assert sim_dict["Z"] == 3
    assert sim_dict["E"] == 4

    # change printer afterwards
    simulation_setup.select_printer("prusa_mini")
    sim_dict = simulation_setup.get_dict()
    assert sim_dict["p_acc"] == 1250


test_setup()
