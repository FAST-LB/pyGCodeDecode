"""Tools for pyGCD."""

import locale as loc
import pathlib
from typing import Union

import numpy as np
import yaml

from .gcode_interpreter import simulation


def save_layer_metrics(
    simulation: simulation,
    filepath: Union[pathlib.Path, str] = "./layer_metrics.csv",
    locale: str = None,
    delimiter: str = ";",
):
    """Print out print times, distance traveled and the average travel speed to a csv-file.

    Args:
        simulation: (simulation) simulation instance
        filepath: (Path | string, default = "./layer_metrics.csv") file name
        locale: (string, default = None) select locale settings, e.g. "en_US.utf8" "de_DE.utf8", None = use system locale
        delimiter: (string, default = ";") select delimiter

    Layers are detected using the given layer cue.
    """
    if "layer_cue" in simulation.initial_machine_setup:
        if locale is None:
            loc.setlocale(loc.LC_ALL, "")
        else:
            loc.setlocale(loc.LC_ALL, locale)

        delimiter = delimiter + " "  # add space after delimiter

        # create directory if necessary
        pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(file=filepath, mode="w") as p_log:
            p_log.write(
                f"layer{delimiter}layer time in s{delimiter}travel distance in mm{delimiter}avg speed in mm/s\n"
            )

            next_layer = 0
            current_layer = 0
            last_layer_time = 0
            travel = 0
            for block in simulation.blocklist:
                next_layer = block.state_B.layer
                if next_layer > current_layer:
                    block_begin = block.segments[0].t_begin
                    duration = block_begin - last_layer_time
                    p_log.write(
                        str(current_layer)
                        + delimiter
                        + loc.str(duration)
                        + delimiter
                        + loc.str(travel)
                        + delimiter
                        + (loc.str(travel / duration) if duration != 0 else "NaN")
                        + "\n"
                    )
                    travel = 0
                    last_layer_time = block_begin
                    current_layer = next_layer

                if block.next_block is None:
                    block_end = block.segments[-1].t_end
                    duration = block_end - last_layer_time

                    p_log.write(
                        str(current_layer)
                        + delimiter
                        + loc.str(duration)
                        + delimiter
                        + loc.str(travel)
                        + delimiter
                        + loc.str((travel / duration) if duration > 0 else "NaN")
                        + "\n"
                    )
                travel += block.get_block_travel()

        print(f"💾 Layer metrics written to:\n👉 {str(filepath)}")
    else:
        print("⚠️ No layer_cue was specified in the simulation setup. Therefore, layer metrics can not be saved!")


