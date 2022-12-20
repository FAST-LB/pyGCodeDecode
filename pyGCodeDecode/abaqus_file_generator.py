from gcode_interpreter import gcode_interpreter, unpack_blocklist


"""
This script is to convert gcode into an event series as abaqus input

An example output looks like this:

time    x       y       z       extrusion bool -> 1 = extrusion moving to next step, 0 = no extrusion
0.0,    1.0,    0.0,    2.0,    1
0.44,   1.0,    22.0,   2.0,    0

timepoints generated are always at segment beginnings / endings, so interpolation linearly is the exact solution

"""
###Fictional Printer Preset
fictional_printer = {
    #general properties
    "nozzle_diam"   :   0.4,
    "filament_diam" :   1.75,
    
    #settings
    "velocity"      :   35,
    "acceleration"  :   20,
    "jerk"          :   10,
    
    #axis max speeds
    "Vx"            :   60,
    "Vy"            :   60,
    "Vz"            :   40,
    "Ve"            :   25
    }

initial_position = True #uses first gcode point as initial position, alternative: [x,y,z,e]

trajectory  = gcode_interpreter(filename="test.gcode",initial_position=initial_position,printer=fictional_printer)

output_filename = "gcode_to_abaqus.inp"




#get all positions and timings
unpacked    = unpack_blocklist(trajectory.blocklist)
pos     = [unpacked[0].get_position(t=unpacked[0].t_begin).get_vec(withExtrusion=True)]
time    = [0]
for segm in unpacked:
    pos.append(segm.get_position(t=segm.t_end).get_vec(withExtrusion=True))
    time.append(segm.t_end)

#figure out if extrusion happens from this to the next step, if yes -> 1, if no -> 0
for id in range(len(pos)-1):
    if pos[id+1][3]-pos[id][3] > 0:
        pos[id][3]   = 1
    else: pos[id][3] = 0
pos[-1][3] = 0

#writeout to file
f = open(output_filename, "w")
for time,pos in zip(time,pos):
    f.write(str(time)   +","+   str(pos[0])     +","+   str(pos[1])     +","+   str(pos[2]) +","+   str(pos[3]) + "\n")
f.close()
