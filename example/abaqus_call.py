from pyGCodeDecode import abaqus_file_generator,gcode_interpreter

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

trajectory = gcode_interpreter.simulate(filename=r"test.gcode",printer=fictional_printer,initial_position=initial_position)

abaqus_file_generator.generate_abaqus_events(trajectory=trajectory,output_filename="abaqus.inp")

trajectory.plot_vel()
trajectory.plot_2d_position()