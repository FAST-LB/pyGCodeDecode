"""The CLI for the pyGCodeDecode package."""

import argparse
import importlib.resources
import pathlib

from pyGCodeDecode import __version__
from pyGCodeDecode.examples.benchy import benchy_example
from pyGCodeDecode.examples.brace import brace_example
from pyGCodeDecode.gcode_interpreter import setup, simulation
from pyGCodeDecode.tools import save_layer_metrics


def _run_example(args: argparse.Namespace):
    """Generate a plot from a GCode file."""
    if args.example == "brace":
        brace_example()
    if args.example == "benchy":
        benchy_example()


def _plot(args: argparse.Namespace):
    """Generate a plot from a GCode file."""

    def _find_gcode_file(specified_path: pathlib.Path | None) -> pathlib.Path:
        """Check if the G-code file exists and try to find one in the cwd if not specified."""
        if specified_path is not None and specified_path.is_file():
            g_code_file = specified_path
        elif specified_path is not None:
            print(f"❌ The specified G-code:\n{specified_path.resolve()}\nis not valid.\n" "🛑 Exiting the program.")
            exit()
        else:
            print("⚠️ No G-code file specified. Looking for a G-code file in the current directory... 👀")
            files_list = list(pathlib.Path.cwd().glob("*.gcode"))
            if files_list.__len__() == 0:
                print("❌ No G-code file found in the current directory.\n" "🛑 Exiting the program.")
                exit()
            elif files_list.__len__() == 1:
                g_code_file = files_list[0]
            else:
                print("❌ Multiple G-code files found in the current directory:")
                for file in files_list:
                    print(f"    - {file.resolve()}")
                print("🛑 Exiting the program.")
                exit()

        print(f"✅ Using the G-code file:\n{g_code_file.resolve()}")
        return g_code_file

    def _get_presets_file(presets_file: pathlib.Path | None) -> pathlib.Path:
        """Get the machine setup from the presets file."""
        if presets_file is None:
            print("⚠️ No presets file specified. Using the default presets shipped with pyGCD.")
            presets_file = importlib.resources.files("pyGCodeDecode").joinpath("data/default_printer_presets.yaml")
        elif not presets_file.is_file():
            print(
                f"❌ The specified presets file:\n{presets_file.resolve()}\nis not valid.\n" "🛑 Exiting the program."
            )
            exit()
        else:
            print(f"✅ Using the presets file:\n{presets_file.resolve()}")

        return presets_file

    def _get_out_dir(out_dir: pathlib.Path | None, g_code_file: pathlib.Path) -> pathlib.Path:
        """Get the output directory for the plot."""
        if out_dir is None:
            answer = ""
            while answer.lower() not in ("y", "yes", "n", "no"):
                answer = input(
                    "⚠️ No output directory specified! Do you want to create one in the current working directory?"
                    "\nOtherwise no outputs will be saved!"
                    "\nYou must answer with yes (y) or no (n)!\n"
                )

            if answer.lower() in ["n", "no"]:
                print("⚠️ Not creating any output files.")
                return None
            elif answer.lower() in ["y", "yes"]:
                out_dir = pathlib.Path.cwd() / f"output_{g_code_file.stem}"

        print(f"✅ Using the output directory:\n{out_dir.resolve()}")
        return out_dir

    g_code_file = _find_gcode_file(args.gcode)
    out_dir = _get_out_dir(args.out_dir, g_code_file)
    presets_file = _get_presets_file(args.presets)

    if args.printer_name is not None:
        printer_name = args.printer_name
        print(f"✅ Using the printer: {printer_name}")
    else:
        print("⚠️ No printer specified. Using the default printer Anisoprint A4.")
        printer_name = "anisoprint_a4"

    # setting up the printer
    printer_setup = setup(
        presets_file=presets_file,
        printer=printer_name,
        layer_cue=args.layer_queue,
    )

    # running the simulation by creating a simulation object
    sim = simulation(
        gcode_path=g_code_file,
        initial_machine_setup=printer_setup,
    )

    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        # save a short summary of the simulation
        sim.save_summary(filepath=out_dir / f"{g_code_file.stem}_summary.yaml")
        # print a file containing some metrics for each layer
        save_layer_metrics(
            simulation=sim,
            filepath=out_dir / f"{g_code_file.stem}_layer_metrics.csv",
            locale="en_US.utf8",
            delimiter=",",
        )
        # create a 3D-plot and save a VTK as well as a screenshot
        mesh = sim.plot_3d(
            extrusion_only=True,
            screenshot_path=out_dir / f"{g_code_file.stem}.png",
            vtk_path=out_dir / f"{g_code_file.stem}.vtk",
        )
    else:
        mesh = None

    # create an interactive 3D-plot
    sim.plot_3d(mesh=mesh)


def _main():
    """Entry point function for the command-line interface (CLI)."""
    global_parser = argparse.ArgumentParser(
        prog="pygcd",
        description=f"{__doc__} You are running version {__version__}.",
    )
    global_parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
    )

    # subparsers vor various functions
    subparsers = global_parser.add_subparsers(
        title="subcommands",
        description="Functions accessible via this CLI.",
    )

    # subparser to run examples
    example_parser = subparsers.add_parser("run_example", help="Run one of the provided examples.")
    example_parser.add_argument(
        "example",
        help="The name of the example to run.",
        choices=["brace", "benchy"],
    )
    example_parser.set_defaults(func=_run_example)

    # subparser to plot a GCode file
    plot_parser = subparsers.add_parser("plot", help="Generate a plot from a GCode file.")
    plot_parser.set_defaults(func=_plot)

    plot_parser.add_argument(
        "-g",
        "--gcode",
        action="store",
        nargs="?",
        help="The path to the G-code file. Looks for a G-code file in the current directory if not specified.",
        default=None,
        type=pathlib.Path,
        metavar="<PATH>",
    )
    plot_parser.add_argument(
        "-p",
        "--presets",
        action="store",
        help="The path to the printer presets file. Default printers can be used if not specified.",
        default=None,
        type=pathlib.Path,
        metavar="<PATH>",
    )
    plot_parser.add_argument(
        "-pn",
        "--printer_name",
        action="store",
        help="The name of the printer as specified in the presets file or the defaults if no presets were specified",
        default=None,
        type=str,
        metavar="<NAME>",
    )
    plot_parser.add_argument(
        "-o",
        "--out_dir",
        action="store",
        help="The path to the output directory.",
        default=None,
        type=pathlib.Path,
        metavar="<PATH>",
    )
    plot_parser.add_argument(
        "-lq",
        "--layer_queue",
        action="store",
        help="The queue indicating a layer switch in the GCode.",
        default=None,
        type=str,
        metavar="<QUEUE>",
    )

    # parse the arguments
    args = global_parser.parse_args()

    # call the respective function specified by the subparser
    if hasattr(args, "func"):
        args.func(args)
    else:
        global_parser.print_help()
