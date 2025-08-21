"""Test for the junction handling."""

import copy
import math
import os
import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pyGCodeDecode.gcode_interpreter import generate_planner_blocks
from pyGCodeDecode.junction_handling import (
    _get_handler_names,
    get_handler,
    junction_handling,
)
from pyGCodeDecode.state import state
from pyGCodeDecode.state_generator import generate_states
from pyGCodeDecode.utils import position


def _rotate_pos(pos: position, alpha):  # 2D Rotation
    alpha_r = math.radians(alpha)
    pos_v = np.array(pos.get_vec()[:2])
    rot_M = np.array([[math.cos(alpha_r), -math.sin(alpha_r)], [math.sin(alpha_r), math.cos(alpha_r)]])
    new_pos = np.matmul(rot_M, pos_v)
    return new_pos


def _rotate_state(state, alpha=45):
    pos = state.state_position
    new_pos = _rotate_pos(pos, alpha)
    state.state_position = position(new_pos[0], new_pos[1], pos.z, pos.e)

    return state


def _initialize_dummy_states(p_acc, jerk, speed):
    settings = state.p_settings(p_acc=p_acc, jerk=jerk, vX=100, vY=100, vZ=100, vE=100, speed=speed)
    stateA = state(state_p_settings=settings)
    stateB = state(state_p_settings=settings)
    stateC = state(state_p_settings=settings)

    stateA.next_state = stateB
    stateB.prev_state = stateA
    stateB.next_state = stateC
    stateC.prev_state = stateB
    return stateA, stateB, stateC


def test_junction_handlings():
    """Test for junction handling."""
    # Test cases for junction handling
    test_firmwares = _get_handler_names()
    test_firmwares.append("unknown")  # Add "unknown" for default handler
    print(f"Testing the following firmwares: {test_firmwares}", file=sys.stderr)

    angles = np.arange(0, 181, 1)
    results = {"turning angle": angles}
    for firmware in test_firmwares:
        handler = get_handler(firmware)
        assert handler is not None
        assert handler is not junction_handling if firmware != "unknown" else handler is junction_handling
        assert callable(handler)

        stateA, stateB, stateC = _initialize_dummy_states(p_acc=1000, jerk=10, speed=50)
        stateA.state_position = position(0, 0, 0, 0)
        stateB.state_position = position(50, 0, 0, 0)

        ang = 0
        stateA = _rotate_state(stateA, ang)
        stateB = _rotate_state(stateB, ang)

        firmware_results = []
        for angle in angles:
            coordXY = [math.cos(math.radians(angle)) * 50 + 50, math.sin(math.radians(angle)) * 50]
            stateC.state_position = position(*coordXY, 0, 0)
            stateC = _rotate_state(stateC, ang)

            result = handler(state_A=stateA, state_B=stateB).get_junction_vel()
            firmware_results.append(result)
        results[firmware] = firmware_results

    # Convert to DataFrame
    df = pd.DataFrame(results)

    fig, ax = plt.subplots(figsize=(6, 4))
    # Plotting with Pandas built-in functions
    df.plot(
        ax=ax,
        x="turning angle",
        y=test_firmwares,
    )

    ax.set_ylabel(r"cornering velocity in $\frac{\mathrm{mm}}{\mathrm{s}}$")
    ax.set_xlabel(r"turning angle in $\deg$")
    ax.set_xticks(range(0, 181, 30))
    ax.set_yticks(range(0, 51, 5))
    ax.grid(visible=True, which="major", axis="both", alpha=0.8, linestyle="dotted")

    fig.savefig("tests/output/junction_handlings.png", dpi=300, bbox_inches="tight")
    # plt.show()


