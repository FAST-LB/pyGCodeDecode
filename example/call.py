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
    [x,y,z,e]   -> non zero coordinates for initial position
    True        -> use first gcode G1 command as initial position
    False, None -> start from zero
"""
initial_position = True

new = gi.gcode_interpreter(filename=r"test.gcode",initial_position=initial_position,printer=fictional_printer)

print(new.states)

new.plot_2d_position(show_points=False)
new.plot_vel(axis=("x","y","e"))
