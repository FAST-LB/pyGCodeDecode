# pyGCodeDecode

![LOGO](pyGCodeDecode/logo.jpg?raw=true "pyGCD")

[![Latest Release](https://git.scc.kit.edu/FAST-LT/additive-manufacturing/pygcodedecode/-/badges/release.svg)](https://git.scc.kit.edu/FAST-LT/additive-manufacturing/pygcodedecode/-/releases)
[![pipeline status](https://git.scc.kit.edu/FAST-LT/additive-manufacturing/pygcodedecode/badges/main/pipeline.svg)](https://git.scc.kit.edu/FAST-LT/additive-manufacturing/pygcodedecode/-/pipelines?scope=branches)
![coverage report](https://git.scc.kit.edu/FAST-LT/additive-manufacturing/pygcodedecode/badges/main/coverage.svg)

![Python](https://img.shields.io/badge/-Python-4B8BBE?&logo=Python&logoColor=fff)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![isort](https://img.shields.io/badge/isort-blue)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## What is this repository for?

This python package is used to generate time dependent boundary conditions from a .gcode file, needed in additive manufacturing simulations such as Fused Filament Fabrication. This package reads the trajectory as well as some relevant constantly changing printing settings. The output describes the nozzle position and velocity at every point in time. Notably, this method does try to simulate the real printer movements at a higher accuracy. This is achieved by replicating grbl and derivative firmwares specific movement planner solutions, such as Junction Deviation as an interpretation for Jerk.

PyGCodeDecode is currently used in:

- PySPH FFF
- Abaqus Event Series Generator

## Install pyGCodeDecode

### Installing in Python 3

Set up a virtual environment named `virtual_env` using the `virtualenv` package

        python -m pip install .
        virtualenv virtual_env
        python -m venv virtual_env

If this does not work, you have to install `virtualenv` first (maybe administrator rights are necessary)

        pip install virtualenv

Activate the virtual environment with

        .\virtual_env\Scripts\activate.bat

Now install the repository as a python package in the root directory of this repository using:

        pip install .

If you want to contribute to the development, install in development mode with

        pip install -e .

Verify the installation via `pip list` and look for `pyGCodeDecode`.

### Installing in `abaqus` python (2.7)

1. Make sure you have installed pip for Abaqus python. If you do not have it, do the following:

        curl -s https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
        abq<version> python get-pip.py --no-warn-script-location

2. Install the package via pip in the root directory of this repository:

        abq<version> python -m pip install .

3. Verify the package installation via `abaqus python -m pip list` and look for `pyGCodeDecode`.

## Supported GCode commands

fully supported:

- G1 X** Y** Z** E** F**
- M82 (absolute extruder mode)
- M83 (relative extruder mode)

partially supported:

- M203 (max axis speed)         *read only
- M204 P** (acceleration)       *P only
- M205 X** (jerk)               *X only

## Workflow

tbd
