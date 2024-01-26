<a id="pyGCodeDecode.abaqus_file_generator"></a>

# pyGCodeDecode.abaqus\_file\_generator

Module for generating Abaqus .inp files for AMSIM.

<a id="pyGCodeDecode.abaqus_file_generator.generate_abaqus_events"></a>

#### generate\_abaqus\_events

```python
def generate_abaqus_events(simulation: "gi.simulate",
                           filename="pyGcodeDecode_abaqus_events.inp")
```

Generate abaqus event series.

**Arguments**:

- `simulation` - (simulate) simulation instance
- `filename` - (string, default = "pyGcodeDecode_abaqus_events.inp") output file name

<a id="pyGCodeDecode.gcode_interpreter"></a>

# pyGCodeDecode.gcode\_interpreter

GCode Interpreter Module.

<a id="pyGCodeDecode.gcode_interpreter.update_progress"></a>

#### update\_progress

```python
def update_progress(progress, name="Percent")
```

Display or update a console progress bar.

**Arguments**:

- `progress` - (float, int) between 0 and 1 for percentage, < 0 represents a 'halt', > 1 represents 100%
- `name` - (string, default = "Percent") customizable name for progressbar

<a id="pyGCodeDecode.gcode_interpreter.generate_planner_blocks"></a>

#### generate\_planner\_blocks

```python
def generate_planner_blocks(states: List[state], firmware=None)
```

Convert list of states to trajectory repr. by plannerblocks.

**Arguments**:

- `states` - (list[state]) list of states
- `firmware` - (string, default = None) select firmware by name


**Returns**:

  blck_list (list[planner_block]) list of all plannerblocks to complete travel between all states

<a id="pyGCodeDecode.gcode_interpreter.find_current_segm"></a>

#### find\_current\_segm

```python
def find_current_segm(path: List[segment],
                      t: float,
                      last_index: int = None,
                      keep_position: bool = False)
```

Find the current segment.

**Arguments**:

- `path` - (list[segment]) all segments to be searched
- `t` - (float) time of search
- `last_index` - (int) last found index for optimizing search
- `keep_position` - (bool) keeps position of last segment, use this when working with gaps of no movement inbetween segments


**Returns**:

- `segment` - (segment) the segment which defines movement at that point in time
- `last_index` - (int) last index where something was found, search speed optimization possible

<a id="pyGCodeDecode.gcode_interpreter.unpack_blocklist"></a>

#### unpack\_blocklist

```python
def unpack_blocklist(blocklist: List[planner_block]) -> List[segment]
```

Return list of segments by unpacking list of plannerblocks.

**Arguments**:

- `blocklist` - (list[planner_block]) list of planner blocks


**Returns**:

- `path` - (list[segment]) list of all segments

<a id="pyGCodeDecode.gcode_interpreter.simulate"></a>

## simulate Objects

```python
class simulate()
```

Simulate .gcode with given machine parameters.

<a id="pyGCodeDecode.gcode_interpreter.simulate.__init__"></a>

#### \_\_init\_\_

```python
def __init__(filename: str,
             initial_machine_setup: "setup",
             output_unit_system: str = "SImm")
```

Simulate a given GCode with initial machine setup.

- Generate all states from GCode.
- Connect states with planner blocks, consisting of segments
- Self correct inconsistencies.

**Arguments**:

- `filename` - (string) path to GCode
- `initial_machine_setup` - (setup) setup instance
- `output_unit_system` - (string, default = "SImm") unit system choosable: SI, SImm & inch


**Example**:

```python
gcode_interpreter.simulate(filename=r"part.gcode", initial_machine_setup=setup)
```

<a id="pyGCodeDecode.gcode_interpreter.simulate.plot_2d_position"></a>

#### plot\_2d\_position

```python
def plot_2d_position(filename="trajectory_2D.png",
                     colvar="Velocity",
                     show_points=False,
                     colvar_spatial_resolution=1,
                     dpi=400,
                     scaled=True,
                     show=False)
```

Plot 2D position (XY plane) with matplotlib (unmaintained).

<a id="pyGCodeDecode.gcode_interpreter.simulate.plot_3d_position_legacy"></a>

#### plot\_3d\_position\_legacy

```python
def plot_3d_position_legacy(filename="trajectory_3D.png",
                            dpi=400,
                            show=False,
                            colvar_spatial_resolution=1,
                            colvar="Velocity")
```

Plot 3D position with Matplotlib (unmaintained).

<a id="pyGCodeDecode.gcode_interpreter.simulate.plot_3d_position"></a>

#### plot\_3d\_position

```python
def plot_3d_position(show=True,
                     colvar="Velocity",
                     colvar_spatial_resolution=1,
                     filename=None,
                     dpi=400)
```

Plot 3D position with Matplotlib.

**Arguments**:

