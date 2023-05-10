from .state import state
import re
from typing import List, Match

commands = {
    "G0": {"E": None, "X": None, "Y": None, "Z": None, "F": None},  # non Extrusion Move
    "G1": {"E": None, "X": None, "Y": None, "Z": None, "F": None},  # Extrusion Move
    "M203": {"E": None, "X": None, "Y": None, "Z": None},  # Max Feedrate
    "M204": {"P": None, "R": None, "S": None, "T": None},  # Starting Acceleration
    "M205": {"E": None, "J": None, "S": None, "X": None, "Y": None, "Z": None},  # Advanced Settings
    "G4": {"P": None, "S": None},  # Dwell
    "M82": None,  # E Absolute
    "M83": None,  # E Relative
    "G20": None,  # Inches
    "G21": None,  # Milimeters
    "G90": None,  # Absolute Positioning
    "G91": None,  # Relative Positioning
    "G92": {"E": None, "X": None, "Y": None, "Z": None},  # Set Position
    "G10": {"S": None},
    "G11": None,
    ";": None,  # Comment
}

default_virtual_machine = {
    "absolute_position": True,
    "absolute_extrusion": True,
    "units": "mm",
    "initial_position": None,
    # general properties
    "nozzle_diam": 0.4,
    "filament_diam": 1.75,
    # default settings
    "p_vel": 35,
    "t_vel": 35,
    "p_acc": 1000,
    "jerk": 10,
    # axis max speeds
    "vX": 180,
    "vY": 180,
    "vZ": 30,
    "vE": 33,
}


