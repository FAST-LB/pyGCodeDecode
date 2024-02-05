# -*- coding: utf-8 -*-
"""GCode Interpreter Module."""

import importlib
import pathlib
import sys
import time
from typing import List, Tuple, Union

import numpy as np
import pyvista as pv
import yaml
from matplotlib.figure import Figure

from .planner_block import planner_block
from .state import state
from .state_generator import state_generator
from .utils import segment, velocity


def update_progress(progress: Union[float, int], name: str = "Percent") -> None:
    """Display or update a console progress bar.

    Args:
        progress: (float | int) between 0 and 1 for percentage, < 0 represents a 'halt', > 1 represents 100%
        name: (string, default = "Percent") customizable name for progress bar
    """
    barLength = 10
    status = ""

    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength * progress))
    progress = round(progress * 100, ndigits=1)
    text = f"\r[{'#' * block + '-' * (barLength - block)}] {progress} % of {name} {status}"
    # LINE_UP = '\033[1A'
    # LINE_CLEAR = '\x1b[2K'
    # print(LINE_UP + LINE_UP, end=LINE_CLEAR)
    # print(text)
    sys.stdout.write(text)
    sys.stdout.flush()


def generate_planner_blocks(states: List[state], firmware=None):
    """Convert list of states to trajectory repr. by planner blocks.

    Args:
        states: (list[state]) list of states
        firmware: (string, default = None) select firmware by name

    Returns:
        block_list (list[planner_block]) list of all planner blocks to complete travel between all states
    """
    block_list = []
    for i, this_state in enumerate(states):
        prev_block = block_list[-1] if len(block_list) > 0 else None  # grab prev block from block_list
        new_block = planner_block(state=this_state, prev_block=prev_block, firmware=firmware)  # generate new block
        if len(new_block.get_segments()) > 0:
            if new_block.prev_block is not None:
                new_block.prev_block.next_block = new_block  # update nb list
            block_list.append(new_block)
        update_progress((i + 1) / len(states), "Planner Block Generation")
    return block_list


