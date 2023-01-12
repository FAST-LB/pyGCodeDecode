from pyGCodeDecode import abaqus_file_generator,gcode_interpreter

###Fictional Printer Preset
fictional_printer = {
    #general properties
    "nozzle_diam"   :   0.4,
    "filament_diam" :   1.75,
    
    #default settings
    "velocity"      :   35,
    "acceleration"  :   20,
    "jerk"          :   10,
    
    #axis max speeds
    "Vx"            :   80,
    "Vy"            :   80,
    "Vz"            :   80,
    "Ve"            :   25
    }

""" INITIAL POSITION:
    None        -> start from zero
    True        -> use first gcode G1 command as initial position
    [x,y,z,e]   -> non zero coordinates for initial position
"""
initial_position = None

trajectory = gcode_interpreter.simulate(filename=r"3DBenchy.gcode",printer=fictional_printer,initial_position=initial_position)

abaqus_file_generator.generate_abaqus_events(trajectory=trajectory,output_filename="abaqus.inp")

trajectory.plot_3d_position()
#trajectory.plot_vel()
trajectory.plot_2d_position(show_points=False)
trajectory.plot_vel(show_JD=False,show_plannerblocks=False,axis=("x","y","z"))