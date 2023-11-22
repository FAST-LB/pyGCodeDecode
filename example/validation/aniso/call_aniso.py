# -*- coding: utf-8 -*-
"""Example usage of pyGCD in the Restore Project."""
import time

from pyGCodeDecode import abaqus_file_generator, gcode_interpreter  # noqa F401

printfile = r"example\validation\aniso\JDJERK_1_5_7_10_15_20_30_drop.gcode"

setup = gcode_interpreter.setup(filename=r"example\printer_presets.yaml")  # load setup
setup.select_printer("anisoprint_A4")  # Select printer from preset.
setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.

setup.set_property({"firmware": "MKA"})
start_time = time.time()
simulation = gcode_interpreter.simulate(filename=printfile, initial_machine_setup=setup)  # Simulate the gcode.
print("---Simulation took %s seconds ---" % (time.time() - start_time))
# simulation.plot_vel(show=True, filename=False)
simulation.plot_3d_mayavi(extrusion_only=False)
setup.set_property({"firmware": "marlin"})
start_time = time.time()
simulation = gcode_interpreter.simulate(filename=printfile, initial_machine_setup=setup)  # Simulate the gcode.
print("---Simulation took %s seconds ---" % (time.time() - start_time))
# simulation.plot_vel(show=True, filename=False)

setup.set_property({"firmware": "marlin_jerk"})
start_time = time.time()
simulation = gcode_interpreter.simulate(filename=printfile, initial_machine_setup=setup)  # Simulate the gcode.
print("---Simulation took %s seconds ---" % (time.time() - start_time))
# simulation.plot_vel(show=True, filename=False)

setup.set_property({"firmware": "marlin_klipper"})
start_time = time.time()
simulation = gcode_interpreter.simulate(filename=printfile, initial_machine_setup=setup)  # Simulate the gcode.
print("---Simulation took %s seconds ---" % (time.time() - start_time))
# simulation.plot_vel(show=True, filename=False)

if False:
    # Write all layer times.
    p_log = open("./example/validation/aniso/layertime_aniso.csv", "w")
    # p_log.write("total time " + str(stator_simulation.blocklist[-1].segments[-1].t_end) + "\n")

    last_layer = 0
    last_layer_time = 0
    travel = 0
    p_log.write("layer, layer time in s, travel distance in mm, avg speed in mm/s\n")

    for block in simulation.blocklist:
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
