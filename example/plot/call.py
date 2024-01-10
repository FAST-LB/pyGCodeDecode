# -*- coding: utf-8 -*-
"""Example usage of pyGCD plotting function."""
from pyGCodeDecode import gcode_interpreter

setup = gcode_interpreter.setup(filename=r"./pygcodedecode/data/default_printer_presets.yaml", printer="prusa_mini")
setup.set_property({"firmware": "klipper"})

# setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.


new = gcode_interpreter.simulate(filename=r"example\plot\part.gcode", initial_machine_setup=setup)

new.plot_3d()
