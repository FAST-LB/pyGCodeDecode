# -*- coding: utf-8 -*-
"""Test for state generator module."""
from pyGCodeDecode.state_generator import state_generator


def test_state_generator():
    """Test the state generator function."""
    import os

    from pyGCodeDecode.gcode_interpreter import setup

    test_setup = setup(
        filename=os.path.abspath("pyGCodeDecode/test/test_state_generator_setup.yaml"),
        printer="test",
        layer_cue="LAYER_CHANGE",
    )

    initial_pos = (5, 4, 3, 2)  # initial position definition
    test_setup.set_initial_position(*initial_pos)

    states = state_generator(
        filename=os.path.abspath("pyGCodeDecode/test/test_state_generator.gcode"),
        initial_machine_setup=test_setup.get_dict(),
    )

    assert isinstance(states, list)  # check if state list gets generated

    assert states[0].state_position.get_vec(withExtrusion=True) == list(initial_pos)  # test for inital position
    assert states[1].state_position.get_vec(withExtrusion=True) == [10, 20, 30, initial_pos[-1]]  # test for second pos
    assert states[2].state_position.get_vec(withExtrusion=True) == [300, 200, 100, 50]  # test for another pos with extr