def write_submodel_times(
    simulation: simulation,
    sub_orig: list,
    sub_side_x_len: float,
    sub_side_y_len: float,
    sub_side_z_len: float,
    filename="submodel_times.yaml",
    **kwargs,
):
    """Write the submodel entry and exit times to a yaml file.

    Args:
        simulation: (simulation) the simulation instance to analyze
        sub_orig: (list with [xcoord, ycoord, zcoord]) the origin of the submodel control volume
        sub_side_len: (float) the side length of the submodel control volume
        filename: (string) yaml filename
        **kwargs: (any) provide additional info to write into the yaml file
    """

    class cube:
        def __init__(self, origin, side_x_len, side_y_len, side_z_len) -> None:
            """Define a cube with origin and side length. Cube is axis aligned."""
            self.origin = origin
            self.side_x_len = side_x_len
            self.side_y_len = side_y_len
            self.side_z_len = side_z_len

        def get_plane_lim(self):
            return [
                [
                    self.origin[0] + self.side_x_len / 2,
                    self.origin[0] - self.side_x_len / 2,
                ],
                [
                    self.origin[1] + self.side_y_len / 2,
                    self.origin[1] - self.side_y_len / 2,
                ],
                [
                    self.origin[2] + self.side_z_len / 2,
                    self.origin[2] - self.side_z_len / 2,
                ],
            ]

        def get_plane_normals(self):
            """Create Plane normals."""
            X_pos = [1, 0, 0]
            X_neg = [-1, 0, 0]

            Y_pos = [0, 1, 0]
            Y_neg = [0, -1, 0]

            Z_pos = [0, 0, 1]
            Z_neg = [0, 0, -1]

            return [X_pos, X_neg, Y_pos, Y_neg, Z_pos, Z_neg]

        def get_plane_orig(self):
            """Create Plane origins."""
            X_pos = [self.origin[0] + self.side_x_len / 2, 0, 0]
            X_neg = [self.origin[0] - self.side_x_len / 2, 0, 0]

            Y_pos = [0, self.origin[1] + self.side_y_len / 2, 0]
            Y_neg = [0, self.origin[1] - self.side_y_len / 2, 0]

            Z_pos = [0, 0, self.origin[2] + self.side_z_len / 2]
            Z_neg = [0, 0, self.origin[2] - self.side_z_len / 2]

            return [X_pos, X_neg, Y_pos, Y_neg, Z_pos, Z_neg]

    def point_eval(point, pl_lim):
        p_eval = []
        for lim_n, p_n in zip(pl_lim, point):
            inters_pl = [p_n <= lim_n[0], p_n >= lim_n[1]]  # check if point is inside of [CV+, CV-]
            p_eval.append(inters_pl)
        return p_eval

    def point_inside(p_eval):
        return all([all(p_ev_ax) for p_ev_ax in p_eval])

    def intersect_possible(p_eval0, p_eval1):
        possible = False
        for ax_eval0, ax_eval1 in zip(p_eval0, p_eval1):

            if ax_eval0 != ax_eval1:
                # crossing
                possible = True  # if one axis crosses any plane, intersection is possible
            elif ax_eval0 == [True, True]:
                # contained
                pass  # no decision can be made here
            else:
                # not inside and not crossing
                return False  # if one axis is not crossing OR contained, CV is impossible

        return possible

    def isect_line_plane(p0, p1, p_co, p_no, epsilon=1e-6):
        """Return a Vector or None (when the intersection can't be found).

        p0, p1: Define the line.
        p_co, p_no: define the plane:
            p_co Is a point on the plane (plane coordinate).
            p_no Is a normal vector defining the plane direction;
                (does not need to be normalized).
        """
        p0 = np.asarray(p0)
        p1 = np.asarray(p1)
        p_co = np.asarray(p_co)
        p_no = np.asarray(p_no)

        u = p1 - p0
        dot = p_no.dot(u)

        if abs(dot) > epsilon:
            # The factor of the point between p0 -> p1 (0 - 1)
            # if 'fac' is between (0 - 1) the point intersects with the segment.
            # Otherwise:
            #  < 0.0: behind p0.
            #  > 1.0: infront of p1.

            w = p0 - p_co
            fac = -np.dot(p_no, w) / dot
            u = u * fac
            if fac >= 0 and fac <= 1:
                return p0 + u, np.linalg.norm(u), True if dot < 0 else False

        # The segment is parallel to plane.
        return None, None, None

    # METHOD IMPLEMENTATION
    control_volume = cube(
        origin=sub_orig, side_x_len=sub_side_x_len, side_y_len=sub_side_y_len, side_z_len=sub_side_z_len
    )  # define control volume
    timetable = []

    for block in simulation.blocklist:
        p_eval_A = point_eval(block.state_A.state_position.get_vec(), control_volume.get_plane_lim())
        p_eval_B = point_eval(block.state_B.state_position.get_vec(), control_volume.get_plane_lim())

        if intersect_possible(p_eval0=p_eval_A, p_eval1=p_eval_B):
            for plane_orig, plane_normal in zip(control_volume.get_plane_orig(), control_volume.get_plane_normals()):
                isec, s_len, sgn = isect_line_plane(
                    p0=block.state_A.state_position.get_vec(),
                    p1=block.state_B.state_position.get_vec(),
                    p_co=plane_orig,
                    p_no=plane_normal,
                )

                if isec is not None and point_inside(p_eval=point_eval(isec, control_volume.get_plane_lim())):
                    timetable.append([float(block.inverse_time_at_pos(s_len)), sgn])

    timetable = np.asarray(timetable)  # convert list to array for sorting
    timetable = timetable[timetable[:, 0].argsort()]  # sort array by first column

    time_in = timetable[:, 0][np.asarray(timetable[:, 1], dtype=bool)]  # filter the data for entering the CV
    time_out = timetable[:, 0][~np.asarray(timetable[:, 1], dtype=bool)]  # filter the data for exiting the CV

    with open(filename, "w") as file:
        yaml.dump(kwargs, file)  # add all kwargs to the file#
        yaml.dump({"time_process": float(simulation.blocklist[-1].get_segments()[-1].t_end)}, file)
        yaml.dump({"n_filaments": len(time_in)}, file)
        yaml.dump({"time_in": time_in.tolist()}, file)  # write out all time IN
        yaml.dump({"time_out": time_out.tolist()}, file)  # write out all time OUT

    file.close()
