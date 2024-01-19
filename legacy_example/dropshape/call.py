# -*- coding: utf-8 -*-
"""Example usage of pyGCD."""
from pyGCodeDecode import gcode_interpreter

setup = gcode_interpreter.setup(presets_file=r"./pygcodedecode/data/default_printer_presets.yaml", printer="prusa_mini")
setup.set_property({"firmware": "klipper"})

# setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.
setup.set_initial_position((89.964, 78.843, 0.0, 0.0))


new = gcode_interpreter.simulation(filename=r"example\dropshape\dropshape.gcode", initial_machine_setup=setup)
# print(new.states)

new.plot_vel(show=True)
new.plot_3d(extrusion_only=False)
