# -*- coding: utf-8 -*-
from pyGCodeDecode import gcode_interpreter

# import time as t
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

""" INITIAL POSITION:
    None        -> start from zero
    True        -> use first gcode G1 command as initial position
    [x,y,z,e]   -> non zero coordinates for initial position
"""
initial_position = None

# new = gcode_interpreter.simulate(
#     filename=r"example\3D_Benchy\3DBenchy.gcode", printer=anisoprint_A4, initial_position=initial_position
# )

new = gcode_interpreter.simulate(
    filename=r"example\processsimulation\shape.gcode", printer=anisoprint_A4, initial_position=initial_position
)
# example\zugproben\dogbone_direkt_90_layer.gcode


# new.plot_2d_position(show=True,colvar_spatial_resolution=0.1,filename=False)
# new.plot_vel(show=True,filename=False)
# time = t.time()

new.plot_3d_mayavi()

# new.plot_3d_position(filename="3DPlot.png", colvar_spatial_resolution=0.1, show=True)
# print(new.states)

# print(f"Display took: {t.time()-time}s")
# snippet.gcode used with 1018 lines of GCODE--> 3D Plot saved as  3DPlot.png, Display took: 18.40489935874939s
# after: ca. 2.01s
