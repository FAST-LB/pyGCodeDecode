# -*- coding: utf-8 -*-
"""State generator module."""
import pathlib
import re
from typing import List, Match

from .state import state
from .utils import position

supported_commands = {
    "G0": {"E": None, "X": None, "Y": None, "Z": None, "F": None},  # non Extrusion Move
    "G1": {"E": None, "X": None, "Y": None, "Z": None, "F": None},  # Extrusion Move
    "M203": {"E": None, "X": None, "Y": None, "Z": None},  # Max Feedrate
    "M204": {"P": None, "R": None, "S": None, "T": None},  # Starting Acceleration
    "M205": {"E": None, "J": None, "S": None, "X": None, "Y": None, "Z": None},  # Advanced Settings
    "G4": {"P": None, "S": None},  # Dwell
    "M82": None,  # E Absolute
    "M83": None,  # E Relative
    "G20": None,  # Inches
    "G21": None,  # Millimeters
    "G90": None,  # Absolute Positioning
    "G91": None,  # Relative Positioning
    "G92": {"E": None, "X": None, "Y": None, "Z": None},  # Set Position
    ";": None,  # Comment
}

unsupported_commands = {
    "G2": {
        "E": None,
        "F": None,
        "I": None,
        "J": None,
        "P": None,
        "R": None,
        "S": None,
        "X": None,
        "Y": None,
    },  # clockwise arc move
    "G3": {
        "E": None,
        "F": None,
        "I": None,
        "J": None,
        "P": None,
        "R": None,
        "S": None,
        "X": None,
        "Y": None,
    },  # counter-clockwise arc move,
    "G10": {"S": None},  # read only
    "G11": None,  # read only
    "G28": {"L": None, "O": None, "R": None, "X": None, "Y": None, "Z": None},  # home all axes
    "G29": {
        "A": None,
        "B": None,
        "C": None,
        "D": None,
        "E": None,
        "F": None,
        "H": None,
        "I": None,
        "J": None,
        "K": None,
        "L": None,
        "P": None,
        "Q": None,
        "R": None,
        "S": None,
        "T": None,
        "U": None,
        "V": None,
        "W": None,
        "X": None,
        "Y": None,
    },  # bed leveling
}
known_commands = {**unsupported_commands, **supported_commands}

default_virtual_machine = {
    "absolute_position": True,
    "absolute_extrusion": True,
    "units": "SImm",
    "initial_position": None,
    # general properties
    "nozzle_diam": 0.4,
    "filament_diam": 1.75,
    # default settings
    "p_vel": 35,
    "t_vel": 35,
    "p_acc": 200,
    "jerk": 10,
    # axis max speeds
    "vX": 180,
    "vY": 180,
    "vZ": 30,
    "vE": 33,
    # axis positions
    "X": 0,
    "Y": 0,
    "Z": 0,
    "E": 0,
}


def arg_extract(string: str, key_dict: dict) -> dict:
    """
    Extract arguments from known command dictionaries.

    Args:
        string: (str) string of Commands
        key_dict: (dict) dictionary with known commands and subcommands

    Returns:
        dict: (dict) dictionary with all found keys and their arguments

    """
    arg_dict = dict()  # dict to store found arguments for each key
    matches: List[Match] = list()  # list to store matching keywords

    for key in key_dict.keys():  # look for each key in the dictionary
        match = re.search(key, string)  # regex search for key in string
        if match is not None:
            matches.append(match)  # append found matches

    # check for longest match and remove smaller match
    i = 0
    while i < len(matches):
        a: Match = matches[i]
        for match in matches:
            if a.start() == match.start() and a.end() < match.end():
                matches.remove(a)
        i += 1

    # support for multiple commands or additional comments per line
    match_start_list = [match.start() for match in matches]
    next_larger = lambda lst, num: min(  # noqa: E731
        filter(lambda x: x >= num, lst), default=len(string)
    )  # function to find next largest occurrence in list, default to eol
    comment_begin = min(
        [start.start() for start in list(filter(lambda x: x.group() == ";", [match for match in matches]))],
        default=len(string),
    )  # find first comment, default to eol

    for match in matches:  # iterate through all matches, with next match available
        match_end = match.end()  # find arg beginning by using end of match
        key = match.group()  # get key from match
        arg = None

        match_next_start = next_larger(match_start_list, match_end)  # find arg end by using beginning of next arg
        if key != ";":
            arg = string[match_end:match_next_start]  # slice string
            arg = arg.replace(" ", "")  # remove spaces if argument is not a comment
            arg = arg.replace("\n", "")  # remove \n if argument is not a comment

            try:
                arg = float(arg)  # casting to float if possible
            except ValueError:
                pass
        else:
            arg = string[match_end:]  # special case for comments where everything coming after match is arg

        if key_dict[key] is not None:  # check for nested commands
            arg = arg_extract(arg, key_dict[key])  # call arg_extract through recursion

        # save matches found outside of comments, not applying for comments
        if match.end() <= comment_begin or key == ";":
            arg_dict[key] = arg  # save argument values in dict

    return arg_dict


