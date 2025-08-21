"""GCode Interpreter Module."""

import importlib.resources
import time
from pathlib import Path
from typing import List, Optional, Tuple, Union

import numpy as np
import yaml

from pyGCodeDecode.helpers import ProgressBar, custom_print, set_verbosity_level

from .planner_block import planner_block
from .result import get_all_result_calculators
from .state import state
from .state_generator import generate_states
from .utils import segment, velocity


def generate_planner_blocks(states: List[state], firmware=None):
    """Convert list of states to trajectory repr. by planner blocks.

    Args:
        states: (list[state]) list of states
        firmware: (string, default = None) select firmware by name

    Returns:
        block_list (list[planner_block]) list of all planner blocks to complete travel between all states
    """
    block_list = []
    bar = ProgressBar(name="Planner Blocks")

    colordict = {"infill": "blue", "perimeter": "green"}
    last_type = None

    for i, this_state in enumerate(states):
        prev_block = block_list[-1] if len(block_list) > 0 else None  # grab prev block from block_list
        new_block = planner_block(state=this_state, prev_block=prev_block, firmware=firmware)  # generate new block

        if this_state.comment is not None:
            for key in colordict.keys():
                if key in this_state.comment.lower():
                    last_type = key

        new_block.e_type = last_type

        if len(new_block.get_segments()) > 0:
            if new_block.prev_block is not None:
                new_block.prev_block.next_block = new_block  # update nb list
            block_list.append(new_block)
        bar.update((i + 1) / len(states))
    return block_list


def find_current_segment(path: List[segment], t: float, last_index: int = None, keep_position: bool = False):
    """Find the current segment.

    Args:
        path: (list[segment]) all segments to be searched
        t: (float) time of search
        last_index: (int) last found index for optimizing search
        keep_position: (bool) keeps position of last segment, use this when working with
            gaps of no movement between segments

    Returns:
        segment: (segment) the segment which defines movement at that point in time
        last_index: (int) last index where something was found, search speed optimization possible
    """
    if keep_position:
        # use this if eval for times where no planner blocks are created
        if last_index is None or len(path) - 1 < last_index or path[last_index].t_begin > t:
            # unoptimized search, still returns index
            for last_index, segm in enumerate(path):
                if t >= segm.t_begin and t < segm.t_end:
                    return segm, last_index
                elif t >= segm.t_end and t < path[last_index + 1].t_begin:
                    # if no segment exists, create one that interpolates the previous segment as static
                    interpolated_segment = segment(
                        t_begin=segm.t_end,
                        t_end=path[last_index + 1].t_begin,
                        pos_begin=segm.pos_end,
                        pos_end=segm.pos_end,
                        vel_begin=velocity(0, 0, 0, 0),
                        vel_end=velocity(0, 0, 0, 0),
                    )
                    return interpolated_segment, last_index
        else:
            # optimized search
            for id, segm in enumerate(path[last_index:]):
                if t >= segm.t_begin and t <= segm.t_end:
                    return segm, last_index + id
                elif t >= segm.t_end and t < path[last_index + 1].t_begin:
                    # if no segment exists, create one that interpolates the previous segment as static
                    interpolated_segment = segment(
                        t_begin=segm.t_end,
                        t_end=path[last_index + 1].t_begin,
                        pos_begin=segm.pos_end,
                        pos_end=segm.pos_end,
                        vel_begin=velocity(0, 0, 0, 0),
                        vel_end=velocity(0, 0, 0, 0),
                    )
                    return interpolated_segment, last_index
    else:
        # original function untouched
        # some robustness checks
        if path[-1].t_end < t:
            custom_print("No movement at this time in Path!", lvl=1)
            return None, None
        elif last_index is None or len(path) - 1 < last_index or path[last_index].t_begin > t:
            custom_print(f"unoptimized Search, last index: {last_index}", lvl=3)
            for last_index, segm in enumerate(path):
                if t >= segm.t_begin and t < segm.t_end:
                    return segm, last_index
        else:
            for id, segm in enumerate(path[last_index:]):
                if t >= segm.t_begin and t <= segm.t_end:
                    return segm, last_index + id
            raise ValueError("nothing found")


def unpack_blocklist(blocklist: List[planner_block]) -> List[segment]:
    """Return list of segments by unpacking list of planner blocks.

    Args:
        blocklist: (list[planner_block]) list of planner blocks

    Returns:
        path: (list[segment]) list of all segments
    """
    path = []
    for block in blocklist:
        path.extend(block.get_segments()[:])
    return path


