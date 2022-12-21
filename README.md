# pyGCodeDecode



# What is this repository for?
Repository contains tools to generate three-dimensional computer graphics of initial plastificates containing the mesh information alongside the fiber orientation state.
Supported output formats are *.udm (moldflow) and *.vtk.

# Install pymoldcharge
### Python 3
Set up a virtual environment named `virtual_env` using the `virtualenv` package

    cd initialcharge
    virtualenv virtual_env
    python -m venv virtual_env

If this does not work, you have to install `virtualenv` first (maybe administrator rights are necessary)

    pip install virtualenv

Activate the virtual environment with

    .\virtual_env\Scripts\activate.bat

Now install the repository as a python package using

    pip install .

If you want to contribute to the development, install in development mode with

    pip install -e .

Verify the installation via `pip list` and look for `pymoldcharge`.

### Python 2 (abaqus python)
First, change the "install_requirements" in `setup.py` for Python 2.
Install as a package in developer mode in python

    cd gitrepository
    abaqus python setup.py develop

Verify the package installation via `abaqus python -m pip list` and look for `pymoldcharge`. **Note:**: Recommended to install [fibermap](https://git.scc.kit.edu/FAST-LT/fibermap), which automatically installs `pymaplib` and the forked `meshio` packages in abaqus python.

If `pip` is not installed in abaqus python, do

    curl -s https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
    abaqus python get-pip.py

# Workflow