def find_current_segment(path: List[segment], t: float, last_index: int = None, keep_position: bool = False):
    """Find the current segment.

    Args:
        path: (list[segment]) all segments to be searched
        t: (float) time of search
        last_index: (int) last found index for optimizing search
        keep_position: (bool) keeps position of last segment, use this when working with gaps of no movement between segments

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
            print("No movement at this time in Path!")
            return None, None
        elif last_index is None or len(path) - 1 < last_index or path[last_index].t_begin > t:
            # print(f"unoptimized Search, last index: {last_index}")
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
        gcode_path: pathlib.Path,
        machine_name: str = None,
        initial_machine_setup: "setup" = None,
        output_unit_system: str = "SImm",
    ):
        """Initialize the Simulation of a given G-code with initial machine setup or default machine.

        - Generate all states from GCode.
        - Connect states with planner blocks, consisting of segments
        - Self correct inconsistencies.

        Args:
            gcode_path: (Path) path to GCode
            machine name: (string, default = None) name of the default machine to use
            initial_machine_setup: (setup, default = None) setup instance
            output_unit_system: (string, default = "SImm") available unit systems: SI, SImm & inch

        Example:
        ```python
        gcode_interpreter.simulation(gcode_path=r"path/to/part.gcode", initial_machine_setup=printer_setup)
        ```
        """
        simulation_start_time = time.time()
        self.last_index = None  # used to optimize search in segment list
        self.filename = gcode_path
        self.firmware = None

        # set output unit system
        self.available_unit_systems = {"SI": 1e-3, "SImm": 1.0, "inch": 1 / 25.4}
        if output_unit_system in self.available_unit_systems:
            self.output_unit_system = output_unit_system
        else:
            raise ValueError("Chosen unit system is unavailable!")

        # create a printer setup with default values if none was specified
        if initial_machine_setup is not None:
            if machine_name is not None and initial_machine_setup.get_dict()["printer_name"] != machine_name:
                raise ValueError("Both a printer name and a printer setup were specified, but they do not match!")
            else:
                pass
        else:
            if machine_name is None:
                raise ValueError("Neither a printer name nor a printer setup was specified. At least one is required!")
            else:
                print(
                    "Only a machine name was specified but no full setup. Trying to create a setup from pyGCD's default values..."
                )
                default_presets_file = importlib.resources.files("pyGCodeDecode").joinpath(
                    "data/default_printer_presets.yaml"
                )
                initial_machine_setup = setup(
                    presets_file=default_presets_file,
                    printer=machine_name,
                )

        # SET INITIAL SETTINGS
        self.initial_machine_setup = initial_machine_setup.get_dict()
        self.check_initial_setup(initial_machine_setup=self.initial_machine_setup)  # move this to setup class todo
        self.firmware = self.initial_machine_setup["firmware"]

        self.states: List[state] = state_generator(
            filepath=gcode_path, initial_machine_setup=self.initial_machine_setup
        )

        print(
            f"Simulating \"{self.filename}\" with {self.initial_machine_setup['printer_name']} using the {self.firmware} firmware.\n"
        )
        self.blocklist: List[planner_block] = generate_planner_blocks(states=self.states, firmware=self.firmware)
        self.trajectory_self_correct()

        self.print_summary(start_time=simulation_start_time)

    def plot_2d_position(
        self,
        filename="trajectory_2D.png",
        colvar="Velocity",
        show_points=False,
        colvar_spatial_resolution=1,
        dpi=400,
        scaled=True,
        show=False,
    ):
        """Plot 2D position (XY plane) with matplotlib (unmaintained)."""
        import matplotlib.pyplot as plt
        from matplotlib import cm
        from matplotlib.collections import LineCollection

        colvar_label = {"Velocity": "Velocity in mm/s", "Acceleration": "Acceleration in mm/s^2"}

        def interp_2D(x, y, cvar, spatial_resolution=1):
            segm_length = np.linalg.norm([np.ediff1d(x), np.ediff1d(y)], axis=0)
            segm_cvar_delt = np.greater(np.abs(np.ediff1d(cvar)), 0)
            segm_interpol = np.r_[
                0, np.where(segm_cvar_delt, np.ceil(segm_length / spatial_resolution) + 1, 1)
            ]  # get nmbr of segments for required resolution, dont interpolate if there is no change
            points = np.array([x, y, cvar]).T
            points = np.c_[points, segm_interpol]

            # generate intermediate points with set resolution
            old_point = None
            interpolated = np.zeros((1, 3))
            for point in points:
                if old_point is not None:
                    steps = np.linspace(0, 1, int(point[3]), endpoint=True)
                    x_i = np.interp(steps, [0, 1], [old_point[0], point[0]])
                    y_i = np.interp(steps, [0, 1], [old_point[1], point[1]])
                    colvar_i = np.interp(steps, [0, 1], [old_point[2], point[2]])
                    interpolated = np.r_[interpolated, np.array([x_i, y_i, colvar_i]).T]
                old_point = point
            interpolated = np.delete(interpolated, 0, 0)

            return interpolated

        segments = unpack_blocklist(blocklist=self.blocklist)
        if colvar == "Velocity":
            # get all planned trajectory vertices + color variable
            x, y, cvar = [], [], []
            x.append(segments[0].pos_begin.get_vec()[0])
            y.append(segments[0].pos_begin.get_vec()[1])
            cvar.append(segments[0].vel_begin.get_norm())

            for i, segm in enumerate(segments):
                update_progress((i + 1) / len(segments), name="2D Plot Lines")
                x.append(segm.pos_end.get_vec()[0])
                y.append(segm.pos_end.get_vec()[1])
                cvar.append(segm.vel_end.get_norm())

            # interpolate values for smooth coloring
            interpolated = interp_2D(x, y, cvar, spatial_resolution=colvar_spatial_resolution)

            x = interpolated[:, 0]
            y = interpolated[:, 1]
            cvar = interpolated[:, 2]  # maybe change interpolation to return tuple?

            # generate point pairs for line collection
            point_pairs = []
            for i in np.arange(len(x) - 1):
                point_pairs.append([(x[i], y[i]), (x[i + 1], y[i + 1])])

            # generate collection from pairs
            collection = LineCollection(point_pairs)
            collection.set_array(cvar)
            collection.set_cmap(cm.jet)

            fig = plt.figure()
            ax1 = fig.add_subplot(1, 1, 1)
            ax1.add_collection(collection)
            ax1.autoscale()
            plt.colorbar(collection, label=colvar_label[colvar], shrink=0.6, location="right")
        else:
            x, y = [], []
            x.append(segments[0].pos_begin.get_vec()[0])
            y.append(segments[0].pos_begin.get_vec()[1])
            for i, segm in enumerate(segments):
                update_progress((i + 1) / len(segments), name="2D Plot Lines")
                x.append(segm.pos_end.get_vec()[0])
                y.append(segm.pos_end.get_vec()[1])
            fig = plt.subplot()
            fig.plot(x, y, color="black")

        if show_points:
            for i, block in enumerate(self.blocklist):
                update_progress(i / len(self.blocklist), name="2D Plot Points")
                fig.scatter(
                    block.get_segments()[-1].pos_end.get_vec()[0],
                    block.get_segments()[-1].pos_end.get_vec()[1],
                    color="blue",
                    marker="x",
                )

        plt.xlabel("x position")
        plt.ylabel("y position")
        plt.title("2D Position")
        if scaled:
            plt.axis("scaled")
        if filename is not False:
            plt.savefig(filename, dpi=dpi)
            print("2D Plot saved as ", filename)
        if show:
            plt.show()
            return fig
        plt.close()

    def plot_3d(self, extrusion_only: bool = True):
        """3D Plot with PyVista.

        Args:
            extrusion_only (bool, default=True): Plot only parts where material is extruded.
        """
        # https://docs.pyvista.org/version/stable/api/core/_autosummary/pyvista.polydatafilters.extrude
        # https://docs.pyvista.org/version/stable/examples/01-filter/extrude-rotate

        # get all data for plots
        segments = unpack_blocklist(blocklist=self.blocklist)

        network = pv.MultiBlock()

        x, y, z, e, vel = [], [], [], [], []

        for n, segm in enumerate(segments):
            update_progress((n + 1) / len(segments), name="3D Plot")

            if (not extrusion_only) or (segm.is_extruding()):
                if len(x) == 0:
                    # append segm begin values to plotting array for first segm
                    pos_begin_vec = segm.pos_begin.get_vec(withExtrusion=True)
                    x.append(pos_begin_vec[0])
                    y.append(pos_begin_vec[1])
                    z.append(pos_begin_vec[2])
                    e.append(pos_begin_vec[3])
                    vel.append(segm.vel_begin.get_norm())

                # append segm end values to plotting array
                pos_end_vec = segm.pos_end.get_vec(withExtrusion=True)

                x.append(pos_end_vec[0])
                y.append(pos_end_vec[1])
                z.append(pos_end_vec[2])
                e.append(pos_end_vec[3])
                vel.append(segm.vel_end.get_norm())

            # plot if following segment is not extruding or if it's the last segment
            if (extrusion_only and (len(x) > 0 and not segm.is_extruding())) or (len(x) > 0 and n == len(segments) - 1):
                points_3d = np.column_stack((x, y, z))
                line = pv.lines_from_points(points_3d)
                line["velocity"] = vel
                tube = line.tube(radius=0.2, n_sides=6)
                network.append(tube)
                x, y, z, e, vel = [], [], [], [], []  # clear plotting array

        network = network.combine()
        p = pv.Plotter()
        p.add_mesh(
            network,
            scalars="velocity",
            smooth_shading=True,
            scalar_bar_args={"title": "travel velocity in mm/s"},
        )
        p.show()

    def plot_vel(
        self,
        axis: Tuple[str] = ("x", "y", "z", "e"),
        show: bool = True,
        show_planner_blocks: bool = True,
        show_segments: bool = False,
        show_jv: bool = False,
        time_steps: Union[int, str] = "constrained",
        filepath: pathlib.Path = None,
        dpi: int = 400,
    ) -> Figure:
        """Plot axis velocity with matplotlib.

        Args:
            axis: (tuple(string), default = ("x", "y", "z", "e")) select plot axis
            show: (bool, default = True) show plot and return plot figure
            show_planner_blocks: (bool, default = True) show planner_blocks as vertical lines
            show_segments: (bool, default = False) show segments as vertical lines
            show_jv: (bool, default = False) show junction velocity as x
            time_steps: (int or string, default = "constrained") number of time steps or constrain plot vertices to segment vertices
            filepath: (Path, default = None) save fig as image if filepath is provided
            dpi: (int, default = 400) select dpi

        Returns:
        (optionally)
            fig: (figure)
        """
        import matplotlib.pyplot as plt

        axis_dict = {"x": 0, "y": 1, "z": 2, "e": 3}

        segments = unpack_blocklist(blocklist=self.blocklist)  # unpack

        # time steps
        if type(time_steps) is int:  # evenly distributed time steps
            times = np.linspace(0, self.blocklist[-1].get_segments()[-1].t_end, time_steps, endpoint=False)
        elif time_steps == "constrained":  # use segment time points as plot constrains
            times = [0]
            for segm in segments:
                times.append(segm.t_end)
        else:
            raise ValueError("Invalid value for 'time_steps', either use Integer or 'constrained' as argument.")

        # gathering values
        pos = [[], [], [], []]
        vel = [[], [], [], []]
        abs = []  # initialize value arrays
        index_saved = 0

        for i, t in enumerate(times):
            segm, index_saved = find_current_segment(path=segments, t=t, last_index=index_saved, keep_position=True)

            tmp_vel = segm.get_velocity(t=t).get_vec(withExtrusion=True)
            tmp_pos = segm.get_position(t=t).get_vec(withExtrusion=True)
            for ax in axis:
                pos[axis_dict[ax]].append(tmp_pos[axis_dict[ax]])
                vel[axis_dict[ax]].append(tmp_vel[axis_dict[ax]])

            abs.append(np.linalg.norm(tmp_vel[:3]))
            update_progress((i + 1) / len(times), name="Velocity Plot")

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        # plot JD-Limits
        for block in self.blocklist:
            # planner blocks vertical line plot
            if show_planner_blocks:
                ax1.axvline(x=block.get_segments()[-1].t_end, color="black", lw=0.5)

            # segments vertical line plot
            if show_segments:
                for segm in block.get_segments():
                    ax1.axvline(x=segm.t_end, color="green", lw=0.25)

            if show_jv:
                # absolute JD Marker
                absJD = np.linalg.norm([block.JD[0], block.JD[1], block.JD[2]])
                ax1.scatter(x=block.get_segments()[-1].t_end, y=absJD, color="red", marker="x")
                for ax in axis:
                    ax1.scatter(
                        x=block.get_segments()[-1].t_end, y=block.JD[axis_dict[ax]], marker="x", color="black", lw=0.5
                    )

        # plot all axis in velocity and position
        for ax in axis:
            ax1.plot(times, vel[axis_dict[ax]], label=ax)  # velocity
            ax2.plot(times, pos[axis_dict[ax]], linestyle="--")  # position w/ extrusion
            # if not ax == "e": ax2.plot(times,pos[axis_dict[ax]],linestyle="--") #position ignoring extrusion
        ax1.plot(times, abs, color="black", label="abs")  # absolute velocity

        ax1.set_xlabel("time in s")
        ax1.set_ylabel("velocity in mm/s")
        ax2.set_ylabel("position in mm")
        ax1.legend(loc="lower left")
        plt.title("Velocity and Position over Time")
        if filepath is not None:
            plt.savefig(filepath, dpi=dpi)
        if show:
            plt.show()
        plt.close()
        return fig

    def trajectory_self_correct(self):
        """Self correct all blocks in the blocklist with self_correction() method."""
        # self correction
        for block in self.blocklist:
            block.self_correction()

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
        segm, self.last_index = find_current_segment(path=segments, t=t, last_index=self.last_index)
        tmp_vel = segm.get_velocity(t=t).get_vec(withExtrusion=True)
        tmp_pos = segm.get_position(t=t).get_vec(withExtrusion=True)

        scaling = self.get_scaling_factor(output_unit_system=output_unit_system)

        # scale to required unit system
        tmp_vel = [scaling * num for num in tmp_vel]
        tmp_pos = [scaling * num for num in tmp_pos]

        return tmp_vel, tmp_pos

    def check_initial_setup(self, initial_machine_setup):
        """Check the printer Dict for typos or missing parameters and raise errors if invalid.

        Args:
            initial_machine_setup: (dict) initial machine setup dictionary
        """
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
            "printer_name",
            "firmware",
        ]
        optional_keys = [
            "layer_cue",
            "nozzle_diam",
            "filament_diam",
        ]

        valid_keys = req_keys + optional_keys

        # check if all provided keys are valid
        for key in initial_machine_setup:
            if key not in valid_keys:
                raise ValueError(
                    f'Invalid Key: "{key}" in Setup Dictionary, check for typos. Valid keys are: {valid_keys}'
                )

        # check if every required key is proivded
        for key in req_keys:
            if key not in initial_machine_setup:
                raise ValueError(
                    f'Missing Key: "{key}" is not provided in Setup Dictionary, check for typos. Required keys are: {req_keys}'
                )

    def print_summary(self, start_time: float):
        """Print simulation summary to console.

        Args:
            start_time (float): time when the simulation run was started
        """
        print(
            f" >> pyGCodeDecode extracted {len(self.states)} states from {self.filename} and generated {len(self.blocklist)} planner blocks.\n"
            f"Estimated time to travel all states with provided printer settings is {self.blocklist[-1].get_segments()[-1].t_end:.2f} seconds.\n"
            f"The Simulation took {(time.time()-start_time):.2f} s."
        )

    def refresh(self, new_state_list: List[state] = None):
        """Refresh simulation. Either through new state list or by rerunning the self.states as input.

        Args:
            new_state_list: (list[state], default = None) new list of states, if None is provided, existing states get resimulated
        """
        if new_state_list is not None:
            self.states = new_state_list

        self.blocklist: List[planner_block] = generate_planner_blocks(
            states=self.states, firmware=self.initial_machine_setup["firmware"]
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
            [block.state_B.state_position.get_vec() for block in self.blocklist if block.is_extruding]
        )
        if len(all_positions_extruding) > 0:
            max_pos = np.amax(all_positions_extruding, axis=0)
            min_pos = np.amin(all_positions_extruding, axis=0)

            scaling = self.get_scaling_factor(output_unit_system=output_unit_system)

            return scaling * np.r_[[min_pos], [max_pos]]
        else:
            raise ValueError("No extrusion happening.")

    def extrusion_max_vel(self, output_unit_system: str = None) -> np.ndarray:
        """Return scaled maximum velocity while extruding.

        Args:
            output_unit_system (str, optional): Unit system for the output.
                The one from the simulation is used, in None is specified.

        Returns:
            max_vel: (numpy.ndarray, 1x4) maximum axis velocity while extruding
        """
        all_blocks_max_vel = np.asarray(
            [np.linalg.norm(block.extrusion_block_max_vel()[:3]) for block in self.blocklist if block.is_extruding]
        )
        max_vel = np.amax(all_blocks_max_vel, axis=0)

        scaling = self.get_scaling_factor(output_unit_system=output_unit_system)

        return scaling * max_vel

    def save_summary(self, filepath: Union[pathlib.Path, str]):
        """Save summary to .yaml file.

        Args:
            filepath (pathlib.Path | str): path to summary file

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
        pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(file=filepath, mode="w") as file:
            yaml.dump(data=summary, stream=file)

        print(f"Summary written to:\n{str(filepath)}")

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
        layer_cue: str = None,
    ) -> None:
        """Create simulation setup.

        Args:
            presets_file: (string) choose setup yaml file with printer presets
            printer: (string) select printer from preset file
            layer_cue: (string) set slicer specific layer change cue from comment
        """
        # the input unit system is only implemented for 'set_initial_position'.
        # Regardless, the class has this attribute so it's more similar to the simulation class.
        self.available_unit_systems = {"SI": 1e3, "SImm": 1.0, "inch": 25.4}
        self.input_unit_system = "SImm"

        self.initial_position = {"X": 0, "Y": 0, "Z": 0, "E": 0}  # default initial pos is zero
        self.setup_dict = self.load_setup(presets_file)

        self.filename = presets_file
        self.printer_select = printer
        self.layer_cue = layer_cue

        if self.printer_select is not None:
            self.select_printer(printer_name=self.printer_select)
            self.firmware = self.get_dict()["firmware"]

    def load_setup(self, filepath):
        """Load setup from file.

        Args:
            filepath: (string) specify path to setup file
        """
        import yaml
        from yaml import Loader

        file = open(file=filepath, mode="r")

        setup_dict = yaml.load(file, Loader=Loader)
        return setup_dict

    def select_printer(self, printer_name):
        """Select printer by name.

        Args:
            printer_name: (string) select printer by name
        """
        if printer_name not in self.setup_dict:
            raise ValueError(f"Selected Printer {self.printer_select} not found in setup file: {self.filename}.")
        else:
            self.printer_select = printer_name

    def set_initial_position(self, initial_position: Union[tuple, dict], input_unit_system: str = None):
        """Set initial Position.

        Args:
            initial_position: (tuple or dict) set initial position as tuple of len(4) or dictionary with keys: {X, Y, Z, E}.
            input_unit_system (str, optional): Wanted input unit system.
                Uses the one specified for the setup if None is specified.

        Example:
        ```python
        setup.set_initial_position((1, 2, 3, 4))
        setup.set_initial_position({"X": 1, "Y": 2, "Z": 3, "E": 4})
        ```

        """
        scaling = self.get_scaling_factor(input_unit_system=input_unit_system)

        if isinstance(initial_position, dict) and all(key in initial_position for key in ["X", "Y", "Z", "E"]):
            for key in initial_position:
                self.initial_position[key] = scaling * initial_position[key]
        elif isinstance(initial_position, tuple) and len(initial_position) == 4:
            self.initial_position = {
                "X": scaling * initial_position[0],
                "Y": scaling * initial_position[1],
                "Z": scaling * initial_position[2],
                "E": scaling * initial_position[3],
            }
        else:
            raise ValueError("Set initial position through dict with keys: {X, Y, Z, E} or as tuple with length 4.")

    def set_property(self, property_dict: dict):
        """Overwrite or add a property to the printer dictionary. Printer has to be selected through select_printer() beforehand.

        Args:
            property_dict: (dict) set or add property to the setup

        Example:
        ```python
        setup.set_property({"layer_cue": "LAYER_CHANGE"})
        ```

        """
        if self.printer_select is not None:
            self.setup_dict[self.printer_select].update(property_dict)
        else:
            raise ValueError("No printer is selected. Select printer through select_printer() beforehand.")

    def get_dict(self) -> dict:
        """Return the setup for the selected printer.

        Returns:
            return_dict: (dict) setup dictionary
        """
        return_dict = self.setup_dict[self.printer_select]  # create dict
        return_dict.update(self.initial_position)  # add initial position
        if self.layer_cue is not None:
            return_dict.update({"layer_cue": self.layer_cue})  # add layer cue
        return_dict.update({"printer_name": self.printer_select})  # add printer name

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
