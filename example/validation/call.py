# -*- coding: utf-8 -*-
"""Example usage of pyGCD in the Restore Project."""
import time

from pyGCodeDecode import abaqus_file_generator, gcode_interpreter  # noqa F401

start_time = time.time()

setup = gcode_interpreter.setup(filename=r"example\printer_presets.yaml")  # load setup
setup.select_printer("prusa_mini_klipper")  # Select printer from preset.
setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.

# setup.set_property({"p_acc": 1000})
setup.set_property({"jerk": 20})

stator_simulation = gcode_interpreter.simulate(
    filename=r"example\validation\prusa_mini_2.gcode", initial_machine_setup=setup
)  # Simulate the gcode.

print("--- %s seconds ---" % (time.time() - start_time))


# Write all layer times.
p_log = open("./example/validation/layertime.csv", "w")
# p_log.write("total time " + str(stator_simulation.blocklist[-1].segments[-1].t_end) + "\n")


last_layer = 0
last_layer_time = 0
travel = 0
p_log.write("layer, layer time in s, travel distance in mm, avg speed in mm/s\n")

for block in stator_simulation.blocklist:
    travel += block.get_block_travel()

    if block.state_B.layer > last_layer:
        p_log.write(
            # "Layertime layer "
            str(block.state_B.layer)
            + ", "
            + str(block.segments[0].t_begin - last_layer_time)
            + ", "
            + str(travel)
            + ", "
            + str(travel / (block.segments[0].t_begin - last_layer_time))
            + "\n"
        )
        last_layer = block.state_B.layer
        last_layer_time = block.segments[0].t_begin
        travel = 0
p_log.close()

# stator_simulation.plot_3d_mayavi()
