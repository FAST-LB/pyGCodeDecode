# -*- coding: utf-8 -*-
from pyGCodeDecode import gcode_interpreter

# Fictional Printer Preset
fictional_printer = {
    # general properties
    "nozzle_diam": 0.4,
    "filament_diam": 1.75,
    # default settings
    "p_vel": 35,
    "p_acc": 200,
    "jerk": 2,
    # axis max speeds
    "vX": 60,
    "vY": 60,
    "vZ": 40,
    "vE": 25,
}

anisoprint_A4 = {
    # general properties
    "nozzle_diam": 0.4,
    "filament_diam": 1.75,
    # default settings
    "p_vel": 35,
    "p_acc": 200,
    "jerk": 10,
    # axis max speeds
    "vX": 180,
    "vY": 180,
    "vZ": 30,
    "vE": 33,
}


setup = gcode_interpreter.setup(filename=r"example\printer_presets.yaml")
setup.select_printer("anisoprint_A4")
setup.set_initial_position({"x": 0, "y": 0, "z": 0})
print(setup.get_dict())

new = gcode_interpreter.simulate(filename=r"example\test.gcode", initial_machine_setup=anisoprint_A4)

# new.plot_vel(show=True, filename=False)
# new.save_summary()
# new.plot_3d_mayavi()
