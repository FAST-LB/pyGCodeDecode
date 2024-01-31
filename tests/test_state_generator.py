# -*- coding: utf-8 -*-
"""Test for state generator module."""
import pathlib

from pyGCodeDecode.state_generator import state_generator


def test_state_generator():
    """
    Test the state generator function.

    Functionality:
    - G0,G1
    - M82
    - M83
    - G90
    - G91
    - G92
    - G20
    - G21
    - comment
    - M203
    - M204
    - M205
    - G4
    To-Do:
        --> rest of supported commands + glitch/inject tests
    """
    from pyGCodeDecode.gcode_interpreter import setup

    test_setup = setup(
        presets_file=pathlib.Path("./tests/data/test_state_generator_setup.yaml"),
        printer="test",
        layer_cue="LAYER cue",
    )

    initial_pos = (5, 4, 3, 2)  # initial position definition
    test_setup.set_initial_position(initial_pos)

    states = state_generator(
        filepath=pathlib.Path("./tests/data/test_state_generator.gcode"),
        initial_machine_setup=test_setup.get_dict(),
    )

    assert isinstance(states, list)  # check if state list gets generated
    print(states)
    assert states[0].state_position.get_vec(withExtrusion=True) == list(initial_pos)  # test for inital position
    # assert states[1]  # set pos to abs
    assert states[3].state_position.get_vec(withExtrusion=True) == [10, 20, 30, initial_pos[-1]]  # test for second pos
    assert states[4].state_position.get_vec(withExtrusion=True) == [300, 200, 100, 50]  # test for another pos with extr
    assert states[5].state_position.get_vec(withExtrusion=True) == [-5, -5, 0, -0.2]  # test for pos with abs extr
    assert states[7].state_position.get_vec(withExtrusion=True) == [-5, -5, 0, 10]  # test for another pos with rel extr
    # assert states[8]  # set pos to rel
    assert states[9].state_position.get_vec(withExtrusion=True) == [5, -5, 0, 10]  # test for rel_move
    # assert states[10]  # set pos to abs
    # assert states[11]  # set E to abs
    assert states[12].state_position.get_vec(withExtrusion=True) == [7, 7, 7, 7]  # abs move
    # assert states[13]  # virtual null all axis
    assert states[14].state_position.get_vec(withExtrusion=True) == [14, 14, 14, 14]  # abs move with offset
    assert states[14].state_p_settings.units == "SImm"
    assert states[15].state_p_settings.units == "inch"
    assert states[16].state_p_settings.units == "SImm"
    assert states[16].layer == 0
    assert states[17].comment == "LAYER cue"
    assert states[17].layer == 1
    assert states[18].state_p_settings.vE == 50  # max extr vel (M203)
    assert states[18].state_p_settings.vX == 60  # max x vel
    assert states[18].state_p_settings.vY == 30  # max y vel
    assert states[18].state_p_settings.vZ == 15  # max z vel
    assert states[19].state_p_settings.p_acc == 1200  # printing acc(M204 P*)
    assert states[20].state_p_settings.jerk == 5  # jerk settings (M205 X*)
    assert states[21].pause == 0.5  # dwell (G4)
    assert states[22].pause == 5
