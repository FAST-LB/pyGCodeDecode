# pyGCodeDecode



# What is this repository for?
tbd

# Install pyGCodeDecode
### Python 3
Set up a virtual environment named `virtual_env` using the `virtualenv` package

        python -m pip install .
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

Verify the installation via `pip list` and look for `pygcodedecode`.

### Python 2 (abaqus python)

1. Make sure you have installed pip for Abaqus python. If you do not have it, do the following:

        curl -s https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
        abq<version> python get-pip.py --no-warn-script-location

2. Install the package via pip in the root directory of this repository:

        abq<version> python -m pip install .

3. Verify the package installation via `abaqus python -m pip list` and look for `pygcodedecode`. 


# Workflow

tbd