def read_gcode_to_dict_list(filepath: pathlib.Path) -> List[dict]:
    """
    Read gcode from .gcode file.

    Args:
        filename: (Path) filepath of the .gcode file

    Returns:
        dict_list: (list[dict]) list with every line as dict
    """
    print("Parsing the gcode...")
    dict_list = []

    with open(file=filepath, mode="r") as file_gcode:
        for i, line in enumerate(file_gcode):
            line_dict = arg_extract(string=line, key_dict=known_commands)
            line_dict["line_number"] = i + 1
            dict_list.append(line_dict)

    print(f"Parsing done. {len(dict_list)} lines parsed.")

    return dict_list


def dict_list_traveler(line_dict_list: List[dict], initial_machine_setup: dict) -> List[state]:
    """
    Convert the line dictionary to a state.

    Parameters:
        line_dict_list: (dict) dict list with commands
        initial_machine_setup: (dict) dict with initial machine setup [absolute_position, absolute_extrusion, units, initial_position...]

    Returns:
        state_list: (list[state]) all states in a list

    """
    state_list: List[state] = list()

    virtual_machine = {
        "X": 0,  # machine coordinates
        "Y": 0,
        "Z": 0,
        "E": 0,
        "_X": 0,  # offset through nulling
        "_Y": 0,
        "_Z": 0,
        "_E": 0,
    }  # keeping track of interstate values

    # optionally record layers
    if "layer_cue" in initial_machine_setup:
        layer_counter = 0

    # overwrite default values from initial machine setup
    """TODO: depending on the setting the user should be informed that a default value is used.
    I prepared a warning below.
    Are all these settings necessary?"""
    for key in default_virtual_machine:
        if initial_machine_setup is not None and key in initial_machine_setup:
            virtual_machine[key] = initial_machine_setup[key]
        else:
            """print(
                f"The parameter '{key}' was not specified in your machine presets. "
                f"Using the the default value of '{default_virtual_machine[key]}' to continue."
            )"""
            virtual_machine[key] = default_virtual_machine[key]

    # initial state creation
    state_position = position(
        virtual_machine["X"] + virtual_machine["_X"],
        virtual_machine["Y"] + virtual_machine["_Y"],
        virtual_machine["Z"] + virtual_machine["_Z"],
        virtual_machine["E"] + virtual_machine["_E"],
    )

    p_settings = state.p_settings(
        speed=virtual_machine["p_vel"],
        p_acc=virtual_machine["p_acc"],
        jerk=virtual_machine["jerk"],
        vX=virtual_machine["vX"],
        vY=virtual_machine["vY"],
        vZ=virtual_machine["vZ"],
        vE=virtual_machine["vE"],
    )
    new_state = state(state_position=state_position, state_p_settings=p_settings)  # create new state

    # add initial state comment
    new_state.comment = "Initial state created by pyGCD."
    new_state.line_number = None

    state_list.append(new_state)

    # GCode functionality:
    for line_dict in line_dict_list:
        # absolute / relative position mode
        if "G90" in line_dict:
            virtual_machine["absolute_position"] = True
        if "G91" in line_dict:
            virtual_machine["absolute_position"] = False

        # absolute / relative extrusion mode
        if "M82" in line_dict:
            virtual_machine["absolute_extrusion"] = True
        if "M83" in line_dict:
            virtual_machine["absolute_extrusion"] = False

        # units
        if "G20" in line_dict:
            virtual_machine["units"] = "inch"
        if "G21" in line_dict:
            virtual_machine["units"] = "SImm"

        # position & velocity
        pos_keys = ["X", "Y", "Z"]
        movement_commands = ["G0", "G1"]
        for command in movement_commands:  # treat G0 and G1 the same
            if command in line_dict:
                # look for xyz movement commands and apply abs/rel
                for key in pos_keys:
                    if key in line_dict[command]:
                        if virtual_machine["absolute_position"] is True:
                            virtual_machine[key] = line_dict[command][key]
                        elif virtual_machine["absolute_position"] is False:  # redundant
                            virtual_machine[key] = virtual_machine[key] + line_dict[command][key]

                # look for extrusion commands and apply abs/rel
                if "E" in line_dict[command]:
                    if virtual_machine["absolute_extrusion"] is True:
                        virtual_machine["E"] = line_dict[command]["E"]
                    if virtual_machine["absolute_extrusion"] is False:  # redundant
                        virtual_machine["E"] = virtual_machine["E"] + line_dict[command]["E"]
                if "F" in line_dict[command]:
                    virtual_machine["p_vel"] = line_dict[command]["F"] / 60

        # set position
        if "G92" in line_dict:
            for key in line_dict["G92"]:
                if key in known_commands["G92"]:
                    virtual_machine["_" + key] = (
                        virtual_machine[key] + line_dict["G92"][key] + virtual_machine["_" + key]
                    )
                    virtual_machine[key] = line_dict["G92"][key]

        # set acceleration
        if "M204" in line_dict and "P" in line_dict["M204"]:
            virtual_machine["p_acc"] = line_dict["M204"]["P"]

        # set max feedrate
        if "M203" in line_dict:
            for key in line_dict["M203"]:
                if key in known_commands["M203"]:
                    virtual_machine["v" + key] = line_dict["M203"][key]

        # set advanced settings
        if "M205" in line_dict and "X" in line_dict["M205"]:
            virtual_machine["jerk"] = line_dict["M205"]["X"]

        # dwell
        pause_duration = None
        if "G4" in line_dict:
            if "P" in line_dict["G4"]:
                pause_duration = line_dict["G4"]["P"] / 1000.0
            if "S" in line_dict["G4"]:
                pause_duration = line_dict["G4"]["S"]

        state_position = position(
            virtual_machine["X"] + virtual_machine["_X"],
            virtual_machine["Y"] + virtual_machine["_Y"],
            virtual_machine["Z"] + virtual_machine["_Z"],
            virtual_machine["E"] + virtual_machine["_E"],
        )

        p_settings = state.p_settings(
            speed=virtual_machine["p_vel"],
            p_acc=virtual_machine["p_acc"],
            jerk=virtual_machine["jerk"],
            vX=virtual_machine["vX"],
            vY=virtual_machine["vY"],
            vZ=virtual_machine["vZ"],
            vE=virtual_machine["vE"],
            units=virtual_machine["units"],
        )
        new_state = state(state_position=state_position, state_p_settings=p_settings)  # create new state

        # parse comment
        new_state.comment = line_dict[";"].strip() if ";" in line_dict else None

        # if layer cue is requested, count and add layers
        if "layer_cue" in initial_machine_setup:
            if new_state.comment is not None and initial_machine_setup["layer_cue"] == new_state.comment:
                layer_counter += 1
            new_state.layer = layer_counter

        new_state.line_number = line_dict["line_number"]

        # add pause time to state
        new_state.pause = pause_duration

        # populate state list
        if len(state_list) > 0:
            new_state.prev_state = state_list[-1]
            state_list[-1].next_state = new_state

        state_list.append(new_state)
    return state_list


