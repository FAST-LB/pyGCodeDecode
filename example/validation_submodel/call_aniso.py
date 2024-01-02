# -*- coding: utf-8 -*-
"""Example usage of pyGCD in a validation project."""
import time

from pyGCodeDecode import abaqus_file_generator as afg
from pyGCodeDecode import gcode_interpreter  # noqa F401
from pyGCodeDecode.tools import print_layertimes

# ---SETUP--- #
printfile = r"example\validation_submodel\submodell_validierung.gcode"
setup = gcode_interpreter.setup(filename=r"./pygcodedecode/data/default_printer_presets.yaml")  # load setup
setup.select_printer("anisoprint_a4")  # Select printer from preset.
setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.

# ---SIMULATION--- #
start_time = time.time()
simulation = gcode_interpreter.simulate(filename=printfile, initial_machine_setup=setup)  # Simulate the gcode.
print("---Simulation took %s seconds ---" % (time.time() - start_time))

# ---RESULTS--- #
afg.generate_abaqus_events(simulation=simulation, filename="example/validation_submodel/time_series.inp")

print_layertimes(simulation=simulation, filename="example/validation_submodel/layertime_aniso.csv")

# simulation.plot_vel()
simulation.plot_3d_mayavi()