- `show` - (bool, default = True) show plot and return plot figure
- `colvar` - (string, default = "Velocity") select color variable
- `colvar_spatial_resolution` - (float, default = 1) spatial interpolation of color variable
- `filename` - (string, default = None) save fig as image if filename is provided
- `dpi` - (int, default = 400) select dpi


**Returns**:

  (optionally)
- `fig` - (figure)

<a id="pyGCodeDecode.gcode_interpreter.simulate.plot_3d_mayavi"></a>

#### plot\_3d\_mayavi

```python
def plot_3d_mayavi(extrusion_only: bool = True, clean_junction=False)
```

Plot 3D Positon with Mayavi (colormap).

**Arguments**:

- `extrusion_only` - (bool, default = True) show only moves with extrusion (slower)
- `clean_junction` - (bool, default = False) add extra vertices at junction for prettier plotting (slower)

<a id="pyGCodeDecode.gcode_interpreter.simulate.plot_vel"></a>

#### plot\_vel

```python
def plot_vel(axis=("x", "y", "z", "e"),
             show=True,
             show_plannerblocks=True,
             show_segments=False,
             show_jv=False,
             timesteps="constrained",
             filename=None,
             dpi=400)
```

Plot axis velocity with matplotlib.

**Arguments**:

- `axis` - (tuple(string), default = ("x", "y", "z", "e")) select plot axis
- `show` - (bool, default = True) show plot and return plot figure
- `show_plannerblocks` - (bool, default = True) show plannerblocks as vertical lines
- `show_segments` - (bool, default = False) show segments as vertical lines
- `show_jv` - (bool, default = False) show junction velocity as x
- `timesteps` - (int or string, default = "constrained") number of timesteps or constrain plot vertices to segment vertices
- `filename` - (string, default = None) save fig as image if filename is provided
- `dpi` - (int, default = 400) select dpi


**Returns**:

  (optionally)
- `fig` - (figure)

<a id="pyGCodeDecode.gcode_interpreter.simulate.trajectory_self_correct"></a>

#### trajectory\_self\_correct

```python
def trajectory_self_correct()
```

Self correct all blocks in the blocklist with self_corection() method.

<a id="pyGCodeDecode.gcode_interpreter.simulate.get_values"></a>

#### get\_values

```python
def get_values(t)
```

Return unit system scaled values for vel and pos.

**Arguments**:

- `t` - (float) time


**Returns**:

- `list` - [vel_x, vel_y, vel_z, vel_e] velocity
- `list` - [pos_x, pos_y, pos_z, pos_e] position

<a id="pyGCodeDecode.gcode_interpreter.simulate.check_initial_setup"></a>

#### check\_initial\_setup

```python
def check_initial_setup(initial_machine_setup)
```

Check the printer Dict for typos or missing parameters and raise errors if invalid.

**Arguments**:

- `initial_machine_setup` - (dict) initial machine setup dictionary

<a id="pyGCodeDecode.gcode_interpreter.simulate.print_summary"></a>

#### print\_summary

```python
def print_summary()
```

Print simulation summary to console.

<a id="pyGCodeDecode.gcode_interpreter.simulate.refresh"></a>

#### refresh

```python
def refresh(new_state_list: List[state] = None)
```

Refresh simulation. Either through new state list or by rerunning the self.states as input.

**Arguments**:

- `new_state_list` - (list[state], default = None) new list of states, if None is provided, existing states get resimulated

<a id="pyGCodeDecode.gcode_interpreter.simulate.extr_extend"></a>

#### extr\_extend

```python
def extr_extend()
```

Return xyz min & max while extruding.

**Returns**:

- `extend` - \[[minX, minY, minZ], [maxX, maxY, maxZ]] (2x3 numpy.ndarray) extend of extruding positions

<a id="pyGCodeDecode.gcode_interpreter.simulate.extr_max_vel"></a>

#### extr\_max\_vel

```python
def extr_max_vel()
```

Return maximum travel velocity while extruding.

**Returns**:

- `max_vel` - (numpy.ndarray, 1x4) maximum axis velocity while extruding

<a id="pyGCodeDecode.gcode_interpreter.simulate.save_summary"></a>

#### save\_summary

```python
def save_summary()
```

Save summary to .yaml file.

Saved data keys:
- filename (string, filename)
- t_end (float, end time)
- x/y/z _min/_max (float, extend where positive extrusion)
- max_extr_trav_vel (float, maximum travel velocity where positive extrusion)

<a id="pyGCodeDecode.gcode_interpreter.setup"></a>

## setup Objects

```python
class setup()
```

Setup for printing simulation.

<a id="pyGCodeDecode.gcode_interpreter.setup.__init__"></a>

#### \_\_init\_\_

```python
def __init__(filename: str,
             printer: str = None,
             layer_cue: str = None) -> None
```

