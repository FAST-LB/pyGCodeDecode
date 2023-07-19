# -*- coding: utf-8 -*-
"""Test for state generator module."""
from pyGCodeDecode.state_generator import state_generator


def test_state_generator():
    """Test the state generator function."""
    from pyGCodeDecode.gcode_interpreter import setup

    test_setup = setup(
        filename=r"pyGCodeDecode\test\test_state_generator_setup.yaml", printer="test", layer_cue="LAYER_CHANGE"
    )
    states = state_generator(
        filename=r"pyGCodeDecode\test\test_state_generator.gcode", initial_machine_setup=test_setup.get_dict()
    )
    # print(states[0])
    # assert True
    assert isinstance(states, list)
    assert states[0].state_position.get_vec(withExtrusion=True) == [0, 0, 0, 0]
    assert states[1].state_position.get_vec(withExtrusion=True) == [10, 20, 30, 0]
    assert states[2].state_position.get_vec(withExtrusion=True) == [300, 200, 100, 0]
