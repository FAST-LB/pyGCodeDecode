# -*- coding: utf-8 -*-
"""Example usage of pyGCD."""
from pyGCodeDecode import gcode_interpreter

setup = gcode_interpreter.setup(filename=r"example\printer_presets.yaml", printer="prusa_mini")
setup.set_property({"firmware": "klipper"})

# setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.
setup.set_initial_position(89.964, 78.843, 0.0, 0.0)


new = gcode_interpreter.simulate(filename=r"example\dropshape\dropshape.gcode", initial_machine_setup=setup)
# print(new.states)

new.plot_vel(show=True, filename=False)
new.plot_3d_mayavi(extrusion_only=False)