class simulation:
    """Simulation of .gcode with given machine parameters."""

    def __init__(
        self,
        gcode_path: Path,
        machine_name: str = None,
        initial_machine_setup: "setup" = None,
        output_unit_system: str = "SI (mm)",
        verbosity_level: Optional[int] = None,
    ):
        """Initialize the Simulation of a given G-code with initial machine setup or default machine.

        - Generate all states from GCode.
        - Connect states with planner blocks, consisting of segments
        - Self correct inconsistencies.

        Args:
            gcode_path: (Path) path to GCode
            machine_name: (string, default = None) name of the default machine to use
            initial_machine_setup: (setup, default = None) setup instance
            output_unit_system: (string, default = "SI (mm)") available unit systems: SI, SI (mm) & inch
            verbosity_level: (int, default = None) set verbosity level (0: no output, 1: warnings, 2: info, 3: debug)

        Example:
        ```python
        gcode_interpreter.simulation(gcode_path=r"path/to/part.gcode", initial_machine_setup=printer_setup)
        ```
        """
        simulation_start_time = time.time()
        self._last_index = None  # used to optimize search in segment list
        self.filename = Path(gcode_path)
        self.firmware = None
        set_verbosity_level(verbosity_level)

        # set output unit system
        self.available_unit_systems = {"SI": 1e-3, "SI (mm)": 1.0, "inch": 1 / 25.4}
        if output_unit_system in self.available_unit_systems:
            self.output_unit_system = output_unit_system
        else:
            raise ValueError("Chosen unit system is unavailable!")

        # create a printer setup with default values if none was specified
        if initial_machine_setup is not None:
            if machine_name is not None and initial_machine_setup.get_dict()["printer"] != machine_name:
                raise ValueError("Both a printer name and a printer setup were specified, but they do not match!")
            else:
                pass
        else:
            if machine_name is None:
                raise ValueError("Neither a printer name nor a printer setup was specified. At least one is required!")
            else:
                custom_print(
                    "Only a machine name was specified but no full setup. "
                    "Trying to create a setup from pyGCD's default values...",
                    lvl=1,
                )
                default_presets_file = importlib.resources.files("pyGCodeDecode").joinpath(
                    "data/default_printer_presets.yaml"
                )
                initial_machine_setup = setup(
                    presets_file=default_presets_file,
                    printer=machine_name,
                )

        # SET INITIAL SETTINGS
        self.initial_machine_setup_dict = initial_machine_setup.check_initial_setup()
        self.firmware = self.initial_machine_setup_dict["firmware"]

        self.states: List[state] = generate_states(
            filepath=self.filename, initial_machine_setup=self.initial_machine_setup_dict
        )

        custom_print(
            f"Simulating {self.filename} with {self.initial_machine_setup_dict['printer']} using "
            f"the {self.firmware} firmware."
        )
        self.blocklist: List[planner_block] = generate_planner_blocks(states=self.states, firmware=self.firmware)
        self.trajectory_self_correct()

        # calculate results
        self.results = {}
        self.calc_results()
        self.calculate_averages()

        self.print_summary(start_time=simulation_start_time)

    def __getattr__(self, name):
        """Get result by name."""
        if name in self.results:
            return self.results[name]

    def trajectory_self_correct(self):
        """Self correct all blocks in the blocklist with self_correction() method."""
        n_max = len(self.blocklist)
        bar = ProgressBar(name="Block Correction")

        for n, block in enumerate(self.blocklist):
            progress = round(n / n_max, ndigits=3)
            if progress > bar.last_progress_update:
                bar.update((n + 1) / len(self.blocklist))
                bar.last_progress_update = progress

            block.self_correction()
        bar.update(1.0)

    def calc_results(self):
        """Calculate the results."""
        calculators = get_all_result_calculators()

        for pb in self.blocklist:
            pb.calc_results(*calculators)

    def calculate_averages(self):
        """Calculate averages for averageable results."""

        def spatial_average(calculator):
            total_dist = 0
            glob_result = 0
            for segm in unpack_blocklist(self.blocklist):
                len = segm.get_segm_len()
                segm_result = segm.get_result(calculator.name + "_savg")
                if segm.is_extruding():
                    total_dist += len
                    glob_result += segm_result * len
            if total_dist > 0:
                return glob_result / total_dist

        def time_average(calculator):
            total_time = 0
            glob_result = 0
            for segm in unpack_blocklist(self.blocklist):
                duration = segm.get_segm_duration()
                segm_result = segm.get_result(calculator.name + "_tavg")
                if segm.is_extruding():
                    total_time += duration
                    glob_result += segm_result * duration
            if total_time > 0:
                return glob_result / total_time

        calculators = get_all_result_calculators()
        for calculator in calculators:
            if hasattr(calculator, "avgs") and isinstance(calculator.avgs, (list, tuple)):
                for avg in calculator.avgs:
                    if avg == "_savg":
                        self.results[calculator.name + "_savg"] = spatial_average(calculator)
                    elif avg == "_tavg":
                        self.results[calculator.name + "_tavg"] = time_average(calculator)
                    else:
                        raise ValueError(f"Unknown average type: {avg} for {calculator.name}")

    def get_values(self, t: float, output_unit_system: str = None) -> Tuple[List[float]]:
        """Return unit system scaled values for vel and pos.

        Args:
            t: (float) time
            output_unit_system (str, optional): Unit system for the output.
                The one from the simulation is used, in None is specified.

        Returns:
            list: [vel_x, vel_y, vel_z, vel_e] velocity
            list: [pos_x, pos_y, pos_z, pos_e] position
        """
        segments = unpack_blocklist(blocklist=self.blocklist)
        segm, self._last_index = find_current_segment(path=segments, t=t, last_index=self._last_index)
        tmp_vel = segm.get_velocity(t=t).get_vec(withExtrusion=True)
        tmp_pos = segm.get_position(t=t).get_vec(withExtrusion=True)

        scaling = self.get_scaling_factor(output_unit_system=output_unit_system)

        # scale to required unit system
        tmp_vel = [scaling * num for num in tmp_vel]
        tmp_pos = [scaling * num for num in tmp_pos]

        return tmp_vel, tmp_pos

    def get_width(self, t: float, extrusion_h: float, filament_dia: Optional[float] = None) -> float:
        """Return the extrusion width for a certain extrusion height at time.

        Args:
            t (float): time
            extrusion_h (float): extrusion height / layer height
            filament_dia (float): filament_diameter

        Returns:
            float: width
        """
        filament_dia = self.initial_machine_setup_dict["filament_diam"] if filament_dia is None else filament_dia

        curr_val = self.get_values(t=t)

        feed_rate = np.linalg.norm(curr_val[0][:3])  # calculate feed rate at current time
        flow_rate = curr_val[0][3]  # get extrusion rate at current time

        filament_cross_sec = np.pi * (filament_dia / 2) ** 2  # calculate cross area of filament
        width = (
            (flow_rate * filament_cross_sec) / (extrusion_h * feed_rate) if feed_rate > 0 else 0
        )  # calculate width, zero if no movement.

        return width

    def print_summary(self, start_time: float):
        """Print simulation summary to console.

        Args:
            start_time (float): time when the simulation run was started
        """
        custom_print(
            f"✅ Simulation finished: pyGCodeDecode extracted {len(self.states)} states from {self.filename}"
            f" and generated {len(self.blocklist)} planner blocks.\n"
            f"Estimated time to travel all states with provided "
            f"printer settings is {self.blocklist[-1].get_segments()[-1].t_end:.2f} seconds.\n"
            f"The Simulation took {(time.time()-start_time):.2f} s of computation time."
        )

    def refresh(self, new_state_list: List[state] = None):
        """Refresh simulation. Either through new state list or by rerunning the self.states as input.

        Args:
            new_state_list: (list[state], default = None) new list of states,
                if None is provided, existing states get resimulated
        """
        if new_state_list is not None:
            self.states = new_state_list

        self.blocklist: List[planner_block] = generate_planner_blocks(
            states=self.states, firmware=self.initial_machine_setup_dict["firmware"]
        )
        self.trajectory_self_correct()

    def extrusion_extent(self, output_unit_system: str = None) -> np.ndarray:
        """Return scaled xyz min & max while extruding.

        Args:
            output_unit_system (str, optional): Unit system for the output.
                The one from the simulation is used, in None is specified.

        Raises:
            ValueError: if nothing is extruded

        Returns:
            np.ndarray: extent of extruding positions
        """
        all_positions_extruding = np.asarray(
            [block.state_A.state_position.get_vec() for block in self.blocklist if block.is_extruding]
            + [block.state_B.state_position.get_vec() for block in self.blocklist if block.is_extruding]
        )

        if len(all_positions_extruding) > 0:
            max_pos = np.amax(all_positions_extruding, axis=0)
            min_pos = np.amin(all_positions_extruding, axis=0)

            scaling = self.get_scaling_factor(output_unit_system=output_unit_system)

            return scaling * np.r_[[min_pos], [max_pos]]
        else:
            raise ValueError("No extrusion happening.")

    def extrusion_max_vel(self, output_unit_system: str = None) -> np.float64:
        """Return scaled maximum velocity while extruding.

        Args:
            output_unit_system (str, optional): Unit system for the output.
                The one from the simulation is used, in None is specified.

        Returns:
            max_vel: (np.float64) maximum travel velocity while extruding
        """
        all_blocks_max_vel = np.asarray(
            [np.linalg.norm(block.extrusion_block_max_vel()[:3]) for block in self.blocklist if block.is_extruding]
        )
        max_vel = np.amax(all_blocks_max_vel, axis=0)

        scaling = self.get_scaling_factor(output_unit_system=output_unit_system)

        return scaling * max_vel

    def save_summary(self, filepath: Union[Path, str]):
        """Save summary to .yaml file.

        Args:
            filepath (Path | str): path to summary file

        Saved data keys:
        - filename (string, filename)
        - t_end (float, end time)
        - x/y/z _min/_max (float, extent where positive extrusion)
        - max_extrusion_travel_velocity (float, maximum travel velocity where positive extrusion)
        """
        t_end = self.blocklist[-1].get_segments()[-1].t_end  # print end time
        extent = self.extrusion_extent()  # extent in [minX, minY, minZ], [maxX, maxY, maxZ]
        max_vel = self.extrusion_max_vel()
        summary = {
            "filename": str(self.filename),
            "t_end": float(t_end),
            "x_min": float(extent[0, 0]),
            "y_min": float(extent[0, 1]),
            "z_min": float(extent[0, 2]),
            "x_max": float(extent[1, 0]),
            "y_max": float(extent[1, 1]),
            "z_max": float(extent[1, 2]),
            "max_extrusion_travel_velocity": float(max_vel),
        }

        # create directory if necessary
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(file=filepath, mode="w") as file:
            yaml.dump(data=summary, stream=file)

        custom_print(f"💾 Summary written to 👉 {str(filepath)}")

    def get_scaling_factor(self, output_unit_system: str = None) -> float:
        """Get a scaling factor to convert lengths from mm to another supported unit system.

        Args:
            output_unit_system (str, optional): Wanted output unit system.
                Uses the one specified for the simulation on None is specified.

        Returns:
            float: scaling factor
        """
        # set the output unit system to the one for the simulation
        if output_unit_system is None:
            output_unit_system = self.output_unit_system

        return self.available_unit_systems[output_unit_system]


