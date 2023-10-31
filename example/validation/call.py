# -*- coding: utf-8 -*-
"""Example usage of pyGCD in the Restore Project."""
from pyGCodeDecode import abaqus_file_generator, gcode_interpreter  # noqa F401

setup = gcode_interpreter.setup(
    filename=r"example\printer_presets.yaml", printer="anisoprint_A4"
)  # Select printer from preset.
setup.set_property({"layer_cue": "LAYER_CHANGE"})  # Prusa Slicer layer change cue.
# setup.set_property({"p_acc": 1000})

stator_simulation = gcode_interpreter.simulate(
    filename=r"example\validation\isocircum_20.gcode", initial_machine_setup=setup
)  # Simulate the gcode.


# Write all layer times.
p_log = open("./example/validation/layertime.csv", "w")
# p_log.write("total time " + str(stator_simulation.blocklist[-1].segments[-1].t_end) + "\n")


last_layer = 0
last_layer_time = 0
for block in stator_simulation.blocklist:
    if block.state_A.layer > last_layer:
        p_log.write(
            # "Layertime layer "
            str(block.state_A.layer)
            + ", "
            + str(block.segments[0].t_begin - last_layer_time)
            + "\n"
        )
        last_layer = block.state_A.layer
        last_layer_time = block.segments[0].t_begin
p_log.close()

stator_simulation.plot_3d_mayavi()
