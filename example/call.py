from pyGCodeDecode import gcode_interpreter as gi

###Fictional Printer Preset
fictional_printer = {
    #general properties
    "nozzle_diam"   :   0.4,
    "filament_diam" :   1.75,
    
    #settings
    "velocity"      :   35,
    "acceleration"  :   20,
    "jerk"          :   2,
    
    #axis max speeds
    "Vx"            :   60,
    "Vy"            :   60,
    "Vz"            :   40,
    "Ve"            :   25
    }

""" INITIAL POSITION:
    None        -> start from zero
    True        -> use first gcode G1 command as initial position
    [x,y,z,e]   -> non zero coordinates for initial position
"""
initial_position = None

new = gi.gcode_interpreter(filename=r"test.gcode",printer=fictional_printer,initial_position=initial_position)

#print(new.states)

new.plot_2d_position(show_points=False)
new.plot_vel(axis=("x","y","e"))
