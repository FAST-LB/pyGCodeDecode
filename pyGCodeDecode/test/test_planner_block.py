# -*- coding: utf-8 -*-
"""Test for planner block module."""
from pyGCodeDecode.planner_block import planner_block
from pyGCodeDecode.state import state
from pyGCodeDecode.utils import position


def test_planner_block():
    """Test method for the Planner Block module."""
    # initialize test parameters
    pos_0 = position(0, 0, 0, 0)
    pos_1 = position(10, 0, 0, 0)
    settings = state.p_settings(p_acc=100, jerk=0, vX=100, vY=100, vZ=100, vE=100, speed=10, absMode=True, units="SImm")
    state_0 = state(state_position=pos_0, state_p_settings=settings)
    state_1 = state(state_position=pos_1, state_p_settings=settings)
    state_1.prev_state = state_0

    # trapez block test
    block_1 = planner_block(state=state_1, prev_blck=None)
    assert block_1.blcktype == "trapez"
    assert block_1.valid is True
    assert block_1.get_segments()[0].get_position(t=0) == pos_0
    t_end = block_1.get_segments()[-1].t_end
    assert t_end == (settings.speed * settings.speed + 10 * settings.p_acc) / (
        settings.p_acc * settings.speed
    )  # analytical check for trapez move from and to standstill
    assert block_1.get_segments()[-1].get_position(t=t_end) == pos_1