class setup:
    """Setup for printing simulation."""

    def __init__(
        self,
        presets_file: str,
        printer: str = None,
        verbosity_level: Optional[int] = None,
        **kwargs,
    ):
        """Initialize the setup for the printing simulation.

        Args:
            presets_file (str): Path to the YAML file containing printer presets.
            printer (str, optional): Name of the printer to select from the preset file. Defaults to None.
            verbosity_level (int, optional): Verbosity level for logging (0: no output, 1: warnings, 2: info, 3: debug). Defaults to None.
            **kwargs: Additional properties to set or override in the setup.

        Raises:
            ValueError: If multiple printers are found in the preset file but none is selected.
        """
        set_verbosity_level(verbosity_level)
        self.available_unit_systems = {"SI": 1e3, "SI (mm)": 1.0, "inch": 25.4}
        self.input_unit_system = "SI (mm)"

        # load the setup
        self.load_setup(presets_file, printer=printer)

        # set additional properties provided as keyword arguments
        self.set_property(kwargs)

    def __getattr__(self, name):
        """Access to setup_dict content."""
        if name in self.setup_dict:
            return self.setup_dict[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """Set setup_dict keys."""
        if name in ["setup_dict", "filename", "available_unit_systems", "input_unit_system"]:
            super().__setattr__(name, value)
        else:
            self.setup_dict[name] = value

    def load_setup(self, filepath, printer=None):
        """Load setup from file.

        Args:
            filepath: (string) specify path to setup file
        """
        import yaml
        from yaml import Loader

        file = open(file=filepath)

        setup_dict = yaml.load(file, Loader=Loader)
        if printer:
            self.setup_dict = setup_dict[printer]
            self.printer = printer
        else:
            printers_available = [printer for printer in setup_dict]

            if len(printers_available) == 1:
                printer = printers_available[0]
                self.setup_dict = setup_dict[printer]
                self.printer = printer
                custom_print(f"Automatically selected the '{printer}' printer in the setup file {filepath}.", lvl=2)
            else:
                raise ValueError("Multiple printers found but none has been selected.")

        # parse initial position if set via config
        if "initial_position" in self.setup_dict:
            self.set_initial_position(self.setup_dict["initial_position"])
        else:
            self.set_initial_position(
                {
                    "X": 0,
                    "Y": 0,
                    "Z": 0,
                    "E": 0,
                }
            )  # default initial pos is zero

    def check_initial_setup(self):
        """Check the printer Dict for typos or missing parameters and raise errors if invalid."""
        req_keys = [
            "p_vel",
            "p_acc",
            "jerk",
            "vX",
            "vY",
            "vZ",
            "vE",
            "X",
            "Y",
            "Z",
            "E",
            "printer",
            "firmware",
        ]
        optional_keys = [
            "layer_cue",
            "nozzle_diam",
            "filament_diam",
            "volumetric_extrusion",
            "absolute_position",
            "absolute_extrusion",
            "initial_position",
            "units",
        ]

        valid_keys = req_keys + optional_keys
        initial_machine_setup = self.setup_dict

        # check if all provided keys are valid
        for key in initial_machine_setup:
            if key not in valid_keys:
                raise ValueError(
                    f"Invalid Key: '{key}' in Setup Dictionary, check for typos. Valid keys are: {valid_keys}"
                )

        # check if every required key is proivded
        for key in req_keys:
            if key not in initial_machine_setup:
                raise ValueError(
                    f"Missing Key: '{key}' is not provided in Setup Dictionary,"
                    f" check for typos. Required keys are: {req_keys}"
                )
        return initial_machine_setup

    def set_initial_position(self, initial_position: Union[tuple, dict], input_unit_system: str = None):
        """Set initial Position.

        Args:
            initial_position: (tuple or dict) set initial position as tuple of len(4)
                or dictionary with keys: {X, Y, Z, E} or "first" to use first occuring absolute position in GCode.
            input_unit_system (str, optional): Wanted input unit system.
                Uses the one specified for the setup if None is specified.

        Example:
        ```python
        setup.set_initial_position((1, 2, 3, 4))
        setup.set_initial_position({"X": 1, "Y": 2, "Z": 3, "E": 4})
        setup.set_initial_position("first") # use first GCode position
        ```

        """
        scaling = self.get_scaling_factor(input_unit_system=input_unit_system)

        if isinstance(initial_position, dict) and all(key in initial_position for key in ["X", "Y", "Z", "E"]):
            for key in initial_position:
                self.setup_dict[key] = scaling * initial_position[key]
        elif isinstance(initial_position, tuple) and len(initial_position) == 4:
            self.setup_dict.update(
                {
                    "X": scaling * initial_position[0],
                    "Y": scaling * initial_position[1],
                    "Z": scaling * initial_position[2],
                    "E": scaling * initial_position[3],
                }
            )
        elif initial_position == "first":  # use first GCode position
            self.setup_dict.update({"X": None, "Y": None, "Z": None, "E": None})
            custom_print("Initial position set to first GCode position.", lvl=3)
        else:
            raise ValueError("Set initial position through dict with keys: {X, Y, Z, E} or as tuple with length 4.")

    def set_property(self, property_dict: dict):
        """Overwrite or add a property to the printer dictionary.

        Args:
            property_dict: (dict) set or add property to the setup

        Example:
        ```python
        setup.set_property({"layer_cue": "LAYER_CHANGE"})
        ```

        """
        self.setup_dict.update(property_dict)

    def get_dict(self) -> dict:
        """Return the setup for the selected printer.

        Returns:
            return_dict: (dict) setup dictionary
        """
        return_dict = self.setup_dict
        return return_dict

    def get_scaling_factor(self, input_unit_system: str = None) -> float:
        """Get a scaling factor to convert lengths from mm to another supported unit system.

        Args:
            input_unit_system (str, optional): Wanted input unit system.
                Uses the one specified for the setup if None is specified.

        Returns:
            float: scaling factor
        """
        # set the output unit system to the one for the simulation
        if input_unit_system is None:
            input_unit_system = self.input_unit_system

        return self.available_unit_systems[input_unit_system]
