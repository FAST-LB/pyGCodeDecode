# -*- coding: utf-8 -*-
"""Example usage of pyGCD in the Restore Project."""
import time

from pyGCodeDecode import gcode_interpreter  # noqa F401
from pyGCodeDecode.tools import print_layertimes

start_time = time.time()

setup = gcode_interpreter.setup(filename=r"example\printer_presets.yaml")  # load setup
setup.select_printer("prusa_mini")  # Select printer from preset.
setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.

simulation = gcode_interpreter.simulate(
    filename=r"example\validation\geom\two_slice.gcode", initial_machine_setup=setup
)  # Simulate the gcode.

print("---Simulation took %s seconds ---" % (time.time() - start_time))
print_layertimes(simulation=simulation, filename="example/validation/geom/layertime.csv")

# simulation.plot_vel()
# simulation.plot_3d_mayavi(extrusion_only=False)
