"""Test the result calculation."""

import pathlib

import numpy as np

from pyGCodeDecode.planner_block import planner_block
from pyGCodeDecode.result import get_all_result_calculators, has_private_results
from pyGCodeDecode.state import state
from pyGCodeDecode.utils import position


def test_result_calc_within_pb():
    """Test the result calculation within a planner block."""
    statA = state(
        state_position=position(0, 0, 0, 0),
        state_p_settings=state.p_settings(
            p_acc=1.0,
            jerk=1.0,
            vX=10.0,
            vY=10.0,
            vZ=10.0,
            vE=10.0,
            speed=10.0,
        ),
    )
    statB = state(
        state_position=position(150, 0, 0, 0),
        state_p_settings=state.p_settings(
            p_acc=1.0,
            jerk=1.0,
            vX=10.0,
            vY=10.0,
            vZ=10.0,
            vE=10.0,
            speed=10.0,
        ),
    )
    statB.prev_state = statA
    pb = planner_block(statB, prev_block=None)

    if has_private_results():
        # Add private results to the planner block
        all_calcs = get_all_result_calculators()

        err = all_calcs
        print("errs: ", err)
        pb.calc_results(*err)

        errs = [calcs.name for calcs in pb.result_calculators]
        errs.extend(calculator.name for calculator in err if calculator.name not in errs)
        for calculator in err:
            if hasattr(calculator, "avgs"):
                for avg in calculator.avgs:
                    errs.append(calculator.name + avg)

        # Check if all results are calculated
        for segm in pb.segments:
            segm.self_check()
            for name in errs:
                print(f"Result {name}: {segm.result[name]}")
                assert isinstance(segm.result[name], (int, float, list)), f"Error {name} is not a number"

        # Check if the results are calculated correctly
        assert len(pb.segments) == 3, "There should be 3 segments in the planner block"

        segm = pb.segments[0]
        assert np.isclose(segm.result["acceleration"], 1.0)
        assert all(np.isclose(segm.result["velocity"], [0, 10.0]))
        assert np.isclose(segm.result["rel_vel_err_tavg"], 0.5)
        assert np.isclose(segm.result["rel_vel_err_savg"], 0.333333)

        segm = pb.segments[1]
        assert np.isclose(segm.result["rel_vel_err_tavg"], 0.0)
        assert np.isclose(segm.result["rel_vel_err_savg"], 0.0)

        segm = pb.segments[2]
        assert np.isclose(segm.result["acceleration"], -1.0)
        assert all(np.isclose(segm.result["velocity"], [10, 0]))
        assert np.isclose(segm.result["rel_vel_err_tavg"], 0.5)
        assert np.isclose(segm.result["rel_vel_err_savg"], 0.333333)


def test_result_calc_simulation():
    """Testing the result calculation in a simulation."""
    from pyGCodeDecode.gcode_interpreter import setup, simulation
    from pyGCodeDecode.result import get_all_result_calculators

    setup_test = setup(
        presets_file=pathlib.Path("./tests/data/test_printer_setups.yaml"),
        printer="prusa_mini",
    )

    sim = simulation(
        gcode_path=pathlib.Path("./tests/data/test_simplest.gcode"),
        # machine_name="prusa_mini",
        initial_machine_setup=setup_test,
    )

    result_calculators = get_all_result_calculators()

    for calculator in result_calculators:
        if hasattr(calculator, "avgs") and isinstance(calculator.avgs, (list, tuple)):
            for avg in calculator.avgs:
                print(f"Testing existence of average {avg} for {calculator.name}")
                assert (
                    calculator.name + avg in sim.results
                ), f"Result {calculator.name + avg} not found in simulation results"

    if has_private_results():
        print("Private results are available.")
        print("Whole simulation results:")
        for key, value in sim.results.items():
            print(f"  {key}: {value}")

        assert np.isclose(getattr(sim, "rel_vel_err_savg", None), 0.33333, atol=1e-5)
        assert np.isclose(getattr(sim, "rel_vel_err_tavg", None), 0.5, atol=1e-5)
