"""WIP gcode Reader"""
import numpy as np
from typing import List
from .planner_block import planner_block
from .state import state
from .state_generator import state_generator
from .utils import segment, velocity


def update_progress(progress, name="Percent"):
    # update_progress() : Displays or updates a console progress bar
    # Accepts a float between 0 and 1. Any int will be converted to a float.
    # A value under 0 represents a 'halt'.
    # A value at 1 or bigger represents 100%

    import sys

    barLength = 10  # Modify this to change the length of the progress bar
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
    text = "\r[{1}] {2}% of {0} {3}".format(name, "#" * block + "-" * (barLength - block), progress, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def generate_planner_blocks(states: List[state]):
    """
    converts list of states to trajectory segments

    Parameters
    ----------
    states  :   List[state]
        list of states

    Returns
    ----------
    blck_list[planner_block]
        list of all plannerblocks to complete travel between all states
    """

    blck_list = []
    cntr = 0
    for state in states:  # noqa
        cntr += 1
        prev_blck = blck_list[-1] if len(blck_list) > 0 else None  # grab prev blck from blck_list
        new_blck = planner_block(state=state, prev_blck=prev_blck)  # generate new blck
        if len(new_blck.get_segments()) > 0:
            if new_blck.prev_blck is not None:
                new_blck.prev_blck.next_blck = new_blck  # update nb list
            blck_list.extend([new_blck])
        update_progress(cntr / len(states), "Planner Block Generation")
    return blck_list


def find_current_segm(path: List[segment], t: float, last_index: int = None, keep_position: bool = False):
    """
    finds the current segment

    Parameters
    ----------
    path    :   List[segment]
        all segments to be searched
    t       :   float
        time of search
    last_index: int
        last found index for optimizing search
    keep_position: bool
        keeps position of last segment, use this when working with gaps of no movement inbetween segments

    Returns
    ----------
    segment
        the segment which defines movement at that point in time
    last_index
        last index where something was found, search speed optimization possible
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
    """
    Returns list of segments by unpacking list of plannerblocks.
    """
    path = []
    for block in blocklist:
        path.extend(block.get_segments()[:])
    return path


class simulate:
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
        import matplotlib.pyplot as plt
        from matplotlib.collections import LineCollection
        from matplotlib import cm

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
            cvar.append(segments[0].vel_begin.get_abs())

            cntr = 0
            for segm in segments:
                cntr += 1
                update_progress(cntr / len(segments), name="2D Plot Lines")
                x.append(segm.pos_end.get_vec()[0])
                y.append(segm.pos_end.get_vec()[1])
                cvar.append(segm.vel_end.get_abs())

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
            cntr = 0
            for segm in segments:
                cntr += 1
                update_progress(cntr / len(segments), name="2D Plot Lines")
                x.append(segm.pos_end.get_vec()[0])
                y.append(segm.pos_end.get_vec()[1])
            fig = plt.subplot()
            fig.plot(x, y, color="black")

        if show_points:
            cntr = 0
            for blck in self.blocklist:
                update_progress(cntr / len(self.blocklist), name="2D Plot Points")
                fig.scatter(
                    blck.get_segments()[-1].pos_end.get_vec()[0],
                    blck.get_segments()[-1].pos_end.get_vec()[1],
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

    def plot_3d_position_legacy(
        self, filename="trajectory_3D.png", dpi=400, show=False, colvar_spatial_resolution=1, colvar="Velocity"
    ):
        import matplotlib.pyplot as plt
        from matplotlib import cm
        from mpl_toolkits.mplot3d.art3d import Line3DCollection

        # from matplotlib.colors import ListedColormap, BoundaryNorm
        # from matplotlib.collections import LineCollection
        # from mpl_toolkits.mplot3d import Axes3D

        colvar_label = {"Velocity": "Velocity in mm/s", "Acceleration": "Acceleration in mm/s^2"}

        def colorline(x, y, z, c):
            # xyz    = positon
            # c      = color variable
            c = cm.jet((c - np.min(c)) / (np.max(c) - np.min(c)))
            ax = plt.gca()

            for i in np.arange(len(x) - 1):
                ax.plot([x[i], x[i + 1]], [y[i], y[i + 1]], [z[i], z[i + 1]], c=c[i])

        def interp(x, y, z, colvar, spatial_resolution=1):
            segm_length = np.linalg.norm([np.ediff1d(x), np.ediff1d(y), np.ediff1d(z)], axis=0)
            segm_colvar_delt = np.greater(np.abs(np.ediff1d(colvar)), 0)
            segm_interpol = np.r_[
                0, np.where(segm_colvar_delt, np.ceil(segm_length / spatial_resolution) + 1, 1)
            ]  # get nmbr of segments for required resolution, dont interpolate if there is no change
            points = np.array([x, y, z, colvar]).T
            points = np.c_[points, segm_interpol]

            # generate intermediate points with set resolution
            old_point = None
            interpolated = np.zeros((1, 4))
            for point in points:
                if old_point is not None:
                    steps = np.linspace(0, 1, int(point[4]), endpoint=True)
                    x_i = np.interp(steps, [0, 1], [old_point[0], point[0]])
                    y_i = np.interp(steps, [0, 1], [old_point[1], point[1]])
                    z_i = np.interp(steps, [0, 1], [old_point[2], point[2]])
                    colvar_i = np.interp(steps, [0, 1], [old_point[3], point[3]])
                    interpolated = np.r_[interpolated, np.array([x_i, y_i, z_i, colvar_i]).T]
                old_point = point
            interpolated = np.delete(interpolated, 0, 0)

            return interpolated

        def w_collection(interpolated):
            segments = interpolated[:, :3]
            c = interpolated[:, 3:].T
            coll = Line3DCollection(segments)
            coll.set_array(c)
            fig = plt.figure()
            ax = fig.gca(projection="3d")
            plt.title("3D-Figure")
            ax.add_collection3d(coll)

        # https://matplotlib.org/stable/gallery/lines_bars_and_markers/multicolored_line.html
        # https://stackoverflow.com/questions/17240694/how-to-plot-one-line-in-different-colors
        # https://stackoverflow.com/questions/13622909/matplotlib-how-to-colorize-a-large-number-of-line-segments-as-independent-gradi

        # get all data for plots
        segments = unpack_blocklist(blocklist=self.blocklist)
        if colvar == "Velocity":
            x, y, z, vel = [], [], [], []
            x.append(segments[0].pos_begin.get_vec()[0])
            y.append(segments[0].pos_begin.get_vec()[1])
            z.append(segments[0].pos_begin.get_vec()[2])
            vel.append(segments[0].vel_begin.get_abs())

            cntr = 0
            for segm in segments:
                cntr += 1
                update_progress(cntr / len(segments), name="3D Plot")
                x.append(segm.pos_end.get_vec()[0])
                y.append(segm.pos_end.get_vec()[1])
                z.append(segm.pos_end.get_vec()[2])
                vel.append(segm.vel_end.get_abs())

            # create scalar mappable for colormap
            sm = plt.cm.ScalarMappable(cmap=cm.jet, norm=plt.Normalize(vmin=np.min(vel), vmax=np.max(vel)))

        # create line segments
        color_plot = plt.figure().add_subplot(projection="3d")
        interpolated = interp(x, y, z, vel, colvar_spatial_resolution)

        colorline(interpolated.T[0], interpolated.T[1], interpolated.T[2], interpolated.T[3])

        ax = plt.gca()
        ax.set_xlabel("x Position")
        ax.set_ylabel("y Position")
        ax.set_zlabel("z Position")
        plt.title("Printing " + colvar)
        plt.colorbar(sm, label=colvar_label[colvar], shrink=0.6, location="left")

        if filename is not False:
            plt.savefig(filename, dpi=400)
            print("3D Plot saved as ", filename)
        if show:
            plt.show()
            return color_plot
        plt.close()

    def plot_3d_position(
        self, filename="trajectory_3D.png", dpi=400, show=False, colvar_spatial_resolution=1, colvar="Velocity"
    ):
        import matplotlib.pyplot as plt
        from matplotlib import cm
        from mpl_toolkits.mplot3d.art3d import Line3DCollection
        from mpl_toolkits.mplot3d import Axes3D

        colvar_label = {"Velocity": "Velocity in mm/s", "Acceleration": "Acceleration in mm/s^2"}

        def interp(x, y, z, colvar, spatial_resolution=1):
            segm_length = np.linalg.norm([np.ediff1d(x), np.ediff1d(y), np.ediff1d(z)], axis=0)
            segm_colvar_delt = np.greater(np.abs(np.ediff1d(colvar)), 0)
            segm_interpol = np.r_[
                0, np.where(segm_colvar_delt, np.ceil(segm_length / spatial_resolution) + 1, 1)
            ]  # get nmbr of segments for required resolution, dont interpolate if there is no change
            points = np.array([x, y, z, colvar]).T
            points = np.c_[points, segm_interpol]

            # generate intermediate points with set resolution
            old_point = None
            interpolated = np.zeros((1, 4))
            for point in points:
                if old_point is not None:
                    steps = np.linspace(0, 1, int(point[4]), endpoint=True)
                    x_i = np.interp(steps, [0, 1], [old_point[0], point[0]])
                    y_i = np.interp(steps, [0, 1], [old_point[1], point[1]])
                    z_i = np.interp(steps, [0, 1], [old_point[2], point[2]])
                    colvar_i = np.interp(steps, [0, 1], [old_point[3], point[3]])
                    interpolated = np.r_[interpolated, np.array([x_i, y_i, z_i, colvar_i]).T]
                old_point = point
            interpolated = np.delete(interpolated, 0, 0)

            return interpolated

        def w_collection(interpolated):
            points = interpolated[:, :3].reshape(-1, 1, 3)  # get points and reshape
            c = interpolated[:, 3:].reshape(-1)  # color variable

            lsegments = np.concatenate([points[:-1], points[1:]], axis=1)  # create point pairs

            collection = Line3DCollection(lsegments, cmap=cm.jet, norm=plt.Normalize(vmin=np.min(c), vmax=np.max(c)))
            collection.set_array(c)
            return collection

        # get all data for plots
        segments = unpack_blocklist(blocklist=self.blocklist)
        if colvar == "Velocity":
            x, y, z, vel = [], [], [], []
            x.append(segments[0].pos_begin.get_vec()[0])
            y.append(segments[0].pos_begin.get_vec()[1])
            z.append(segments[0].pos_begin.get_vec()[2])
            vel.append(segments[0].vel_begin.get_abs())

            cntr = 0
            for segm in segments:
                cntr += 1
                update_progress(cntr / len(segments), name="3D Plot")
                x.append(segm.pos_end.get_vec()[0])
                y.append(segm.pos_end.get_vec()[1])
                z.append(segm.pos_end.get_vec()[2])
                vel.append(segm.vel_end.get_abs())

            # create scalar mappable for colormap
            sm = plt.cm.ScalarMappable(cmap=cm.jet, norm=plt.Normalize(vmin=np.min(vel), vmax=np.max(vel)))

        # create line segments
        interpolated = interp(x, y, z, vel, colvar_spatial_resolution)

        color_plot = plt.figure()
        # color_plot.add_subplot(projection="3d")
        ax = Axes3D(color_plot)
        collection = w_collection(interpolated=interpolated)
        ax.add_collection3d(collection)

        ax.set_xlabel("x Position")
        ax.set_ylabel("y Position")
        ax.set_zlabel("z Position")

        ax.set_xlim(min(x), max(x))
        ax.set_ylim(min(y), max(y))
        ax.set_zlim(min(z), max(z))

        plt.title("Printing " + colvar)
        plt.colorbar(sm, label=colvar_label[colvar], shrink=0.6, location="left")

        if filename is not False:
            plt.savefig(filename, dpi=400)
            print("3D Plot saved as ", filename)
        if show:
            plt.show()
            return color_plot
        plt.close()

    def plot_3d_mayavi(self, colvar_spatial_resolution: float = 0.5):
        import mayavi.mlab as ma

        # get all data for plots
        segments = unpack_blocklist(blocklist=self.blocklist)
        x, y, z, e, vel = [], [], [], [], []
        x.append(segments[0].pos_begin.get_vec()[0])
        y.append(segments[0].pos_begin.get_vec()[1])
        z.append(segments[0].pos_begin.get_vec()[2])
        e.append(segments[0].pos_begin.get_vec(withExtrusion=True)[3])
        vel.append(segments[0].vel_begin.get_abs())

        figure = ma.figure(figure="Velocity", bgcolor=(0.0, 0.0, 0.0))

        cntr = 0
        extrude = False
        for n, segm in enumerate(segments):
            cntr += 1
            update_progress(cntr / len(segments), name="3D Plot")
            x.append(segm.pos_end.get_vec()[0])
            y.append(segm.pos_end.get_vec()[1])
            z.append(segm.pos_end.get_vec()[2])
            e.append(segm.pos_end.get_vec(withExtrusion=True)[3])
            vel.append(segm.vel_end.get_abs())
            if len(e) >= 2 and e[-1] > e[-2] and extrude is False:
                extrude = True
                x = [x[-2], x[-1]]
                y = [y[-2], y[-1]]
                z = [z[-2], z[-1]]
                e = [e[-2], e[-1]]
                vel = [vel[-2], vel[-1]]
            if len(e) >= 2 and (e[-1] <= e[-2] or n == len(segments)) and extrude:
                x = x[:-1]
                y = y[:-1]
                z = z[:-1]
                e = e[:-1]
                vel  = vel[:-1]
                plot = ma.plot3d(x, y, z, vel, tube_radius=0.2, figure=figure, vmin=0, vmax=35)  # vmax
                x = []
                y = []
                z = []
                vel = []
                e = []
                # x = [x[-1]]
                # y = [y[-1]]
                # z = [z[-1]]
                # vel = [vel[-1]]
                # e = [e[-1]]
                extrude = False

        # show only extrusion

        ma.colorbar(object=plot)
        ma.show()

        # lsegments = np.concatenate([points[:-1], points[1:]], axis=1)  # create point pairs

    def plot_vel(
        self,
        axis=("x", "y", "z", "e"),
        show=False,
        show_plannerblocks=True,
        show_segments=False,
        show_JD=True,
        timesteps="constrained",
        filename="velplot.png",
        dpi=400,
    ):
        import matplotlib.pyplot as plt

        axis_dict = {"x": 0, "y": 1, "z": 2, "e": 3}

        segments = unpack_blocklist(blocklist=self.blocklist)  # unpack

        # timesteps
        if type(timesteps) == int:  # evenly distributed timesteps
            times = np.linspace(0, self.blocklist[-1].get_segments()[-1].t_end, timesteps, endpoint=False)
        elif timesteps == "constrained":  # use segment timepoints as plot constrains
            times = [0]
            for segm in segments:
                times.append(segm.t_end)
        else:
            raise ValueError('Invalid value for Timesteps, either use Integer or "constrained" as argument.')

        # gathering values
        pos = [[], [], [], []]
        vel = [[], [], [], []]
        abs = []  # initialize value arrays
        index_saved = 0
        cntr = 0
        for t in times:
            segm, index_saved = find_current_segm(path=segments, t=t, last_index=index_saved, keep_position=True)
            cntr += 1

            tmp_vel = segm.get_velocity(t=t).get_vec(withExtrusion=True)
            tmp_pos = segm.get_position(t=t).get_vec(withExtrusion=True)
            for ax in axis:
                pos[axis_dict[ax]].append(tmp_pos[axis_dict[ax]])
                vel[axis_dict[ax]].append(tmp_vel[axis_dict[ax]])

            abs.append(np.linalg.norm(tmp_vel[:3]))
            update_progress(cntr / len(times), name="Velocity Plot")

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        # plot JD-Limits
        for blck in self.blocklist:
            # plannerblocks vertical line plot
            if show_plannerblocks:
                ax1.axvline(x=blck.get_segments()[-1].t_end, color="black", lw=0.5)

            # segments vertical line plot
            if show_segments:
                for segm in blck.get_segments():
                    ax1.axvline(x=segm.t_end, color="green", lw=0.25)

            if show_JD:
                # absolute JD Marker
                absJD = np.linalg.norm([blck.JD[0], blck.JD[1], blck.JD[2]])
                ax1.scatter(x=blck.get_segments()[-1].t_end, y=absJD, color="red", marker="x")
                for ax in axis:
                    ax1.scatter(
                        x=blck.get_segments()[-1].t_end, y=blck.JD[axis_dict[ax]], marker="x", color="black", lw=0.5
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
        if filename is not False:
            plt.savefig(filename, dpi=400)
        if show:
            plt.show()
            return fig
        plt.close()

    def trajectory_self_correct(self):
        # self correction
        for block in self.blocklist:
            block.self_correction()

    def get_values(self, t):
        segments = unpack_blocklist(blocklist=self.blocklist)
        segm, self.last_index = find_current_segm(path=segments, t=t, last_index=self.last_index)
        tmp_vel = segm.get_velocity(t=t).get_vec(withExtrusion=True)
        tmp_pos = segm.get_position(t=t).get_vec(withExtrusion=True)

        # scale to required unit system
        tmp_vel = [self.scaling * num for num in tmp_vel]
        tmp_pos = [self.scaling * num for num in tmp_pos]

        return tmp_vel, tmp_pos

    def check_printer(self, printer):
        """
        Method to check the printer Dict for typos or missing parameters.
        """
        printer_keys = ["nozzle_diam", "filament_diam", "velocity", "acceleration", "jerk", "Vx", "Vy", "Vz", "Ve"]

        # Following code could be improved i guess..

        # check if all provided keys are valid
        for key in printer:
            if key not in printer_keys:
                raise ValueError(
                    f'Invalid Key: "{key}" in Printer Dictionary, check for typos. Valid keys are: {printer_keys}'
                )

        # check if every required key is proivded
        for key in printer_keys:
            if key not in printer:
                raise ValueError(
                    f'Key: "{key}" is not provided in Printer Dictionary, check for typos. Required keys are: {printer_keys}'
                )

    def print_summary(self, filename):
        print(
            f""" >> pyGCodeDecode extracted {len(self.states)} states from {filename} and generated {len(self.blocklist)} plannerblocks.\n
            Estimated time to travel all states with provided printer settings is {self.blocklist[-1].get_segments()[-1].t_end} seconds."""
        )

    def refresh(self, new_state_list: List[state] = None):
        if new_state_list is not None:
            self.states = new_state_list

        self.blocklist: List[planner_block] = generate_planner_blocks(states=self.states)
        self.trajectory_self_correct()

    def __init__(self, filename, printer, initial_position=None, output_unit_system: str = "SImm"):
        self.last_index = None  # used to optimize search in segment list
        self.filename = filename

        # set scaling to chosen unit system
        self.available_unit_systems = {"SI": 1e-3, "SImm": 1.0, "inches": 1 / 25.4}
        if output_unit_system in self.available_unit_systems:
            self.output_unit_system = output_unit_system
            self.scaling = self.available_unit_systems[self.output_unit_system]
        else:
            raise ValueError("Chosen unit system is unavailable!")

        # SET INITIAL SETTINGS
        # self.check_printer(printer=printer)

        self.states: List[state] = state_generator(filename=filename, initial_machine_setup=printer)

        self.blocklist: List[planner_block] = generate_planner_blocks(states=self.states)
        self.trajectory_self_correct()

        self.print_summary(filename=filename)
