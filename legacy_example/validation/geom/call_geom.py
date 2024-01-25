# -*- coding: utf-8 -*-
"""Example usage of pyGCD in the Restore Project."""
import time

from pyGCodeDecode import gcode_interpreter  # noqa F401
from pyGCodeDecode.tools import print_layer_metrics

start_time = time.time()

setup = gcode_interpreter.setup(presets_file=r"./pygcodedecode/data/default_printer_presets.yaml")  # load setup
setup.select_printer("prusa_mini")  # Select printer from preset.
setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.

simulation = gcode_interpreter.simulation(
    gcode_path=r"example\validation\geom\two_slice.gcode", initial_machine_setup=setup
)  # Simulate the gcode.

print("---Simulation took %s seconds ---" % (time.time() - start_time))
print_layer_metrics(simulation=simulation, filepath="example/validation/geom/layertime.csv")

# simulation.plot_vel()
# simulation.plot_3d(extrusion_only=False)
