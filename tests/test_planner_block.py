# -*- coding: utf-8 -*-
"""Test for planner block module."""
import numpy as np

from pyGCodeDecode.planner_block import planner_block
from pyGCodeDecode.state import state
from pyGCodeDecode.utils import position, velocity


def test_planner_block():
    """
    Test method for the Planner Block module.

    Create single standalone blocks with no initial velocity.
    Test for the three cases: trapezoid, triangle and singular against known analytical solutions.
    To-Do:
        - self correction is not being tested.
        - advanced tests for Junction Deviation, currently only straight line JD is tested.
        - extrusion only not being tested
        - helper function
    """
    # initialize test parameters trapezoid
    dist = 10
    pos_0 = position(0, 0, 0, 0)
    pos_1 = position(dist, 0, 0, 0)
    settings = state.p_settings(p_acc=100, jerk=0, vX=100, vY=100, vZ=100, vE=100, speed=10, units="SImm")
    state_0 = state(state_position=pos_0, state_p_settings=settings)
    state_1 = state(state_position=pos_1, state_p_settings=settings)
    state_1.prev_state = state_0
    block_1 = planner_block(state=state_1, prev_block=None)

    # trapezoid block test
    assert block_1.blocktype == "trapezoid"
    assert block_1.valid is True
    assert block_1.get_segments()[0].get_position(t=0) == pos_0
    assert block_1.get_segments()[-1].get_position(t=block_1.get_segments()[-1].t_end) == pos_1

    t_end = block_1.get_segments()[-1].t_end
    assert t_end == (settings.speed * settings.speed + dist * settings.p_acc) / (
        settings.p_acc * settings.speed
    )  # analytical check for trapezoid move from and to standstill
    assert block_1.get_segments()[-1].get_position(t=t_end) == pos_1

    # initialize test parameters triangle
    dist = 30
    pos_0 = position(0, 0, 0, 0)
    pos_1 = position(dist, 0, 0, 0)
    settings = state.p_settings(p_acc=100, jerk=0, vX=100, vY=100, vZ=100, vE=100, speed=100, units="SImm")
    state_0 = state(state_position=pos_0, state_p_settings=settings)
    state_1 = state(state_position=pos_1, state_p_settings=settings)
    state_1.prev_state = state_0
    block_2 = planner_block(state=state_1, prev_block=None)

    # triangle block test
    assert block_2.blocktype == "triangle"
    assert block_2.valid is True
    assert block_2.get_segments()[0].get_position(t=0) == pos_0
    assert block_2.get_segments()[-1].get_position(t=block_2.get_segments()[-1].t_end) == pos_1
    assert np.isclose(block_2.get_segments()[0].t_end, np.sqrt(4 * dist * settings.p_acc) / (2 * settings.p_acc))
    assert np.isclose(
        block_2.get_segments()[0].vel_end.get_norm(), (settings.p_acc * block_2.get_segments()[0].t_end)
    )  # analytical check for peak vel

    # initialize test parameters single
    dist = 3
    pos_0 = position(0, 0, 0, 0)
    pos_1 = position(dist, 0, 0, 0)
    pos_2 = position(dist * 2, 0, 0, 0)

    settings = state.p_settings(p_acc=100, jerk=10, vX=100, vY=100, vZ=100, vE=100, speed=100, units="SImm")
    state_0 = state(state_position=pos_0, state_p_settings=settings)
    state_1 = state(state_position=pos_1, state_p_settings=settings)
    state_2 = state(state_position=pos_2, state_p_settings=settings)
    state_1.prev_state = state_0
    state_1.next_state = state_2  # needed next state to create singular PB with non zero ending vel
    block_3 = planner_block(state=state_1, prev_block=None, firmware="marlin_jd")

    # single block test
    assert block_3.blocktype == "single"
    assert block_3.valid is True
    assert block_3.get_segments()[0].get_position(t=0) == pos_0
    assert block_3.get_segments()[-1].get_position(t=block_3.get_segments()[-1].t_end) == pos_1
    assert np.isclose(block_3.get_segments()[0].t_end, np.sqrt(2 * dist * settings.p_acc) / (settings.p_acc))
    assert np.isclose(
        block_3.get_segments()[0].vel_end.get_norm(), (settings.p_acc * block_3.get_segments()[0].t_end)
    )  # analytical check for end vel

    # self correction test
    block_3.segments[0].pos_begin = position(30, 0, 0, 0)
    block_3.segments[0].pos_end = position(34.224744871391, 0, 0, 0)
    block_3.segments[0].vel_begin = velocity(10, 0, 0, 0)
    block_2.next_block = block_3
    block_2.self_correction()
    # check if interface velocity has been corrected
    assert block_2.segments[-1].vel_end.get_norm() == block_2.next_block.segments[0].vel_begin.get_norm()