Create simulation setup.

**Arguments**:

- `filename` - (string) choose setup yaml file with printer presets
- `printer` - (string) select printer from preset file
- `layer_cue` - (string) set slicer specific layer change cue from comment

<a id="pyGCodeDecode.gcode_interpreter.setup.load_setup"></a>

#### load\_setup

```python
def load_setup(filename)
```

Load setup from file.

**Arguments**:

- `filename` - (string) specify path to setup file

<a id="pyGCodeDecode.gcode_interpreter.setup.select_printer"></a>

#### select\_printer

```python
def select_printer(printer_name)
```

Select printer by name.

**Arguments**:

- `printer_name` - (string) select printer by name

<a id="pyGCodeDecode.gcode_interpreter.setup.set_initial_position"></a>

#### set\_initial\_position

```python
def set_initial_position(*initial_position)
```

Set initial Position.

**Arguments**:

- `initial_position` - (dict or tuple) set initial position with keys: {X, Y, Z, E} or as tuple of len(4).


**Example**:

```python
setup.set_initial_position(1, 2, 3, 4)
setup.set_initial_position({"X": 1, "Y": 2, "Z": 3, "E": 4})
```

<a id="pyGCodeDecode.gcode_interpreter.setup.set_property"></a>

#### set\_property

```python
def set_property(property_dict: dict)
```

Overwrite or add a property to the printer dictionary. Printer has to be selected through select_printer() beforehand.

**Arguments**:

- `property_dict` - (dict) set or add property to the setup


**Example**:

```python
setup.set_property({"layer_cue": "LAYER_CHANGE"})
```

<a id="pyGCodeDecode.gcode_interpreter.setup.get_dict"></a>

#### get\_dict

```python
def get_dict()
```

Return the setup for the selected printer.

**Returns**:

- `return_dict` - (dict) setup dictionary

<a id="pyGCodeDecode.junction_handling"></a>

# pyGCodeDecode.junction\_handling

Junction handling module.

<a id="pyGCodeDecode.junction_handling.junction_handling"></a>

## junction\_handling Objects

```python
class junction_handling()
```

Junction handling super class.

<a id="pyGCodeDecode.junction_handling.junction_handling.connect_state"></a>

#### connect\_state

```python
def connect_state(state_A: state, state_B: state)
```

Connect two states and generates the velocity for the move from state_A to state_B.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state


**Returns**:

- `velocity` - (float) the target velocity for that travel move

<a id="pyGCodeDecode.junction_handling.junction_handling.calc_vel_next"></a>

#### calc\_vel\_next

```python
def calc_vel_next()
```

Return the target velocity for the following move.

<a id="pyGCodeDecode.junction_handling.junction_handling.get_target_vel"></a>

#### get\_target\_vel

```python
def get_target_vel()
```

Return target velocity.

<a id="pyGCodeDecode.junction_handling.junction_handling.__init__"></a>

#### \_\_init\_\_

```python
def __init__(state_A: state, state_B: state)
```

Initialize the junction handling.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state

<a id="pyGCodeDecode.junction_handling.junction_handling.get_junction_vel"></a>

#### get\_junction\_vel

```python
def get_junction_vel()
```

Return default junction velocity of zero.

**Returns**:

- `0` - zero for default full stop junction handling

<a id="pyGCodeDecode.junction_handling.junction_handling_marlin_jd"></a>

## junction\_handling\_marlin\_jd Objects

```python
class junction_handling_marlin_jd(junction_handling)
```

Marlin specific junction handling with Junction Deviation.

<a id="pyGCodeDecode.junction_handling.junction_handling_marlin_jd.calc_JD"></a>

#### calc\_JD

```python
def calc_JD(vel_0: velocity, vel_1: velocity, p_settings: state.p_settings)
```

Calculate junction deviation velocity from 2 velocitys.

**Reference:**

