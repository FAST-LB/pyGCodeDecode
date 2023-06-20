# -*- coding: utf-8 -*-
from pyGCodeDecode import gcode_interpreter

setup = gcode_interpreter.setup(filename=r"example\printer_presets.yaml", printer="anisoprint_A4")
setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa layer change cue.

new = gcode_interpreter.simulate(filename=r"example\test.gcode", initial_machine_setup=setup)

print(new.states)

# new.plot_vel(show=True, filename=False)
# new.save_summary()

# new.plot_vel(show=True, filename=False)
new.plot_3d_mayavi(extrusion_only=True)
