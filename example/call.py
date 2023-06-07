# -*- coding: utf-8 -*-
from pyGCodeDecode import gcode_interpreter

setup = gcode_interpreter.setup(filename=r"example\printer_presets.yaml", printer="anisoprint_A4")
print(setup.get_dict())

new = gcode_interpreter.simulate(filename=r"example\test.gcode", initial_machine_setup=setup)
print(new.states)
# new.plot_vel(show=True, filename=False)
# new.save_summary()
new.plot_3d_mayavi(extrusion_only=False)
