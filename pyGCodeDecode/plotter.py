"""This module provides functionality for 3D plotting of G-code simulation data using PyVista."""

import os
import pathlib
from typing import Tuple, Union

import numpy as np
import pyvista as pv
from matplotlib.figure import Figure

from pyGCodeDecode.gcode_interpreter import (
    find_current_segment,
    simulation,
    unpack_blocklist,
)
from pyGCodeDecode.helpers import ProgressBar, custom_print


def plot_3d(
    sim: simulation,
    extrusion_only: bool = True,
    scalar_value: str = "velocity",
    screenshot_path: pathlib.Path = None,
    camera_settings: dict = None,
    vtk_path: pathlib.Path = None,
    mesh: pv.MultiBlock = None,
    layer_select: int = None,
    z_scaler: float = None,
    window_size: tuple = (2048, 1536),
    mpl_subplot: bool = False,
    mpl_rcParams: Union[dict, None] = None,
    solid_color: str = "black",
    transparent_background: bool = True,
    parallel_projection: bool = False,
    lighting: bool = True,
    block_colorbar: bool = False,
    extra_plotting: callable = None,  # function to add plotting, args: plotter, mesh
    overwrite_labels: Union[dict, None] = None,
    scalar_value_bounds: Union[Tuple[float, float], None] = None,
    return_type: str = "mesh",  # "mesh" or "image", only available with screenshot_path
) -> pv.MultiBlock:
    """Plot a 3D visualization of G-code simulation data using PyVista.

    Args:
        sim (simulation): The simulation object containing blocklist and segment data.
        extrusion_only (bool, optional): If True, plot only segments where extrusion occurs. Defaults to True.
        scalar_value (str, optional): Scalar value to color the plot. Options: "velocity", "rel_vel_err", "acceleration", or None. Defaults to "velocity".
        screenshot_path (pathlib.Path, optional): If provided, saves a screenshot to this path and disables interactive plotting. Defaults to None.
        camera_settings (dict, optional): Camera settings for the plotter. Keys: "camera_position", "elevation", "azimuth", "roll". Defaults to None.
        vtk_path (pathlib.Path, optional): If provided, saves the mesh as a VTK file to this path. Defaults to None.
        mesh (pv.MultiBlock, optional): Precomputed PyVista mesh to use instead of generating a new one. Defaults to None.
        layer_select (int, optional): If provided, only plot the specified layer. Defaults to None (all layers).
        z_scaler (float, optional): Scaling factor for the z-axis layer squishing (z_scaler = width/height of extrusion). Defaults to None (automatic scaling).
        window_size (tuple, optional): Size of the plot window in pixels. Defaults to (2048, 1536).
        mpl_subplot (bool, optional): If True, use matplotlib for screenshot and colorbar. Defaults to False.
        mpl_rcParams (dict or None, optional): Custom matplotlib rcParams for styling. Defaults to None.
        solid_color (str, optional): Background color for the plot. Defaults to "black".
        transparent_background (bool, optional): If True, screenshot background is transparent. Defaults to True.
        parallel_projection (bool, optional): If True, enables parallel projection in PyVista. Defaults to False.
        lighting (bool, optional): If True, enables lighting in the plot. Defaults to True.
        block_colorbar (bool, optional): If True, removes the scalar colorbar from the plot. Defaults to False.
        extra_plotting (callable, optional): Function to add extra plotting to the PyVista plotter. Signature: (plotter, mesh). Defaults to None.
        overwrite_labels (dict or None, optional): Dictionary to overwrite colorbar labels. Defaults to None.
        scalar_value_bounds (tuple or None, optional): Tuple (min, max) to set scalar colorbar range. Defaults to None.
        return_type (str, optional): Return type, "mesh" or "image". Defaults to "mesh".

    Returns:
        pv.MultiBlock: The PyVista mesh used for plotting.
        or
        np.ndarray: The screenshot image if `screenshot_path` is provided and `return_type` is "image".
    """

    def _safe_screenshot(plotter: pv.Plotter, screenshot_path=None):
        if display_available:
            img = plotter.screenshot(
                transparent_background=transparent_background,
                filename=screenshot_path,
            )
            if screenshot_path is not None:
                custom_print(f"💾 PyVista Screenshot saved to 👉 {screenshot_path}")
        else:
            img = None
            custom_print("PyVista Screenshot can not be created without a display!", lvl=1)
        return img

    colorbar_label = {
        "velocity": [r"$v$ in $\frac{mm}{s}$", "v in mm/s", "viridis"],
        "rel_vel_err": [r"$\epsilon_{\mathrm{loc}}$", "vel. Error", "Reds"],
        "acceleration": [r"$a$ in $\frac{mm}{s^2}$", "a in mm/s^2", "viridis"],
    }
    if overwrite_labels:
        colorbar_label.update(overwrite_labels)

    if layer_select is not None:
        layer_blcklst = [block for block in sim.blocklist if block.state_B.layer == layer_select]
        segments = unpack_blocklist(blocklist=layer_blcklst)
        custom_print("Number of Segments in this Layer: ", len(segments), lvl=3)
    else:
        segments = unpack_blocklist(blocklist=sim.blocklist)

    if z_scaler is None:
        e_width = 0.45
        l_height = 0.2
        z_scaler = e_width / l_height

    if mesh is None:
        mesh = pv.MultiBlock()
        x, y, z, e, scalar = [], [], [], [], []

        bar = ProgressBar(name="3D Plot")
        for n, segm in enumerate(segments):
            bar.update((n + 1) / len(segments))

            if (not extrusion_only) or (segm.is_extruding()):
                if len(x) == 0:
                    pos_begin_vec = segm.pos_begin.get_vec(withExtrusion=True)
                    x.append(pos_begin_vec[0])
                    y.append(pos_begin_vec[1])
                    z.append(pos_begin_vec[2] * z_scaler)
                    e.append(pos_begin_vec[3])

                    if scalar_value is not None:
                        sc = segm.get_result(scalar_value)
                        if hasattr(sc, "__len__"):
                            scalar.append(sc[0])
                        else:
                            scalar.append(sc)

                pos_end_vec = segm.pos_end.get_vec(withExtrusion=True)
                x.append(pos_end_vec[0])
                y.append(pos_end_vec[1])
                z.append(pos_end_vec[2] * z_scaler)
                e.append(pos_end_vec[3])

                if scalar_value is not None:
                    sc = segm.get_result(scalar_value)
                    if hasattr(sc, "__len__"):
                        scalar.append(sc[1])
                    else:
                        scalar.append(sc)

            if (extrusion_only and (len(x) > 0 and not segm.is_extruding())) or (
                len(x) > 0 and n == (len(segments) - 1)
            ):
                points_3d = np.column_stack((x, y, z))
                line = pv.lines_from_points(points_3d)
                if scalar_value is not None:
                    line[scalar_value] = scalar
                tube = line.tube(radius=e_width / 2, n_sides=6)
                mesh.append(tube)
                x, y, z, e, scalar = [], [], [], [], []

        mesh = mesh.combine()

    # check wether a display is available or Windows is used
    if os.name == "nt" or "DISPLAY" in os.environ:
        display_available = True
    else:
        display_available = False

    # saving a screenshot and an interactive plot aren't possible at the same tim
    if screenshot_path is None:
        off_screen = False
    else:
        off_screen = True

    if off_screen:
        p = pv.Plotter(off_screen=off_screen, window_size=window_size)
    else:
        p = pv.Plotter(off_screen=off_screen)

    if parallel_projection:
        p.enable_parallel_projection()

    p.set_scale(zscale=1 / z_scaler)

    if extra_plotting:
        try:
            custom_print("Running extra plotting function", lvl=3)
            extra_plotting(p, mesh)
        except Exception as e:
            custom_print(f"Error in extra plotting function: {e}", lvl=1)

    if scalar_value is not None:
        actor = p.add_mesh(
            mesh,
            scalars=scalar_value,
            smooth_shading=True,
            scalar_bar_args={
                "title": colorbar_label[scalar_value][1],
                "title_font_size": 40,
                "label_font_size": 25,
                "width": 0.05,
                "vertical": True,
                "font_family": "arial",
            },
            cmap=colorbar_label[scalar_value][-1],
            lighting=lighting,
        )
        if scalar_value == "rel_vel_err":
            p.update_scalar_bar_range([0, 1])

        if scalar_value_bounds is not None:
            p.update_scalar_bar_range(scalar_value_bounds)
    else:
        p.set_background(solid_color)
        p.add_mesh(mesh, color=solid_color, smooth_shading=True, lighting=lighting)

    if layer_select is not None:
        p.view_xy()

    if camera_settings is not None:
        p.camera_position = camera_settings["camera_position"]
        if camera_settings.get("elevation", False):
            p.camera.elevation = camera_settings["elevation"]
        if camera_settings.get("azimuth", False):
            p.camera.azimuth = camera_settings["azimuth"]
        if camera_settings.get("roll", False):
            p.camera.roll = camera_settings["roll"]

    if vtk_path is not None:
        mesh.save(filename=vtk_path)
        custom_print(f"💾 VTK saved to 👉 {vtk_path}", lvl=2)

    if screenshot_path is not None:
        custom_print(f"Offscreen plotting, with resolution {p.window_size}", lvl=3)

        if mpl_subplot:
            import matplotlib.pyplot as plt

            if isinstance(mpl_rcParams, dict):
                custom_print(
                    f"Using custom matplotlib rcParams in plot_3d.\n{mpl_rcParams}",
                    lvl=3,
                )
                # print("rcParams:", mpl_rcParams)
                plt.rcParams.update(mpl_rcParams)
                # print("Updated rcParams:", plt.rcParams)

            fig, ax = plt.subplots()

            if scalar_value is not None:
                lut = actor.mapper.lookup_table
                if scalar_value_bounds is None:
                    min_val = lut.GetRange()[0]
                    max_val = lut.GetRange()[1]
                else:
                    min_val, max_val = scalar_value_bounds

                dummy_img = ax.imshow(
                    np.array([[min_val, max_val]]), cmap=colorbar_label[scalar_value][-1], vmin=min_val, vmax=max_val
                )

                p.remove_scalar_bar()

                # image = p.screenshot(transparent_background=True, window_size=window_size)
                image = _safe_screenshot(p)
                # ax.axis("off")
                if not block_colorbar:
                    cbar = fig.colorbar(dummy_img, ax=ax, shrink=0.6)
                    cbar.set_label(colorbar_label[scalar_value][0], fontsize=20)

            else:
                # image = p.screenshot(transparent_background=True)
                image = _safe_screenshot(p)
            ax.axis("off")
            if image is not None:
                ax.imshow(image)
            fig.tight_layout()
            dpi = window_size[1] / fig.get_size_inches()[1]
            fig.savefig(screenshot_path, dpi=dpi, transparent=transparent_background)  # bbox_inches="tight",

            custom_print(f"💾 MPL Screenshot saved to 👉{screenshot_path}")
        else:
            if block_colorbar:
                p.remove_scalar_bar()
            image = _safe_screenshot(p, screenshot_path)

        if return_type == "image":
            return image
        return mesh

    if not off_screen and display_available:
        p.show()

    return mesh


