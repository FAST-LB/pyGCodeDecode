# -*- coding: utf-8 -*-
"""Example usage of pyGCD in the Restore Project."""
from pyGCodeDecode import abaqus_file_generator, gcode_interpreter  # noqa F401

setup = gcode_interpreter.setup(
    filename=r"example\printer_presets.yaml", printer="anisoprint_A4"
)  # Select printer from preset.
setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.

stator_simulation = gcode_interpreter.simulate(
    filename=r"example\Restore\stator.gcode", initial_machine_setup=setup
)  # Simulate the gcode.


# Write all pause times and total printing time into seperate file.
p_log = open("./example/Restore/pause_log.txt", "w")
p_log.write("total time " + str(stator_simulation.blocklist[-1].segments[-1].t_end) + "\n")

stator_simulation.plot_3d_mayavi()

# for block in stator_simulation.blocklist:
#     if block.state_B.pause is not None:
#         # print("Pause ---> " + str(block.state_B.comment))
#         # print("pause start: " + str(block.segments[0].t_begin))
#         # print("pause   end: " + str(block.segments[-1].t_end))
#         # print("Z: " + str(block.segments[0].pos_begin.z) + "\n")

#         p_log.write("Pause ---> " + str(block.state_B.comment))
#         p_log.write("\tpause start: " + str(block.segments[0].t_begin))
#         p_log.write("\tpause start+5: " + str(block.segments[0].t_begin + 5))
#         p_log.write("\tpause end: " + str(block.segments[-1].t_end))
#         p_log.write("\tpause dur: " + str(block.segments[-1].t_end - block.segments[0].t_begin))
#         p_log.write("\tZ: " + str(block.segments[0].pos_begin.z) + "\n")
# p_log.close()

# abaqus_file_generator.generate_abaqus_events(stator_simulation, "./example/Restore/stator_event_series.inp")
