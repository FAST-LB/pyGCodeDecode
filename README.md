# pyGCodeDecode

![LOGO](https://media.githubusercontent.com/media/FAST-LB/pyGCodeDecode/main/logo.jpg)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![tests](https://github.com/FAST-LB/pyGCodeDecode/workflows/Tests/badge.svg)](https://github.com/FAST-LB/pyGCodeDecode/actions/workflows/tests.yaml)
[![GitHub Release](https://img.shields.io/github/release/FAST-LB/pyGCodeDecode.svg?style=flat)](https://github.com/FAST-LB/pyGCodeDecode/releases)

[![Python](https://img.shields.io/pypi/pyversions/pygcodedecode.svg)]()
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)
[![isort](https://img.shields.io/badge/isort-blue)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## What is this repository for?
![comparison](https://media.githubusercontent.com/media/FAST-LB/pyGCodeDecode/main/paper/comparison.png)

This package reads the target trajectory and commands for changing firmware settings from a GCode file. Furthermore it simulates a motion planner with acceleration and jerk / junction control. The simulation result describes the nozzle and extrusion axis position and velocity at every point in time. Notably, this method does try to simulate the real printer movements at a higher accuracy than assuming constant velocity. A comparison between the simulated accceleration approach and a constant velocity assumption is illustrated above. Constant velocity is usually also pictured in slicer previews and other GCode analyzing tools such as <span style="font-variant:small-caps;">Prusa Slicer</span> [1][prusa_slicer] or <span style="font-variant:small-caps;">gCodeViewer</span> [2][gcodeviewer]. The more accurate modeling is only achieved by replicating grbl and derivative firmwares specific movement planner solutions, such as Junction Deviation as an interpretation for Jerk. This python package can be used to generate time dependent boundary conditions from a GCode file, needed in additive manufacturing simulations such as Fused Filament Fabrication. With implemented 3D plotting functions, it also can be useful as a GCode analyzer tool, to visualize local velocities to gain better process understanding.

The package is modularized to enable quick modification and extension of all features.


## Install pyGCodeDecode

It is recommended that you first create a virtual Python-environment, e.g. using the `venv`-module built into Python. You can  clone the repository and run

        pip install .

from inside the root directory. Alternatively you can simply install from PyPI:

        pip install pyGCodeDecode

If you plan to contribute to the development, install in development mode and with the additional dependencies:

        pip install -e .[DEVELOPER]

You may want to verify the installation and version. Inside your environment, just run:

        python -c "import pyGCodeDecode
        print(pyGCodeDecode.__version__)"

This should return the correct version.

<!-- ### Installing in `abaqus` python (2.7)

1. Make sure you have installed pip for Abaqus python. If you do not have it, do the following:

        curl -s https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
        abq<version> python get-pip.py --no-warn-script-location

2. Install the package via pip in the root directory of this repository:

        abq<version> python -m pip install .

3. Verify the package installation via `abaqus python -m pip list` and look for `pyGCodeDecode`. -->


## Workflow
Example simulations are provided in [./examples/](https://github.com/FAST-LB/pyGCodeDecode/blob/main/examples/) and can be modified to suit your needs. If you want to start from scratch, the following instructions will help you setup & run a simulation.

### Define your printer defaults in a `.yaml` file

For example, the definition may look like this (also see [./pyGCodeDecode/data/default_printer_presets.yaml](https://github.com/FAST-LB/pyGCodeDecode/blob/main/pyGCodeDecode/data/default_printer_presets.yaml)):

        prusa_mini:
                # general properties
                nozzle_diam: 0.4
                filament_diam: 1.75
                # default settings
                p_vel: 35
                p_acc: 1250
                jerk: 8
                # axis max speeds
                vX: 180
                vY: 180
                vZ: 12
                vE: 80
                firmware: marlin_jerk
The default settings usually are machine specific and often can be read from the printer using a Serial Connection with a GCode command. you can use `M503` for Marlin, Prusa and some other firmwares.

### Use pyGCD to run a GCode Simulation

An easy way to use pyGCD is by creating a .py file to set up and run the simulation.

1. Import the package and modules you want to use:

        from pyGCodeDecode import gcode_interpreter

1. Load your setup `.yaml` file through:

        setup = gcode_interpreter.setup(filename=r"e./pygcodedecode/data/default_printer_presets.yaml")

1. Select your printer from the setup by name:

        setup.select_printer("prusa_mini")

1. You can optionally set or modify custom properties after loading the setup:

        setup.set_property({"layer_cue": "LAYER_CHANGE"})

1. Finally, run the simulation by providing a `GCode` and passing the setup defined before:

        simulation = gcode_interpreter.simulation(filename=r"example\example.gcode", initial_machine_setup=setup)


### Access the Results

Now `simulation` contains the simulation results, you can access it through the instance.

Get the individual axis values (position and velocity) at a certain time (e.g. after 2.6 s) to use it in further simulation by:

        simulation.get_values(t=2.6)

You can visualize the GCode by plotting it in 3D:

        simulation.plot_3d()

pyGCD can also be used to create files defining an event series for ABAQUS simulations:

        generate_abaqus_event_series(
                simulation=simulation,
                filpath="path/to/event_series.csv"
        )

For more in depth information have a look into the [documentation](https://github.com/FAST-LB/pyGCodeDecode/blob/main/doc.md).


## Supported GCode commands

Fully supported commands:

        "G0": {"E": None, "X": None, "Y": None, "Z": None, "F": None},  # non Extrusion Move
        "G1": {"E": None, "X": None, "Y": None, "Z": None, "F": None},  # Extrusion Move
        "G4": {"P": None, "S": None},  # Dwell
        "M82": None,  # E Absolute
        "M83": None,  # E Relative
        "G20": None,  # Inches
        "G21": None,  # Milimeters
        "G90": None,  # Absolute Positioning
        "G91": None,  # Relative Positioning
        "G92": {"E": None, "X": None, "Y": None, "Z": None},  # Set Position
        ";": None,  # Comment


Only partially supported commands:

        "M203": {"E": None, "X": None, "Y": None, "Z": None},  # Max Feedrate *read only
        "M204": {"P": None, "R": None, "S": None, "T": None},  # Starting Acceleration *P only
        "M205": {"E": None, "J": None, "S": None, "X": None, "Y": None, "Z": None},  # Advanced Settings *X only
        "G10": {"S": None}, *read only
        "G11": None, *read only

Known unsupported commands that may cause issues:

        "G2" / "G3: {-} Arc/Circle move, please disable this command in your Slicer settings
        

[prusa_slicer]: <https://github.com/prusa3d/PrusaSlicer> "Prusa Slicer"

[gcodeviewer]: <https://gcode.ws/> "gCodeViewer"