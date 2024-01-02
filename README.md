# pyGCodeDecode

![LOGO](./logo.jpg?raw=true "pyGCD")

[![Python](https://img.shields.io/badge/-Python-4B8BBE?&logo=Python&logoColor=fff)]()
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)
[![isort](https://img.shields.io/badge/isort-blue)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## What is this repository for?

This package reads the target trajectory and commands for changing firmware settings from a GCode file. Furthermore it simulates a motion planner with acceleration and jerk / junction control. The simulation result describes the nozzle and extrusion axis position and velocity at every point in time. Notably, this method does try to simulate the real printer movements at a higher accuracy than assuming constant velocity. This is achieved by replicating grbl and derivative firmwares specific movement planner solutions, such as Junction Deviation as an interpretation for Jerk. This python package can be used to generate time dependent boundary conditions from a GCode file, needed in additive manufacturing simulations such as Fused Filament Fabrication. With implemented 3D plotting functions, it also can be useful as a GCode analyzer tool, to visualize local velocities to gain better process understanding.

The package is highly modularized to enable quick modification and extension of all features.

PyGCodeDecode is currently used in:

- PySPH FFF
- Abaqus Event Series Generator

## Install pyGCodeDecode

### Installing in Python 3

<!-- Set up a virtual environment named `virtual_env` using the `virtualenv` package

        python -m pip install .
        virtualenv virtual_env
        python -m venv virtual_env

If this does not work, you have to install `virtualenv` first (maybe administrator rights are necessary)

        pip install virtualenv

Activate the virtual environment with

        .\virtual_env\Scripts\activate.bat -->

Now install the repository as a python package in the root directory of this repository using:

        pip install .

If you want to contribute to the development, install in development mode with

        pip install -e .[DEVELOPER]

Verify the installation via `pip list` and look for `pyGCodeDecode`.

<!-- ### Installing in `abaqus` python (2.7)

1. Make sure you have installed pip for Abaqus python. If you do not have it, do the following:

        curl -s https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
        abq<version> python get-pip.py --no-warn-script-location

2. Install the package via pip in the root directory of this repository:

        abq<version> python -m pip install .

3. Verify the package installation via `abaqus python -m pip list` and look for `pyGCodeDecode`. -->

## Supported GCode commands

fully supported:

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


partially supported:

        "M203": {"E": None, "X": None, "Y": None, "Z": None},  # Max Feedrate *read only
        "M204": {"P": None, "R": None, "S": None, "T": None},  # Starting Acceleration *P only
        "M205": {"E": None, "J": None, "S": None, "X": None, "Y": None, "Z": None},  # Advanced Settings *X only
        "G10": {"S": None}, *read only
        "G11": None, *read only

## Workflow

### define a printer with default parameters in a .yaml

example definition (also see in [/example/printer_presets.yaml](example/printer_presets.yaml)):

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

### create a runfile

Create a .py file to call the simulation. (also see in [/example/call.py](pyGCodeDecode/example/call.py))
Import the package:

        from pyGCodeDecode import gcode_interpreter

load the setup with:

        setup = gcode_interpreter.setup(filename=r"example\printer_presets.yaml")

select a printer:

        setup.select_printer("prusa_mini")

(optional) set custom properties:

        setup.set_property({"layer_cue": "LAYER_CHANGE"})

run the simulation:

        simulation = gcode_interpreter.simulate(filename=r"example\example.gcode", initial_machine_setup=setup)

use the simulation obj from now on, to retrieve information or use plot functions:

get axis values at a certain time (e.g. 2.6 s):

        simulation.get_values(t=2.6)


plot in 3D:

        simulation.plot_3d_mayavi()

for more in depth information have a look into the [documentation](doc.md)