def plot_2d(
    sim: simulation,
    filepath: pathlib.Path = pathlib.Path("trajectory_2D.png"),
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

    colvar_label = {
        "Velocity": "Velocity in mm/s",
        "Acceleration": "Acceleration in mm/s^2",
    }

    def _interp_2D(x, y, cvar, spatial_resolution=1):
        segm_length = np.linalg.norm([np.ediff1d(x), np.ediff1d(y)], axis=0)
        segm_cvar_delt = np.greater(np.abs(np.ediff1d(cvar)), 0)
        segm_interpol = np.r_[
            0,
            np.where(segm_cvar_delt, np.ceil(segm_length / spatial_resolution) + 1, 1),
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

    segments = unpack_blocklist(blocklist=sim.blocklist)
    if colvar == "Velocity":
        # get all planned trajectory vertices + color variable
        x, y, cvar = [], [], []
        x.append(segments[0].pos_begin.get_vec()[0])
        y.append(segments[0].pos_begin.get_vec()[1])
        cvar.append(segments[0].vel_begin.get_norm())

        bar = ProgressBar(name="2D Plot Lines")
        for i, segm in enumerate(segments):
            bar.update((i + 1) / len(segments))
            x.append(segm.pos_end.get_vec()[0])
            y.append(segm.pos_end.get_vec()[1])
            cvar.append(segm.vel_end.get_norm())

        # interpolate values for smooth coloring
        interpolated = _interp_2D(x, y, cvar, spatial_resolution=colvar_spatial_resolution)

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
            bar.update((i + 1) / len(segments))
            x.append(segm.pos_end.get_vec()[0])
            y.append(segm.pos_end.get_vec()[1])
        fig = plt.subplot()
        fig.plot(x, y, color="black")

    if show_points:
        for i, block in enumerate(sim.blocklist):
            bar.update(i / len(sim.blocklist))
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
    if filepath is not False:
        plt.savefig(filepath, dpi=dpi)
        custom_print(f"💾 2D Plot saved 👉 {filepath}")
    if show:
        plt.show()
        return fig
    plt.close()


def plot_vel(
    sim: simulation,
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
        time_steps: (int or string, default = "constrained") number of time steps or constrain plot
            vertices to segment vertices
        filepath: (Path, default = None) save fig as image if filepath is provided
        dpi: (int, default = 400) select dpi

    Returns:
    (optionally)
        fig: (figure)
    """
    import matplotlib.pyplot as plt

    axis_dict = {"x": 0, "y": 1, "z": 2, "e": 3}

    segments = unpack_blocklist(blocklist=sim.blocklist)  # unpack

    # time steps
    if type(time_steps) is int:  # evenly distributed time steps
        times = np.linspace(
            0,
            sim.blocklist[-1].get_segments()[-1].t_end,
            time_steps,
            endpoint=False,
        )
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
    bar = ProgressBar(name="Velocity Plot")

    for i, t in enumerate(times):
        segm, index_saved = find_current_segment(path=segments, t=t, last_index=index_saved, keep_position=True)

        tmp_vel = segm.get_velocity(t=t).get_vec(withExtrusion=True)
        tmp_pos = segm.get_position(t=t).get_vec(withExtrusion=True)
        for ax in axis:
            pos[axis_dict[ax]].append(tmp_pos[axis_dict[ax]])
            vel[axis_dict[ax]].append(tmp_vel[axis_dict[ax]])

        abs.append(np.linalg.norm(tmp_vel[:3]))
        bar.update((i + 1) / len(times))

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # plot JD-Limits
    for block in sim.blocklist:
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
                    x=block.get_segments()[-1].t_end,
                    y=block.JD[axis_dict[ax]],
                    marker="x",
                    color="black",
                    lw=0.5,
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