def arg_extract(string: str, key_dict: dict):
    """
    Extract arguments from known command dictionarys.
    converts list of states to trajectory segments

    Parameters
    ----------
    string  :   str
        string of Commands
    key_dict : dict
        dictionary with known commands and subcommands

    Returns
    ----------
    dict
        dictionary with all found keys and their arguments

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
    )  # function to find next largest occurence in list, default to eol
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


def read_gcode_to_dict_list(filename):
    """
    read gcode from .gcode file

    Parameters
    ----------
    filename : string
        filename of the .gcode file: e.g. "print.gcode"

    Returns
    ----------
    list[dict]
        list with every line as dict
    """
    file_gcode = open(filename)
    dict_list = list()

    counter = 0
    for line in file_gcode:
        counter += 1
        line_dict = arg_extract(line, commands)
        line_dict["line_number"] = counter
        dict_list.append(line_dict)

    return dict_list


def dict_list_traveler(line_dict_list: List[dict], initial_machine_setup: dict = None):
    """
    Converts the line dictionary to a state.

    Parameters
    ----------
    line_dict_list  :  dict
        dict list with commands
    initial_machine_setup  :  dict
        dict with initial machine setup [absolute_position, absolute_extrusion, units, initial_position...]

    Returns
    ----------
    state
        incomplete state

    """

    def dict_extract(key: str, line_dict: dict):
        if key in line_dict:
            return line_dict[key]
        else:
            return None

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
    for key in default_virtual_machine:
        if initial_machine_setup is not None and key in initial_machine_setup:
            virtual_machine[key] = initial_machine_setup[key]
        else:
            virtual_machine[key] = default_virtual_machine[key]

    # GCode functionality:
    for line_dict in line_dict_list:
        # absolute / relative position mode
        if "G90" in line_dict:
            virtual_machine["absolute_position"] = True
        if "G91" in line_dict:
            virtual_machine["absolute_position"] = False

        # absolute / relative extrusionb mode
        if "M82" in line_dict:
            virtual_machine["absolute_extrusion"] = True
        if "M83" in line_dict:
            virtual_machine["absolute_extrusion"] = False

        # units
        if "G20" in line_dict:
            virtual_machine["units"] = "inch"
        if "G21" in line_dict:
            virtual_machine["units"] = "mm"

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
                if key in commands["G92"]:
                    virtual_machine["_" + key] = virtual_machine[key] + line_dict["G92"][key]
                    virtual_machine[key] = line_dict["G92"][key]

        # set acceleration
        if "M204" in line_dict and "P" in line_dict["M204"]:
            virtual_machine["p_acc"] = line_dict["M204"]["P"]

        # set max feedrate
        if "M203" in line_dict:
            for key in line_dict["M203"]:
                if key in commands["M203"]:
                    virtual_machine["v" + key] = line_dict["M203"][key]

        state_position = state.position(
            x=virtual_machine["X"] + virtual_machine["_X"],
            y=virtual_machine["Y"] + virtual_machine["_Y"],
            z=virtual_machine["Z"] + virtual_machine["_Z"],
            e=virtual_machine["E"] + virtual_machine["_E"],
        )

        p_settings = state.p_settings(
            speed=virtual_machine["p_vel"],
            p_acc=virtual_machine["p_acc"],
            jerk=virtual_machine["jerk"],
            Vx=virtual_machine["vX"],
            Vy=virtual_machine["vY"],
            Vz=virtual_machine["vZ"],
            Ve=virtual_machine["vE"],
            absMode=virtual_machine["absolute_extrusion"],
        )
        new_state = state(state_position=state_position, state_p_settings=p_settings)  # create new state

        # parse comment
        new_state.comment = dict_extract(";", line_dict=line_dict)
        new_state.line_nmbr = line_dict["line_number"]

        # populate state list
        if len(state_list) > 0:
            new_state.prev_state = state_list[-1]
            state_list[-1].next_state = new_state

        state_list.append(new_state)
    return state_list


def state_generator(filename: str, initial_machine_setup: dict = None):
    line_dict_list = read_gcode_to_dict_list(filename=filename)
    states = dict_list_traveler(line_dict_list=line_dict_list, initial_machine_setup=initial_machine_setup)

    return states


# old functions below


def array_to_state(old_state, array):
    """
    converts the GCODE line as array/list to a State

    Parameters
    ----------
    old_state   :   state
        used to keep old non changing values
    array       :   list
        GCODE line as generated by GCODE_line_dissector with
          G1          M203      M204      M205      T:M82/F:M83
         [[X,Y,Z,E,F],[X,Y,Z,E],[P,R,S,T],[X,Y,Z,E],[bool]]

    Returns
    ----------
    state
        state with updated values
    """
    G1_empty = True
    if not array[0] == [None]:
        G1_empty = False
        x = array[0][0]
        y = array[0][1]
        z = array[0][2]
        e = array[0][3]
        speed = array[0][4] / 60.0 if not array[0][4] is None else None  # convert mm/min to mm/s
    else:
        x = y = z = e = speed = None

    if not array[1] == [None]:
        Vx = array[1][0]
        Vy = array[1][1]
        Vz = array[1][2]
        Ve = array[1][3]
    else:
        Vx = Vy = Vz = Ve = None

    p_acc = array[2][0] if not array[2] == [None] else None
    jerk = array[3][0] if not array[3] == [None] else None

    abs_extruder = array[4][0]

    new_p_settings = state.p_settings.new(
        old_settings=old_state.state_p_settings,
        p_acc=p_acc,
        jerk=jerk,
        Vx=Vx,
        Vy=Vy,
        Vz=Vz,
        Ve=Ve,
        speed=speed,
        absMode=abs_extruder,
    )

    if new_p_settings.absMode:  # if abs mode, normal position call
        new_position = state.position.new(old_position=old_state.state_position, x=x, y=y, z=z, e=e)
    else:  # if rel mode use special call with absMode = False
        new_position = state.position.new(old_position=old_state.state_position, x=x, y=y, z=z, e=e, absMode=False)

    new_state = state.new(old_state=old_state, position=new_position, p_settings=new_p_settings)
    return new_state, G1_empty


def GCODE_line_dissector(line):
    """
    Dissects single Gcode lines into array following convention
    M203 for max axis speed
    M204,P for printing acceleration (R,S,T not yet supported)
    M205, axis Jerk, only use X value for calculation
    M82/M83, abs (M82) / rel (M83) extruder toggle

    Parameters
    ----------
    line : string
        single Gcode line

    Returns
    ----------
    float array
        array with   G1          M203      M204      M205      T:M82/F:M83
                    [[X,Y,Z,E,F],[X,Y,Z,E],[P,R,S,T],[X,Y,Z,E],bool]
    """

    def value_getter(line, all_params):
        line = line[: line.find(";")] if line.find(";") >= 0 else line  # remove comments
        all_params_return = []
        for i, param_group in enumerate(all_params):
            group_array = []
            if type(param_group[1]) is list:  # if keyword has parameters extract those
                if line.find(param_group[0]) != -1 or line.find("G0") != -1 and i == 0:  # get keyword group
                    for i, param in enumerate(param_group[1]):
                        if line.find(param) != -1:  # get parameters
                            posA = line.find(param) + len(param)
                            posE = line[posA:].find(" ") + posA
                            if posE > posA:
                                group_array.insert(i, float(line[posA:posE]))
                            else:
                                group_array.insert(i, float(line[posA:]))
                        else:
                            group_array.insert(i, None)
                else:
                    group_array.insert(i, None)
            else:  # if no parameters are given, toggle keyword
                if line.find(param_group[0]) == 0:  # first list element defines "True"
                    group_array.insert(0, True)
                elif line.find(param_group[1]) == 0:  # second list element defines "False"
                    group_array.insert(0, False)
                else:
                    group_array.insert(i, None)

            all_params_return.insert(i, group_array)
        return all_params_return

    G1_params = ["G1", ["X", "Y", "Z", "E", "F"]]  # G1   params convention
    M203_params = ["M203", ["X", "Y", "Z", "E"]]  # M203 params convention
    M204_params = ["M204", ["P", "R", "S", "T"]]  # M204 params convention
    M205_params = ["M205", ["X", "Y", "Z", "E"]]  # M205 params convention

    M8X_params = ["M82", "M83"]  # abs (M82) / rel (M83) toggle

    all_params = [G1_params] + [M203_params] + [M204_params] + [M205_params] + [M8X_params]
    output = value_getter(line, all_params)
    return output


def read_GCODE_from_file(filename, initial_p_settings: state.p_settings, initial_position):
    """
    read gcode from .gcode file and fill in a state vector

    Parameters
    ----------
    filename : string
        filename of the .gcode file: e.g. "print.gcode"
    initial_p_settings : state.settings
        default settings for printer
    initial_position :
                        None        -> start from zero
                        True        -> use first gcode G1 command as initial position
                        [x,y,z,e]   -> non zero coordinates for initial position
        initial position, where the simulation begins

    Returns
    ----------
    state object list
    """
    _remv_first_state = False

    # handle initial position
    if initial_position is True:
        _remv_first_state = True  # flag for removal later
        initial_position = state.position(0, 0, 0, 0)
        initial_state = state(state_position=initial_position, state_p_settings=initial_p_settings)
        initial_state.line_nmbr = -2

    elif initial_position is None:
        initial_position = state.position(0, 0, 0, 0)
        initial_state = state(state_position=initial_position, state_p_settings=initial_p_settings)
        initial_state.line_nmbr = 0

    elif type(initial_position) == list and len(initial_position) == 4:
        initial_position = state.position(
            x=initial_position[0], y=initial_position[1], z=initial_position[2], e=initial_position[3]
        )
        initial_state = state(state_position=initial_position, state_p_settings=initial_p_settings)
        initial_state.line_nmbr = -1
    else:
        raise ValueError("Invalid Initial Position")

    state_list = [initial_state]
    tmp_prev_state = initial_state
    file_gcode = open(filename)
    counter = 0
    for line in file_gcode:
        counter += 1

        newState, G1_empty = array_to_state(tmp_prev_state, GCODE_line_dissector(line=line))
        newState.line_nmbr = counter

        tmp_prev_state = newState
        # this is needed to store the previous states settings even if the state doesnt result in a pos change and is not appended to the state list.

        if (
            newState.state_position.is_travel(old_position=initial_state.state_position)
            or newState.state_position.is_extruding(old_position=initial_state.state_position)
            or (state_list[-1].line_nmbr == -2 and not G1_empty)
        ):
            state_list.append(newState)
            newState.prev_state = initial_state
            newState.prev_state.next_state = newState
            initial_state = newState

    if _remv_first_state:
        del state_list[0]
        state_list[0].prev_state = None

    return state_list