[https://onehossshay.wordpress.com/2011/09/24/improving_grbl_cornering_algorithm/](https://onehossshay.wordpress.com/2011/09/24/improving_grbl_cornering_algorithm/)
[http://blog.kyneticcnc.com/2018/10/computing-junction-deviation-for-marlin.html](http://blog.kyneticcnc.com/2018/10/computing-junction-deviation-for-marlin.html)


**Arguments**:

- `vel_0` - (velocity) entry
- `vel_1` - (velocity) exit
- `p_settings` - (state.p_settings) print settings


**Returns**:

- `velocity` - (float) velocity abs value

<a id="pyGCodeDecode.junction_handling.junction_handling_marlin_jd.__init__"></a>

#### \_\_init\_\_

```python
def __init__(state_A: state, state_B: state)
```

Marlin specific junction velocity calculation with Junction Deviation.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state

<a id="pyGCodeDecode.junction_handling.junction_handling_marlin_jd.get_junction_vel"></a>

#### get\_junction\_vel

```python
def get_junction_vel()
```

Return junction velocity.

**Returns**:

- `junction_vel` - (float) junction velocity

<a id="pyGCodeDecode.junction_handling.junction_handling_marlin_jerk"></a>

## junction\_handling\_marlin\_jerk Objects

```python
class junction_handling_marlin_jerk(junction_handling)
```

Marlin classic jerk specific junction handling.

**Reference**
[https://github.com/MarlinFirmware/Marlin/pull/8887](https://github.com/MarlinFirmware/Marlin/pull/8887)
[https://github.com/MarlinFirmware/Marlin/pull/8888](https://github.com/MarlinFirmware/Marlin/pull/8888)
[https://github.com/MarlinFirmware/Marlin/issues/367#issuecomment-12505768](https://github.com/MarlinFirmware/Marlin/issues/367#issuecomment-12505768)

<a id="pyGCodeDecode.junction_handling.junction_handling_marlin_jerk.__init__"></a>

#### \_\_init\_\_

```python
def __init__(state_A: state, state_B: state)
```

Marlin classic jerk specific junction velocity calculation.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state

<a id="pyGCodeDecode.junction_handling.junction_handling_marlin_jerk.calc_j_vel"></a>

#### calc\_j\_vel

```python
def calc_j_vel()
```

Calculate the junction velocity.

<a id="pyGCodeDecode.junction_handling.junction_handling_marlin_jerk.get_junction_vel"></a>

#### get\_junction\_vel

```python
def get_junction_vel()
```

Return the calculated junction velocity.

**Returns**:

- `junction_vel` - (float) junction velocity

<a id="pyGCodeDecode.junction_handling.junction_handling_klipper"></a>

## junction\_handling\_klipper Objects

```python
class junction_handling_klipper(junction_handling)
```

Klipper specific junction handling.

- similar junction deviation calc
- corner vel set by: square_corner_velocity
    end_velocity^2 = start_velocity^2 + 2*accel*move_distance
  for 90deg turn
- todo: smoothed look ahead

**Reference:**
[https://www.klipper3d.org/Kinematics.html](https://www.klipper3d.org/Kinematics.html)
[https://github.com/Klipper3d/klipper/blob/ea2f6bc0f544132738c7f052ffcc586fa884a19a/klippy/toolhead.py](https://github.com/Klipper3d/klipper/blob/ea2f6bc0f544132738c7f052ffcc586fa884a19a/klippy/toolhead.py)

<a id="pyGCodeDecode.junction_handling.junction_handling_klipper.__init__"></a>

#### \_\_init\_\_

```python
def __init__(state_A: state, state_B: state)
```

Klipper specific junction velocity calculation.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state

<a id="pyGCodeDecode.junction_handling.junction_handling_klipper.calc_j_delta"></a>

#### calc\_j\_delta

```python
def calc_j_delta()
```

Calculate the junction deviation with klipper specific values.

The jerk value represents the square_corner_velocity!

<a id="pyGCodeDecode.junction_handling.junction_handling_klipper.calc_j_vel"></a>

#### calc\_j\_vel

```python
def calc_j_vel()
```

Calculate the junction velocity.

<a id="pyGCodeDecode.junction_handling.junction_handling_klipper.get_junction_vel"></a>

#### get\_junction\_vel

```python
def get_junction_vel()
```

Return the calculated junction velocity.

**Returns**:

- `junction_vel` - (float) junction velocity

<a id="pyGCodeDecode.junction_handling.junction_handling_MKA"></a>

## junction\_handling\_MKA Objects

```python
class junction_handling_MKA(junction_handling)
```

Anisoprint A4 like junction handling.

**Reference:**
[https://github.com/anisoprint/MKA-firmware/blob/6e02973b1b8f325040cc3dbf66ac545ffc5c06b3/src/core/planner/planner.cpp#L1830](https://github.com/anisoprint/MKA-firmware/blob/6e02973b1b8f325040cc3dbf66ac545ffc5c06b3/src/core/planner/planner.cpp#L1830)

<a id="pyGCodeDecode.junction_handling.junction_handling_MKA.__init__"></a>

#### \_\_init\_\_

```python
def __init__(state_A: state, state_B: state)
```

Marlin classic jerk specific junction velocity calculation.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state

<a id="pyGCodeDecode.junction_handling.junction_handling_MKA.calc_j_vel"></a>

#### calc\_j\_vel

```python
def calc_j_vel()
```

Calculate the junction velocity.

<a id="pyGCodeDecode.junction_handling.junction_handling_MKA.get_junction_vel"></a>

#### get\_junction\_vel

```python
def get_junction_vel()
```

Return the calculated junction velocity.

**Returns**:

- `junction_vel` - (float) junction velocity

<a id="pyGCodeDecode.planner_block"></a>

# pyGCodeDecode.planner\_block

Plannerblock Module.

<a id="pyGCodeDecode.planner_block.planner_block"></a>

## planner\_block Objects

```python
class planner_block()
```

Planner Block Class.

<a id="pyGCodeDecode.planner_block.planner_block.move_maker2"></a>

#### move\_maker2

```python
def move_maker2(v_end)
```

Calculate the correct move type (trapezoidal,triangular or singular) and generate the corresponding segments.

**Arguments**:

- `vel_end` - (velocity) target velocity for end of move

<a id="pyGCodeDecode.planner_block.planner_block.self_correction"></a>

#### self\_correction

```python
def self_correction(tolerance=float("1e-12"))
```

Check for interfacing vel and self correct.

<a id="pyGCodeDecode.planner_block.planner_block.timeshift"></a>

#### timeshift

```python
def timeshift(delta_t: float)
```

Shift planner block in time.

**Arguments**:

- `delta_t` - (float) time to be shifted

<a id="pyGCodeDecode.planner_block.planner_block.extr_block_max_vel"></a>

#### extr\_block\_max\_vel

```python
def extr_block_max_vel()
```

Return max vel from plannerblock while extruding.

**Returns**:

- `block_max_vel` - (np.ndarray 1x4) maximum axis velocity while extruding in block

<a id="pyGCodeDecode.planner_block.planner_block.__init__"></a>

#### \_\_init\_\_

```python
def __init__(state: state, prev_blck: "planner_block", firmware=None)
```

Calculate and store planner block consisting of one or multiple segments.

**Arguments**:

- `state` - (state) the current state
- `prev_blck` - (planner_block) previous planner block
- `firmware` - (string, default = None) firmware selection for junction

<a id="pyGCodeDecode.planner_block.planner_block.prev_blck"></a>

#### prev\_blck

```python
@property
def prev_blck()
```

Define prev_blck as property.

<a id="pyGCodeDecode.planner_block.planner_block.next_blck"></a>

#### next\_blck

```python
@property
def next_blck()
```

Define next_blck as property.

<a id="pyGCodeDecode.planner_block.planner_block.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Create string from plannerblock.

<a id="pyGCodeDecode.planner_block.planner_block.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__() -> str
```

Represent plannerblock.

<a id="pyGCodeDecode.planner_block.planner_block.get_segments"></a>

#### get\_segments

```python
def get_segments()
```

Return segments, contained by the plannerblock.

<a id="pyGCodeDecode.planner_block.planner_block.get_block_travel"></a>

#### get\_block\_travel

```python
def get_block_travel()
```

Return the travel length of the plannerblock.

<a id="pyGCodeDecode.state"></a>

# pyGCodeDecode.state

State module with state.

<a id="pyGCodeDecode.state.state"></a>

## state Objects

```python
class state()
```

State contains a Position and Printing Settings (p_settings) to apply for the corresponding move to this State.

<a id="pyGCodeDecode.state.state.p_settings"></a>

## p\_settings Objects

```python
class p_settings()
```

Store Printing Settings.

<a id="pyGCodeDecode.state.state.p_settings.__init__"></a>

#### \_\_init\_\_

```python
def __init__(p_acc, jerk, vX, vY, vZ, vE, speed, absMode=True, units="SImm")
```

Initialize printing settings.

**Arguments**:

- `p_acc` - (float) printing acceleration
- `jerk` - (float) jerk or similar
- `vX` - (float) max x velocity
- `vY` - (float) max y velocity
- `vZ` - (float) max z velocity
- `vE` - (float) max e velocity
- `speed` - (float) default target velocity
- `absMode` - (bool, default = True) absolute / relative mode
- `units` - (string, default = "SImm") unit settings

<a id="pyGCodeDecode.state.state.p_settings.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Create summary string for p_settings.

<a id="pyGCodeDecode.state.state.p_settings.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__() -> str
```

Define representation.

<a id="pyGCodeDecode.state.state.__init__"></a>

#### \_\_init\_\_

```python
def __init__(state_position: position = None,
             state_p_settings: p_settings = None)
```

Initialize a state.

**Arguments**:

- `state_position` - (position) state position
- `state_p_settings` - (p_settings) state printing settings

<a id="pyGCodeDecode.state.state.state_position"></a>

#### state\_position

```python
@property
def state_position()
```

Define property state_position.

<a id="pyGCodeDecode.state.state.state_p_settings"></a>

#### state\_p\_settings

```python
@property
def state_p_settings()
```

Define property state_p_settings.

<a id="pyGCodeDecode.state.state.line_nmbr"></a>

#### line\_nmbr

```python
@property
def line_nmbr()
```

Define property line_nmbr.

<a id="pyGCodeDecode.state.state.line_nmbr"></a>

#### line\_nmbr

```python
@line_nmbr.setter
def line_nmbr(nmbr)
```

Set line number.

**Arguments**:

- `nmbr` - (int) line number

<a id="pyGCodeDecode.state.state.next_state"></a>

#### next\_state

```python
@property
def next_state()
```

Define property next_state.

<a id="pyGCodeDecode.state.state.next_state"></a>

#### next\_state

```python
@next_state.setter
def next_state(state: "state")
```

Set next state.

**Arguments**:

- `state` - (state) next state

<a id="pyGCodeDecode.state.state.prev_state"></a>

#### prev\_state

```python
@property
def prev_state()
```

Define property prev_state.

<a id="pyGCodeDecode.state.state.prev_state"></a>

#### prev\_state

```python
@prev_state.setter
def prev_state(state: "state")
```

Set previous state.

**Arguments**:

- `state` - (state) previous state

<a id="pyGCodeDecode.state.state.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Generate string for representation.

<a id="pyGCodeDecode.state.state.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__() -> str
```

Call __str__() for representation.

<a id="pyGCodeDecode.state_generator"></a>

# pyGCodeDecode.state\_generator

State generator module.

<a id="pyGCodeDecode.state_generator.arg_extract"></a>

#### arg\_extract

```python
def arg_extract(string: str, key_dict: dict)
```

Extract arguments from known command dictionarys.

**Arguments**:

- `string` - (str) string of Commands
- `key_dict` - (dict) dictionary with known commands and subcommands


**Returns**:

- `dict` - (dict) dictionary with all found keys and their arguments

<a id="pyGCodeDecode.state_generator.read_gcode_to_dict_list"></a>

#### read\_gcode\_to\_dict\_list

```python
def read_gcode_to_dict_list(filename)
```

Read gcode from .gcode file.

**Arguments**:

- `filename` - (string) filename of the .gcode file: e.g. "print.gcode"


**Returns**:

- `dict_list` - (list[dict]) list with every line as dict

<a id="pyGCodeDecode.state_generator.dict_list_traveler"></a>

#### dict\_list\_traveler

```python
def dict_list_traveler(line_dict_list: List[dict],
                       initial_machine_setup: dict = None)
```

Convert the line dictionary to a state.

**Arguments**:

- `line_dict_list` - (dict) dict list with commands
- `initial_machine_setup` - (dict) dict with initial machine setup [absolute_position, absolute_extrusion, units, initial_position...]


**Returns**:

- `state_list` - (list[state]) all states in a list

<a id="pyGCodeDecode.state_generator.state_generator"></a>

#### state\_generator

```python
def state_generator(filename: str, initial_machine_setup: dict = None)
```

Generate state list from GCode file.

**Arguments**:

- `filename` - (string) filename of GCode
- `initial_machine_setup` - (dict) dictionary with machine setup


**Returns**:

- `states` - (list[states]) all states in a list

<a id="pyGCodeDecode.test.self_test.self_test"></a>

# pyGCodeDecode.test.self\_test.self\_test

Test pyGCD with known analytical solutions for simple trajectory planning tasks with other features as well.

<a id="pyGCodeDecode.test.test_gcode_interpreter"></a>

# pyGCodeDecode.test.test\_gcode\_interpreter

Test for gcode interpreter.

<a id="pyGCodeDecode.test.test_gcode_interpreter.test_setup"></a>

#### test\_setup

```python
def test_setup()
```

Test for the simulation setup class.

<a id="pyGCodeDecode.test.test_gcode_interpreter.test_simulate"></a>

#### test\_simulate

```python
def test_simulate()
```

Test for simulate class.

<a id="pyGCodeDecode.test.test_planner_block"></a>

# pyGCodeDecode.test.test\_planner\_block

Test for planner block module.

<a id="pyGCodeDecode.test.test_planner_block.test_planner_block"></a>

#### test\_planner\_block

```python
def test_planner_block()
```

Test method for the Planner Block module.

Create single standalone blocks with no initial velocity.
Test for the three cases: trapez, triangle and singular against known analytical solutions.
To-Do:
    - self correction is not being tested.
    - advanced tests for Junction Deviation, currently only straight line JD is tested.
    - extrusion only not being tested
    - helper function

<a id="pyGCodeDecode.test.test_state_generator"></a>

# pyGCodeDecode.test.test\_state\_generator

Test for state generator module.

<a id="pyGCodeDecode.test.test_state_generator.test_state_generator"></a>

#### test\_state\_generator

```python
def test_state_generator()
```

Test the state generator function.

Functionality:
- G0,G1
- M82
- M83
- G90
- G91
- G92
- G20
- G21
- comment
- M203
- M204
- M205
- G4
To-Do:
    --> rest of supported commands + glitch/inject tests

<a id="pyGCodeDecode.test"></a>

# pyGCodeDecode.test

Tests for the pyGCodeDecode package.

<a id="pyGCodeDecode.tools"></a>

# pyGCodeDecode.tools

Tools for pyGCD.

<a id="pyGCodeDecode.tools.print_layertimes"></a>

#### print\_layertimes

```python
def print_layertimes(simulation: simulate,
                     filename="layertimes.csv",
                     locale=None,
                     delimiter=";")
```

Print out all layer times (detected by layer cue in GCode comment) to a file.

**Arguments**:

- `simulation` - (simulate) simulation instance
- `filename` - (string, default = "layertimes.csv") file name
- `locale` - (string, default = None) select locale settings, e.g. "en_us" "de_de", None = use system locale
- `delimiter` - (string, default = ";") select delimiter

<a id="pyGCodeDecode.utils"></a>

# pyGCodeDecode.utils

Utilitys.

Utils for the GCode Reader contains:
- vector 4D
    - velocity
    - position

<a id="pyGCodeDecode.utils.vector_4D"></a>

## vector\_4D Objects

```python
class vector_4D()
```

The vector_4D class stores 4D vector in x,y,z,e.

**Supports:**
- str
- add
- sub
- mul (scalar)
- truediv (scalar)
- eq

<a id="pyGCodeDecode.utils.vector_4D.__init__"></a>

#### \_\_init\_\_

```python
def __init__(*args)
```

Store 3D position + extrusion axis.

**Arguments**:

- `args` - (tuple or list) as x,y,z,e or [x,y,z,e]

<a id="pyGCodeDecode.utils.vector_4D.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Return string representation.

<a id="pyGCodeDecode.utils.vector_4D.__add__"></a>

#### \_\_add\_\_

```python
def __add__(other)
```

Add functionality for 4D vectors.

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')


**Returns**:

- `add` - (self) component wise addition

<a id="pyGCodeDecode.utils.vector_4D.__sub__"></a>

#### \_\_sub\_\_

```python
def __sub__(other)
```

Sub functionality for 4D vectors.

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')


**Returns**:

- `sub` - (self) component wise subtraction

<a id="pyGCodeDecode.utils.vector_4D.__mul__"></a>

#### \_\_mul\_\_

```python
def __mul__(other)
```

Scalar multiplication functionality for 4D vectors.

**Arguments**:

- `other` - (float or int)


**Returns**:

- `mul` - (self) scalar multiplication, scaling

<a id="pyGCodeDecode.utils.vector_4D.__truediv__"></a>

#### \_\_truediv\_\_

```python
def __truediv__(other)
```

Scalar division functionality for 4D Vectors.

**Arguments**:

- `other` - (float or int)


**Returns**:

- `div` - (self) scalar division, scaling

<a id="pyGCodeDecode.utils.vector_4D.__eq__"></a>

#### \_\_eq\_\_

```python
def __eq__(other)
```

Check for equality and return True if equal.

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')


**Returns**:

- `eq` - (bool) true if equal (with tolerance)

<a id="pyGCodeDecode.utils.vector_4D.get_vec"></a>

#### get\_vec

```python
def get_vec(withExtrusion=False)
```

Return the 4D vector, optionally with extrusion.

**Arguments**:

- `withExtrusion` - (bool, default = False) choose if vec repr contains extrusion


**Returns**:

- `vec` - (list[3 or 4]) with (x,y,z,(optionally e))

<a id="pyGCodeDecode.utils.vector_4D.get_norm"></a>

#### get\_norm

```python
def get_norm(withExtrusion=False)
```

Return the 4D vector norm. Optional with extrusion.

**Arguments**:

- `withExtrusion` - (bool, default = False) choose if norm contains extrusion


**Returns**:

- `norm` - (float) length/norm of 3D or 4D vector

<a id="pyGCodeDecode.utils.velocity"></a>

## velocity Objects

```python
class velocity(vector_4D)
```

4D - Velocity object for (cartesian) 3D printer.

<a id="pyGCodeDecode.utils.velocity.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Print out velocity.

<a id="pyGCodeDecode.utils.velocity.get_norm_dir"></a>

#### get\_norm\_dir

```python
def get_norm_dir(withExtrusion=False)
```

Get normalized vector (regarding travel distance), if only extrusion occurs, normalize to extrusion length.

**Arguments**:

- `withExtrusion` - (bool, default = False) choose if norm dir contains extrusion


**Returns**:

- `dir` - (list[3 or 4]) normalized direction vector as list

<a id="pyGCodeDecode.utils.velocity.avoid_overspeed"></a>

#### avoid\_overspeed

```python
def avoid_overspeed(p_settings)
```

Return velocity without any axis overspeed.

**Arguments**:

- `p_settings` - (p_settings) printing settings


**Returns**:

- `vel` - (velocity) constrained by max velocity

<a id="pyGCodeDecode.utils.velocity.not_zero"></a>

#### not\_zero

```python
def not_zero()
```

Return True if velocity is not zero.

**Returns**:

- `not_zero` - (bool) true if velocity is not zero

<a id="pyGCodeDecode.utils.velocity.is_extruding"></a>

#### is\_extruding

```python
def is_extruding()
```

Return True if extrusion velocity is not zero.

**Returns**:

- `is_extruding` - (bool) true if positive extrusion velocity

<a id="pyGCodeDecode.utils.position"></a>

## position Objects

```python
class position(vector_4D)
```

4D - Position object for (cartesian) 3D printer.

<a id="pyGCodeDecode.utils.position.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Print out position.

<a id="pyGCodeDecode.utils.position.is_travel"></a>

#### is\_travel

```python
def is_travel(other) -> bool
```

Return True if there is travel between self and other position.

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')


**Returns**:

- `is_travel` - (bool) true if between self and other is distance

<a id="pyGCodeDecode.utils.position.is_extruding"></a>

#### is\_extruding

```python
def is_extruding(other: "position", ignore_retract: bool = True) -> bool
```

Return True if there is extrusion between self and other position.

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')
- `ignore_retract` - (bool, default = True) if true ignore retract movements else retract is also extrusion


**Returns**:

- `is_extruding` - (bool) true if between self and other is extrusion

<a id="pyGCodeDecode.utils.position.get_t_distance"></a>

#### get\_t\_distance

```python
def get_t_distance(other=None, withExtrusion=False) -> float
```

Calculate the travel distance between self and other position. If none is provided, zero will be used.

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray', default = None)
- `withExtrusion` - (bool, default = False) use or ignore extrusion


**Returns**:

- `travel` - (float) travel or extrusion and travel distance

<a id="pyGCodeDecode.utils.segment"></a>

## segment Objects

```python
class segment()
```

Store Segment data for linear 4D Velocity function segment.

contains: time, position, velocity
**Supports**
- str

**Additional methods**
- move_segment_time: moves Segment in time by a specified interval
- get_velocity: returns the calculated Velocity for all axis at a given point in time
- get_position: returns the calculated Position for all axis at a given point in time

**Class method**
- create_initial: returns the artificial initial segment where everything is at standstill, intervall length = 0
- self_check: returns True if all self checks have been successfull

<a id="pyGCodeDecode.utils.segment.__init__"></a>

#### \_\_init\_\_

```python
def __init__(t_begin: float,
             t_end: float,
             pos_begin: position,
             vel_begin: velocity,
             pos_end: position = None,
             vel_end: velocity = None)
```

Initialize a segment.

**Arguments**:

- `t_begin` - (float) begin of segment
- `t_end` - (float) end of segment
- `pos_begin` - (position) beginning position of segment
- `vel_begin` - (velocity) beginning velocity of segment
- `pos_end` - (position, default = None) ending position of segment
- `vel_end` - (velocity, default = None) ending velocity of segment

<a id="pyGCodeDecode.utils.segment.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Create string from segment.

<a id="pyGCodeDecode.utils.segment.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__()
```

Segment representation.

<a id="pyGCodeDecode.utils.segment.move_segment_time"></a>

#### move\_segment\_time

```python
def move_segment_time(delta_t: float)
```

Move segment in time.

**Arguments**:

- `delta_t` - (float) time to be shifted

<a id="pyGCodeDecode.utils.segment.get_velocity"></a>

#### get\_velocity

```python
def get_velocity(t)
```

Get current velocity of segment at a certain time.

**Arguments**:

- `t` - (float) time


**Returns**:

- `current_vel` - (velocity) velocity at time t

<a id="pyGCodeDecode.utils.segment.get_position"></a>

#### get\_position

```python
def get_position(t)
```

Get current position of segment at a certain time.

**Arguments**:

- `t` - (float) time


**Returns**:

- `pos` - (position) position at time t

<a id="pyGCodeDecode.utils.segment.self_check"></a>

#### self\_check

```python
def self_check(p_settings=None)
```

Check the segment for self consistency.

todo:
- max acceleration

**Arguments**:

- `p_settings` - (p_setting, default = None) printing settings to verify

<a id="pyGCodeDecode.utils.segment.is_extruding"></a>

#### is\_extruding

```python
def is_extruding()
```

Return true if the segment is pos. extruding.

**Returns**:

- `is_extruding` - (bool) true if positive extrusion

<a id="pyGCodeDecode.utils.segment.create_initial"></a>

#### create\_initial

```python
@classmethod
def create_initial(cls, initial_position: position = None)
```

Create initial static segment with (optionally) initial position else start from Zero.

**Arguments**:

- `initial_position` - (postion, default = None) position to begin segment series


**Returns**:

- `segment` - (segment) initial beginning segment