def test_junction_handlings_rotating_COS():
    """Test for junction handling with coordinate system rotation."""
    test_firmwares = _get_handler_names()
    test_firmwares.append("unknown")  # Add "unknown" for default handler
    print(f"Testing the following firmwares: {test_firmwares}", file=sys.stderr)

    angles = np.arange(0, 181, 1)
    results = {"turning angle": angles}

    cos_rot_angles = np.arange(0, 360, 5)
    rotated_results = {"turning angle": angles}

    for firmware in test_firmwares:
        handler = get_handler(firmware)
        assert handler is not None
        assert handler is not junction_handling if firmware != "unknown" else handler is junction_handling
        assert callable(handler)

        stateA, stateB, stateC = _initialize_dummy_states(p_acc=1000, jerk=10, speed=50)
        stateA.state_position = position(0, 0, 0, 0)
        stateB.state_position = position(50, 0, 0, 0)

        ang = 0
        stateA = _rotate_state(stateA, ang)
        stateB = _rotate_state(stateB, ang)

        firmware_results = []
        rotated_firmware_results = []

        for angle in angles:
            coordXY = [math.cos(math.radians(angle)) * 50 + 50, math.sin(math.radians(angle)) * 50]
            stateC.state_position = position(*coordXY, 0, 0)
            stateC = _rotate_state(stateC, ang)

            # Unrotated
            result = handler(state_A=stateA, state_B=stateB).get_junction_vel()
            firmware_results.append(result)

            # Rotated: rotate all positions by rot_angle
            rotations = []
            for rot_angle in cos_rot_angles:
                # Deepcopy states to avoid mutation
                stateA_r = copy.deepcopy(stateA)
                stateB_r = copy.deepcopy(stateB)
                stateC_r = copy.deepcopy(stateC)
                stateA_r.next_state = stateB_r
                stateB_r.prev_state = stateA_r
                stateB_r.next_state = stateC_r
                stateC_r.prev_state = stateB_r
                stateA_r = _rotate_state(stateA_r, rot_angle)
                stateB_r = _rotate_state(stateB_r, rot_angle)
                stateC_r = _rotate_state(stateC_r, rot_angle)

                # Sanity check for angle between vectors
                vec1 = np.array(stateB_r.state_position.get_vec()[:2]) - np.array(stateA_r.state_position.get_vec()[:2])
                vec2 = np.array(stateC_r.state_position.get_vec()[:2]) - np.array(stateB_r.state_position.get_vec()[:2])
                dot_product = np.dot(vec1, vec2)
                norm1 = np.linalg.norm(vec1)
                norm2 = np.linalg.norm(vec2)
                cos_theta = dot_product / (norm1 * norm2)
                angle_between = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))
                if not np.isclose(angle_between, angle, atol=1e-2):
                    print(f"Angle between vectors: {angle_between:.2f} degrees, should be {angle:.2f} degrees")
                # Sanity check end

                result_rot = handler(state_A=stateA_r, state_B=stateB_r).get_junction_vel()
                rotations.append(result_rot)
            rotated_firmware_results.append((angle, rotations))

        results[firmware] = firmware_results
        rotated_results[firmware] = rotated_firmware_results

    # Convert to DataFrame
    df = pd.DataFrame(results)

    fig, ax = plt.subplots(figsize=(6, 4))
    color_map = {}
    # Plot solid lines for unrotated
    for idx, fw in enumerate(test_firmwares):
        line = ax.plot(
            angles,
            df[fw],
            label=fw,
            linewidth=2,
        )[0]
        color_map[fw] = line.get_color()

    # For each firmware, plot all rotated results as curves (one per rotation angle)
    for fw in test_firmwares:
        # rotated_results[fw] is a list of (angle, [results for each rotation])
        # transpose the data: for each rotation, collect the results for all angles
        all_rotations = list(zip(*[rot[1] for rot in rotated_results[fw]]))  # shape: (num_rotations, num_angles)
        for rot_curve in all_rotations:
            ax.plot(
                angles,
                rot_curve,
                color=color_map[fw],
                linewidth=1,
                alpha=0.075,
            )

    ax.set_ylabel(r"cornering velocity in $\frac{\mathrm{mm}}{\mathrm{s}}$")
    ax.set_xlabel(r"turning angle in $\deg$")
    ax.set_xticks(range(0, 181, 30))
    ax.set_yticks(range(0, 51, 5))
    ax.grid(visible=True, which="major", axis="both", alpha=0.8, linestyle="dotted")
    ax.legend()

    # Ensure output directory exists
    output_dir = "tests/output"
    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(os.path.join(output_dir, "junction_handlings_rotating_COS.png"), dpi=300, bbox_inches="tight")
    # plt.show()


def test_junction_handling_state_connect():
    """Test for the state connect method in the junction handling."""
    from pyGCodeDecode.gcode_interpreter import setup

    test_setup = setup(
        presets_file=pathlib.Path("./tests/data/test_printer_setups.yaml"),
        printer="prusa_mini",
        layer_cue="LAYER cue",
    )
    test_setup.set_property({"p_acc": 10})

    print(test_setup.firmware)
    states = generate_states(
        filepath=pathlib.Path("./tests/data/test_state_generator.gcode"),
        initial_machine_setup=test_setup.get_dict(),
    )

    blocks = generate_planner_blocks(states, firmware=test_setup.firmware)

    print(blocks)
    # TODO assert states are connected correctly


if __name__ == "__main__":
    test_junction_handlings()
    plt.show()
    test_junction_handlings_rotating_COS()
    plt.show()
