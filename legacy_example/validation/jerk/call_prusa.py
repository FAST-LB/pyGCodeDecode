# -*- coding: utf-8 -*-
"""Example usage of pyGCD in the Restore Project."""
import time

from pyGCodeDecode import abaqus_file_generator, gcode_interpreter  # noqa F401
from pyGCodeDecode.tools import print_layertimes

start_time = time.time()

setup = gcode_interpreter.setup(presets_file=r"./pygcodedecode/data/default_printer_presets.yaml")  # load setup
setup.select_printer("prusa_mini")  # Select printer from preset.
setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.

setup.set_property({"firmware": "marlin_jerk"})
simulation = gcode_interpreter.simulation(
    filename=r"example\validation\jerk\JDJERK_1_5_7_10_15_20_30.gcode", initial_machine_setup=setup
)  # Simulate the gcode.

print("---Simulation took %s seconds ---" % (time.time() - start_time))
print_layertimes(simulation=simulation, filename="./example/validation/jerk/layertime.csv")

simulation.plot_vel()