def check_for_unsupported_commands(line_dict_list: dict) -> dict:
    """Search for unsupported commands used in the G-code, warn the user and return the occurrences.

    Args:
        line_dict_list (dict): list of dicts containing all commands appearing

    Returns:
        dict: a dict containing the appearing unsupported commands and how often they appear.
    """
    # search for unsupported commands
    print("Searching for known but unsupported G-code commands...")
    unsupported_commands_found = []
    for line_dict in line_dict_list:
        for key in line_dict.keys():
            if key in unsupported_commands.keys():
                unsupported_commands_found.append(key)

    unsupported_command_counts = {
        command: unsupported_commands_found.count(command) for command in unsupported_commands_found
    }

    if unsupported_commands_found != []:
        print(f"⚠️ Warning: {len(unsupported_command_counts.keys())} known but unsupported command(s) found:")
        for key, value in unsupported_command_counts.items():
            print(f" - Command '{key}' found {value} time(s).")
    else:
        print("Great, the G-code does not contain any unsupported commands known to pyGCD 🎈.")

    return unsupported_command_counts


def state_generator(filepath: pathlib.Path, initial_machine_setup: dict) -> List[state]:
    """Generate state list from GCode file.

    Args:
        filepath: (Path) filepath to GCode
        initial_machine_setup: (dict) dictionary with machine setup

    Returns:
        states: (list[states]) all states in a list
    """
    line_dict_list = read_gcode_to_dict_list(filepath=filepath)
    check_for_unsupported_commands(line_dict_list=line_dict_list)
    states = dict_list_traveler(line_dict_list=line_dict_list, initial_machine_setup=initial_machine_setup)

    return states
