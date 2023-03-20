from pyGCodeDecode import gcode_interpreter

###Fictional Printer Preset
fictional_printer = {
    #general properties
    "nozzle_diam"   :   0.4,
    "filament_diam" :   1.75,
    
    #default settings
    "velocity"      :   35,
    "acceleration"  :   20,
    "jerk"          :   2,
    
    #axis max speeds
    "Vx"            :   60,
    "Vy"            :   60,
    "Vz"            :   40,
    "Ve"            :   25
    }

anisoprint_A4 = {
    #general properties
    "nozzle_diam"   :   0.4,
    "filament_diam" :   1.75,
    
    #default settings
    "velocity"      :   35,
    "acceleration"  :   1000,
    "jerk"          :   10,
    
    #axis max speeds
    "Vx"            :   180,
    "Vy"            :   180,
    "Vz"            :   30,
    "Ve"            :   33
    }

""" INITIAL POSITION:
    None        -> start from zero
    True        -> use first gcode G1 command as initial position
    [x,y,z,e]   -> non zero coordinates for initial position
"""
initial_position = None

new = gcode_interpreter.simulate(filename=r"example\test.gcode",printer=anisoprint_A4,initial_position=initial_position)


new.plot_2d_position(show=True,colvar_spatial_resolution=0.1,filename=False)
new.plot_vel(show=True,filename=False)

#new.plot_3d_position(filename="3DPlot.png",colvar_spatial_resolution=0.1)
#new.plot_vel(axis=("x","y","e"))
