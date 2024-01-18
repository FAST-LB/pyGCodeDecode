# -*- coding: utf-8 -*-
"""Example usage of pyGCD in the Restore Project."""
import time

from pyGCodeDecode import abaqus_file_generator, gcode_interpreter  # noqa F401

printfile = r"example\validation\aniso\JDJERK_1_5_7_10_15_20_30_drop.gcode"

setup = gcode_interpreter.setup(filename=r"./pygcodedecode/data/default_printer_presets.yaml")  # load setup
setup.select_printer("anisoprint_a4")  # Select printer from preset.
setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.

setup.set_property({"firmware": "MKA"})
start_time = time.time()
simulation = gcode_interpreter.simulate(filename=printfile, initial_machine_setup=setup)  # Simulate the gcode.
print("---Simulation took %s seconds ---" % (time.time() - start_time))
# simulation.plot_vel()
# simulation.plot_3d(extrusion_only=False)
setup.set_property({"firmware": "marlin_jd"})
start_time = time.time()
simulation = gcode_interpreter.simulate(filename=printfile, initial_machine_setup=setup)  # Simulate the gcode.
print("---Simulation took %s seconds ---" % (time.time() - start_time))
# simulation.plot_vel()

setup.set_property({"firmware": "marlin_jerk"})
start_time = time.time()
simulation = gcode_interpreter.simulate(filename=printfile, initial_machine_setup=setup)  # Simulate the gcode.
print("---Simulation took %s seconds ---" % (time.time() - start_time))
# simulation.plot_vel()

setup.set_property({"firmware": "marlin_klipper"})
start_time = time.time()
simulation = gcode_interpreter.simulate(filename=printfile, initial_machine_setup=setup)  # Simulate the gcode.
print("---Simulation took %s seconds ---" % (time.time() - start_time))
# simulation.plot_vel()
