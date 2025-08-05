# pyGCodeDecode Reference

<a id="pyGCodeDecode.abaqus_file_generator"></a>

## pyGCodeDecode.abaqus\_file\_generator

Module for generating Abaqus .inp files for AMSIM.

<a id="pyGCodeDecode.abaqus_file_generator.generate_abaqus_event_series"></a>

#### generate\_abaqus\_event\_series

```python
def generate_abaqus_event_series(
        simulation: gcode_interpreter.simulation,
        filepath: str = "pyGcodeDecode_abaqus_events.inp",
        tolerance: float = 1e-12,
        output_unit_system: str = None,
        return_tuple: bool = False) -> tuple
```

Generate abaqus event series.

**Arguments**:

- `simulation` _gcode_interpreter.simulation_ - simulation instance
- `filepath` _string, default = "pyGcodeDecode_abaqus_events.inp"_ - output file path
- `tolerance` _float, default = 1e-12_ - tolerance to determine whether extrusion is happening
- `output_unit_system` _str, optional_ - Unit system for the output.
  The one from the simulation is used, in None is specified.
- `return_tuple` _bool, default = False_ - return the event series as tuple.


**Returns**:

  (optional) tuple: the event series as a tuple for use in ABAQUS-Python

<a id="pyGCodeDecode.cli"></a>

## pyGCodeDecode.cli

The CLI for the pyGCodeDecode package.

<a id="pyGCodeDecode.gcode_interpreter"></a>

## pyGCodeDecode.gcode\_interpreter

GCode Interpreter Module.

<a id="pyGCodeDecode.gcode_interpreter.generate_planner_blocks"></a>

#### generate\_planner\_blocks

```python
def generate_planner_blocks(states: List[state], firmware=None)
```

Convert list of states to trajectory repr. by planner blocks.

**Arguments**:

- `states` - (list[state]) list of states
- `firmware` - (string, default = None) select firmware by name


**Returns**:

  block_list (list[planner_block]) list of all planner blocks to complete travel between all states

<a id="pyGCodeDecode.gcode_interpreter.find_current_segment"></a>

#### find\_current\_segment

```python
def find_current_segment(path: List[segment],
                         t: float,
                         last_index: int = None,
                         keep_position: bool = False)
```

Find the current segment.

**Arguments**:

- `path` - (list[segment]) all segments to be searched
- `t` - (float) time of search
- `last_index` - (int) last found index for optimizing search
- `keep_position` - (bool) keeps position of last segment, use this when working with
  gaps of no movement between segments


**Returns**:

- `segment` - (segment) the segment which defines movement at that point in time
- `last_index` - (int) last index where something was found, search speed optimization possible

<a id="pyGCodeDecode.gcode_interpreter.unpack_blocklist"></a>

#### unpack\_blocklist

```python
def unpack_blocklist(blocklist: List[planner_block]) -> List[segment]
```

Return list of segments by unpacking list of planner blocks.

**Arguments**:

- `blocklist` - (list[planner_block]) list of planner blocks


**Returns**:

- `path` - (list[segment]) list of all segments

<a id="pyGCodeDecode.gcode_interpreter.simulation"></a>

### simulation Objects

```python
class simulation()
```

Simulation of .gcode with given machine parameters.

<a id="pyGCodeDecode.gcode_interpreter.simulation.trajectory_self_correct"></a>

#### trajectory\_self\_correct

```python
def trajectory_self_correct()
```

Self correct all blocks in the blocklist with self_correction() method.

<a id="pyGCodeDecode.gcode_interpreter.simulation.calc_results"></a>

#### calc\_results

```python
def calc_results()
```

Calculate the results.

<a id="pyGCodeDecode.gcode_interpreter.simulation.calculate_averages"></a>

#### calculate\_averages

```python
def calculate_averages()
```

Calculate averages for averageable results.

<a id="pyGCodeDecode.gcode_interpreter.simulation.get_values"></a>

#### get\_values

```python
def get_values(t: float, output_unit_system: str = None) -> Tuple[List[float]]
```

Return unit system scaled values for vel and pos.

**Arguments**:

- `t` - (float) time
- `output_unit_system` _str, optional_ - Unit system for the output.
  The one from the simulation is used, in None is specified.


**Returns**:

- `list` - [vel_x, vel_y, vel_z, vel_e] velocity
- `list` - [pos_x, pos_y, pos_z, pos_e] position

<a id="pyGCodeDecode.gcode_interpreter.simulation.get_width"></a>

#### get\_width

```python
def get_width(t: float,
              extrusion_h: float,
              filament_dia: Optional[float] = None) -> float
```

Return the extrusion width for a certain extrusion height at time.

**Arguments**:

- `t` _float_ - time
- `extrusion_h` _float_ - extrusion height / layer height
- `filament_dia` _float_ - filament_diameter


**Returns**:

- `float` - width

<a id="pyGCodeDecode.gcode_interpreter.simulation.print_summary"></a>

#### print\_summary

```python
def print_summary(start_time: float)
```

Print simulation summary to console.

**Arguments**:

- `start_time` _float_ - time when the simulation run was started

<a id="pyGCodeDecode.gcode_interpreter.simulation.refresh"></a>

#### refresh

```python
def refresh(new_state_list: List[state] = None)
```

Refresh simulation. Either through new state list or by rerunning the self.states as input.

**Arguments**:

- `new_state_list` - (list[state], default = None) new list of states,
  if None is provided, existing states get resimulated

<a id="pyGCodeDecode.gcode_interpreter.simulation.extrusion_extent"></a>

#### extrusion\_extent

```python
def extrusion_extent(output_unit_system: str = None) -> np.ndarray
```

Return scaled xyz min & max while extruding.

**Arguments**:

- `output_unit_system` _str, optional_ - Unit system for the output.
  The one from the simulation is used, in None is specified.


**Raises**:

- `ValueError` - if nothing is extruded


**Returns**:

- `np.ndarray` - extent of extruding positions

<a id="pyGCodeDecode.gcode_interpreter.simulation.extrusion_max_vel"></a>

#### extrusion\_max\_vel

```python
def extrusion_max_vel(output_unit_system: str = None) -> np.float64
```

Return scaled maximum velocity while extruding.

**Arguments**:

- `output_unit_system` _str, optional_ - Unit system for the output.
  The one from the simulation is used, in None is specified.


**Returns**:

- `max_vel` - (np.float64) maximum travel velocity while extruding

<a id="pyGCodeDecode.gcode_interpreter.simulation.save_summary"></a>

#### save\_summary

```python
def save_summary(filepath: Union[pathlib.Path, str])
```

Save summary to .yaml file.

**Arguments**:

- `filepath` _pathlib.Path | str_ - path to summary file

  Saved data keys:
  - filename (string, filename)
  - t_end (float, end time)
  - x/y/z _min/_max (float, extent where positive extrusion)
  - max_extrusion_travel_velocity (float, maximum travel velocity where positive extrusion)

<a id="pyGCodeDecode.gcode_interpreter.simulation.get_scaling_factor"></a>

#### get\_scaling\_factor

```python
def get_scaling_factor(output_unit_system: str = None) -> float
```

Get a scaling factor to convert lengths from mm to another supported unit system.

**Arguments**:

- `output_unit_system` _str, optional_ - Wanted output unit system.
  Uses the one specified for the simulation on None is specified.


**Returns**:

- `float` - scaling factor

<a id="pyGCodeDecode.gcode_interpreter.setup"></a>

### setup Objects

```python
class setup()
```

Setup for printing simulation.

<a id="pyGCodeDecode.gcode_interpreter.setup.load_setup"></a>

#### load\_setup

```python
def load_setup(filepath)
```

Load setup from file.

**Arguments**:

- `filepath` - (string) specify path to setup file

<a id="pyGCodeDecode.gcode_interpreter.setup.check_initial_setup"></a>

#### check\_initial\_setup

```python
def check_initial_setup()
```

Check the printer Dict for typos or missing parameters and raise errors if invalid.

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
def set_initial_position(initial_position: Union[tuple, dict],
                         input_unit_system: str = None)
```

Set initial Position.

**Arguments**:

- `initial_position` - (tuple or dict) set initial position as tuple of len(4)
  or dictionary with keys: {X, Y, Z, E}.
- `input_unit_system` _str, optional_ - Wanted input unit system.
  Uses the one specified for the setup if None is specified.


**Example**:

```python
setup.set_initial_position((1, 2, 3, 4))
setup.set_initial_position({"X": 1, "Y": 2, "Z": 3, "E": 4})
```

<a id="pyGCodeDecode.gcode_interpreter.setup.set_property"></a>

#### set\_property

```python
def set_property(property_dict: dict)
```

Overwrite or add a property to the printer dictionary.

Printer has to be selected through select_printer() beforehand.

**Arguments**:

- `property_dict` - (dict) set or add property to the setup


**Example**:

```python
setup.set_property({"layer_cue": "LAYER_CHANGE"})
```

<a id="pyGCodeDecode.gcode_interpreter.setup.get_dict"></a>

#### get\_dict

```python
def get_dict() -> dict
```

Return the setup for the selected printer.

**Returns**:

- `return_dict` - (dict) setup dictionary

<a id="pyGCodeDecode.gcode_interpreter.setup.get_scaling_factor"></a>

#### get\_scaling\_factor

```python
def get_scaling_factor(input_unit_system: str = None) -> float
```

Get a scaling factor to convert lengths from mm to another supported unit system.

**Arguments**:

- `input_unit_system` _str, optional_ - Wanted input unit system.
  Uses the one specified for the setup if None is specified.


**Returns**:

- `float` - scaling factor

<a id="pyGCodeDecode.helpers"></a>

## pyGCodeDecode.helpers

Helper functions.

<a id="pyGCodeDecode.helpers.VERBOSITY_LEVEL"></a>

#### VERBOSITY\_LEVEL

default to INFO

<a id="pyGCodeDecode.helpers.set_verbosity_level"></a>

#### set\_verbosity\_level

```python
def set_verbosity_level(level: Optional[int]) -> None
```

Set the global verbosity level.

<a id="pyGCodeDecode.helpers.get_verbosity_level"></a>

#### get\_verbosity\_level

```python
def get_verbosity_level() -> int
```

Get the current global verbosity level.

<a id="pyGCodeDecode.helpers.custom_print"></a>

#### custom\_print

```python
def custom_print(*args, lvl=2, **kwargs) -> None
```

Sanitize outputs for ABAQUS and print them if the log level is high enough. Takes all arguments for print.

**Arguments**:

- `*args` - arguments to be printed
- `lvl` - verbosity level of the print (1 = WARNING, 2 = INFO, 3 = DEBUG)
- `**kwargs` - keyword arguments to be passed to print

<a id="pyGCodeDecode.helpers.ProgressBar"></a>

### ProgressBar Objects

```python
class ProgressBar()
```

A simple progress bar for the console.

<a id="pyGCodeDecode.helpers.ProgressBar.update"></a>

#### update

```python
def update(progress: float) -> None
```

Display or update a console progress bar.

**Arguments**:

- `progress` - float between 0 and 1 for percentage, < 0 represents a 'halt', > 1 represents 100%

<a id="pyGCodeDecode.junction_handling"></a>

## pyGCodeDecode.junction\_handling

Junction handling module.

<a id="pyGCodeDecode.junction_handling.junction_handling"></a>

### junction\_handling Objects

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

<a id="pyGCodeDecode.junction_handling.junction_handling.get_junction_vel"></a>

#### get\_junction\_vel

```python
def get_junction_vel()
```

Return default junction velocity of zero.

**Returns**:

- `0` - zero for default full stop junction handling

<a id="pyGCodeDecode.junction_handling.prusa"></a>

### prusa Objects

```python
class prusa(junction_handling)
```

Prusa specific classic jerk junction handling (validated on Prusa Mini).

**Reference**
[Prusa Firmware Buddy GitHub](https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/818d812f954802903ea0ff39bf44376fb0b35dd2/lib/Marlin/Marlin/src/module/planner.cpp#L1911) # noqa: E501


**Code reference:**
[Prusa-Firmware-Buddy/lib/Marlin/Marlin/src/module/planner.cpp](https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/818d812f954802903ea0ff39bf44376fb0b35dd2/lib/Marlin/Marlin/src/module/planner.cpp#L1951)

```cpp
// ...
// Factor to multiply the previous / current nominal velocities to get componentwise limited velocities.
  float v_factor = 1;
  limited = 0;

  // The junction velocity will be shared between successive segments. Limit the junction velocity to their minimum.
  // Pick the smaller of the nominal speeds. Higher speed shall not be achieved at the junction during coasting.
  vmax_junction = _MIN(block->nominal_speed, previous_nominal_speed);

  // Now limit the jerk in all axes.
  const float smaller_speed_factor = vmax_junction / previous_nominal_speed;
  `if` HAS_LINEAR_E_JERK
    LOOP_XYZ(axis)
  `else`
    LOOP_XYZE(axis)
  `endif`
  {
    // Limit an axis. We have to differentiate: coasting, reversal of an axis, full stop.
    float v_exit = previous_speed[axis] * smaller_speed_factor,
          v_entry = current_speed[axis];
    if (limited) {
      v_exit *= v_factor;
      v_entry *= v_factor;
    }

    // Calculate jerk depending on whether the axis is coasting in the same direction or reversing.
    const float jerk = (v_exit > v_entry)
        ? //                                  coasting             axis reversal
          ( (v_entry > 0 || v_exit < 0) ? (v_exit - v_entry) : _MAX(v_exit, -v_entry) )
        : // v_exit <= v_entry                coasting             axis reversal
          ( (v_entry < 0 || v_exit > 0) ? (v_entry - v_exit) : _MAX(-v_exit, v_entry) );

    if (jerk > settings.max_jerk[axis]) {
      v_factor *= settings.max_jerk[axis] / jerk;
      ++limited;
    }
  }
  if (limited) vmax_junction *= v_factor;
  // Now the transition velocity is known, which maximizes the shared exit / entry velocity while
  // respecting the jerk factors, it may be possible, that applying separate safe exit / entry velocities will achieve faster prints.
  const float vmax_junction_threshold = vmax_junction * 0.99f;
  if (previous_safe_speed > vmax_junction_threshold && safe_speed > vmax_junction_threshold)
    vmax_junction = safe_speed;
}
// ...
```

<a id="pyGCodeDecode.junction_handling.prusa.calc_j_vel"></a>

#### calc\_j\_vel

```python
def calc_j_vel()
```

Calculate the junction velocity.

<a id="pyGCodeDecode.junction_handling.prusa.get_junction_vel"></a>

#### get\_junction\_vel

```python
def get_junction_vel()
```

Return the calculated junction velocity.

**Returns**:

- `junction_vel` - (float) junction velocity

<a id="pyGCodeDecode.junction_handling.marlin"></a>

### marlin Objects

```python
class marlin(junction_handling)
```

Marlin classic jerk specific junction handling.

**Reference**
[https://github.com/MarlinFirmware/Marlin/pull/8887](https://github.com/MarlinFirmware/Marlin/pull/8887)
[https://github.com/MarlinFirmware/Marlin/pull/8888](https://github.com/MarlinFirmware/Marlin/pull/8888)
[https://github.com/MarlinFirmware/Marlin/issues/367#issuecomment-12505768](https://github.com/MarlinFirmware/Marlin/issues/367#issuecomment-12505768)


**Code reference:**
[Marlin/src/module/planner.cpp](https://github.com/MarlinFirmware/Marlin/blob/8ec9c379405bb9962aff170d305ddd0725bd64e2/Marlin/src/module/planner.cpp#L2762)
```cpp
// ...
float v_factor = 1.0f;
LOOP_LOGICAL_AXES(i) {
  // Jerk is the per-axis velocity difference.
  const float jerk = ABS(speed_diff[i]), maxj = max_j[i];
  if (jerk * v_factor > maxj) v_factor = maxj / jerk;
}
vmax_junction_sqr = sq(vmax_junction * v_factor);
// ...
```

<a id="pyGCodeDecode.junction_handling.marlin.calc_j_vel"></a>

#### calc\_j\_vel

```python
def calc_j_vel()
```

Calculate the junction velocity.

<a id="pyGCodeDecode.junction_handling.marlin.get_junction_vel"></a>

#### get\_junction\_vel

```python
def get_junction_vel()
```

Return the calculated junction velocity.

**Returns**:

- `junction_vel` - (float) junction velocity

<a id="pyGCodeDecode.junction_handling.ultimaker"></a>

### ultimaker Objects

```python
class ultimaker(junction_handling)
```

Ultimaker specific junction handling.

**Code reference:**
[UM2.1-Firmware/Marlin/planner.cpp](https://github.com/Ultimaker/UM2.1-Firmware/blob/f6e69344c00d7f300dace730990652ba614a2105/Marlin/planner.cpp#L840)
```cpp
// ...
float vmax_junction = max_xy_jerk/2;
float vmax_junction_factor = 1.0;
if(fabs(current_speed[Z_AXIS]) > max_z_jerk/2)
    vmax_junction = min(vmax_junction, max_z_jerk/2);
if(fabs(current_speed[E_AXIS]) > max_e_jerk/2)
    vmax_junction = min(vmax_junction, max_e_jerk/2);
vmax_junction = min(vmax_junction, block->nominal_speed);
float safe_speed = vmax_junction;

if ((moves_queued > 1) && (previous_nominal_speed > 0.0001)) {
    float xy_jerk = sqrt(square(current_speed[X_AXIS]-previous_speed[X_AXIS])+square(current_speed[Y_AXIS]-previous_speed[Y_AXIS]));
    //    if((fabs(previous_speed[X_AXIS]) > 0.0001) || (fabs(previous_speed[Y_AXIS]) > 0.0001)) {
    vmax_junction = block->nominal_speed;
    //    }
    if (xy_jerk > max_xy_jerk) {
    vmax_junction_factor = (max_xy_jerk / xy_jerk);
    }
    if(fabs(current_speed[Z_AXIS] - previous_speed[Z_AXIS]) > max_z_jerk) {
    vmax_junction_factor= min(vmax_junction_factor, (max_z_jerk/fabs(current_speed[Z_AXIS] - previous_speed[Z_AXIS])));
    }
    if(fabs(current_speed[E_AXIS] - previous_speed[E_AXIS]) > max_e_jerk) {
    vmax_junction_factor = min(vmax_junction_factor, (max_e_jerk/fabs(current_speed[E_AXIS] - previous_speed[E_AXIS])));
    }
    vmax_junction = min(previous_nominal_speed, vmax_junction * vmax_junction_factor); // Limit speed to max previous speed
}
// Max entry speed of this block equals the max exit speed of the previous block.
block->max_entry_speed = vmax_junction;
// ...
```

<a id="pyGCodeDecode.junction_handling.ultimaker.calc_j_vel"></a>

#### calc\_j\_vel

```python
def calc_j_vel()
```

Calculate the junction velocity.

<a id="pyGCodeDecode.junction_handling.ultimaker.get_junction_vel"></a>

#### get\_junction\_vel

```python
def get_junction_vel()
```

Return the calculated junction velocity.

**Returns**:

- `junction_vel` - (float) junction velocity

<a id="pyGCodeDecode.junction_handling.mka"></a>

### mka Objects

```python
class mka(prusa)
```

Anisoprint A4 like junction handling.

**Code reference:**
[anisoprint/MKA-firmware/src/core/planner/planner.cpp#L1830](https://github.com/anisoprint/MKA-firmware/blob/6e02973b1b8f325040cc3dbf66ac545ffc5c06b3/src/core/planner/planner.cpp#L1830)
```cpp
// ...
float v_exit = previous_speed[axis] * smaller_speed_factor,
        v_entry = current_speed[axis];
  if (limited) {
    v_exit *= v_factor;
    v_entry *= v_factor;
  }

  // Calculate jerk depending on whether the axis is coasting in the same direction or reversing.
  const float jerk = (v_exit > v_entry)
      ? //                                  coasting             axis reversal
        ( (v_entry > 0 || v_exit < 0) ? (v_exit - v_entry) : max(v_exit, -v_entry) )
      : // v_exit <= v_entry                coasting             axis reversal
        ( (v_entry < 0 || v_exit > 0) ? (v_entry - v_exit) : max(-v_exit, v_entry) );

  const float maxj = mechanics.max_jerk[axis];
  if (jerk > maxj) {
    v_factor *= maxj / jerk;
    ++limited;
  }
}
if (limited) vmax_junction *= v_factor;
// ...
```

<a id="pyGCodeDecode.junction_handling.junction_deviation"></a>

### junction\_deviation Objects

```python
class junction_deviation(junction_handling)
```

Marlin specific junction handling with Junction Deviation.

**Reference:**
1: [Developer Blog](https://onehossshay.wordpress.com/2011/09/24/improving_grbl_cornering_algorithm/)
2: [Kynetic CNC Blog](http://blog.kyneticcnc.com/2018/10/computing-junction-deviation-for-marlin.html)

<a id="pyGCodeDecode.junction_handling.junction_deviation.calc_JD"></a>

#### calc\_JD

```python
def calc_JD(vel_0: velocity, vel_1: velocity, p_settings: state.p_settings)
```

Calculate junction deviation velocity from 2 velocities.

**Arguments**:

- `vel_0` - (velocity) entry
- `vel_1` - (velocity) exit
- `p_settings` - (state.p_settings) print settings


**Returns**:

- `velocity` - (float) velocity abs value

<a id="pyGCodeDecode.junction_handling.junction_deviation.get_junction_vel"></a>

#### get\_junction\_vel

```python
def get_junction_vel()
```

Return junction velocity.

**Returns**:

- `junction_vel` - (float) junction velocity

<a id="pyGCodeDecode.junction_handling.get_handler"></a>

#### get\_handler

```python
def get_handler(firmware_name: str) -> type[junction_handling]
```

Get the junction handling class for the given firmware name.

**Arguments**:

- `firmware_name` - (str) name of the firmware


**Returns**:

- `junction_handling` - (type[junction_handling]) junction handling class

<a id="pyGCodeDecode.planner_block"></a>

## pyGCodeDecode.planner\_block

Planner block Module.

<a id="pyGCodeDecode.planner_block.planner_block"></a>

### planner\_block Objects

```python
class planner_block()
```

Planner Block Class.

<a id="pyGCodeDecode.planner_block.planner_block.move_maker"></a>

#### move\_maker

```python
def move_maker(v_end)
```

Calculate the correct move type (trapezoidal,triangular or singular) and generate the corresponding segments.

**Arguments**:

- `v_end` - (velocity) target velocity for end of move

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

<a id="pyGCodeDecode.planner_block.planner_block.extrusion_block_max_vel"></a>

#### extrusion\_block\_max\_vel

```python
def extrusion_block_max_vel() -> Union[np.ndarray, None]
```

Return max vel from planner block while extruding.

**Returns**:

- `block_max_vel` - (np.ndarray 1x4) maximum axis velocity while extruding in block or None
  if no extrusion is happening

<a id="pyGCodeDecode.planner_block.planner_block.calc_results"></a>

#### calc\_results

```python
def calc_results(*additional_calculators: abstract_result)
```

Calculate the result of the planner block.

<a id="pyGCodeDecode.planner_block.planner_block.prev_block"></a>

#### prev\_block

```python
@property
def prev_block()
```

Define prev_block as property.

<a id="pyGCodeDecode.planner_block.planner_block.next_block"></a>

#### next\_block

```python
@property
def next_block()
```

Define next_block as property.

<a id="pyGCodeDecode.planner_block.planner_block.get_segments"></a>

#### get\_segments

```python
def get_segments()
```

Return segments, contained by the planner block.

<a id="pyGCodeDecode.planner_block.planner_block.get_block_travel"></a>

#### get\_block\_travel

```python
def get_block_travel()
```

Return the travel length of the planner block.

<a id="pyGCodeDecode.planner_block.planner_block.inverse_time_at_pos"></a>

#### inverse\_time\_at\_pos

```python
def inverse_time_at_pos(dist_local)
```

Get the global time, at which the local length is reached.

**Arguments**:

- `dist_local` - (float) local (relative to planner block start) distance


**Returns**:

- `time_global` - (float) global time when the point will be reached.

<a id="pyGCodeDecode.plotter"></a>

## pyGCodeDecode.plotter

This module provides functionality for 3D plotting of G-code simulation data using PyVista.

Functions:
    plot_3d: Generates a 3D plot of the simulation data, with options for customization such as
             extrusion-only plotting, scalar value selection, layer selection, and saving the plot
             as a screenshot or VTK file.
    plot_2d: Generates a 2D plot of the simulation data, showing the position of the extruder head
             over time.

Dependencies:
    - pyGCodeDecode.gcode_interpreter.simulation
    - pyGCodeDecode.gcode_interpreter.unpack_blocklist
    - pyGCodeDecode.utils
    - numpy
    - pyvista
    - pathlib

<a id="pyGCodeDecode.plotter.plot_3d"></a>

#### plot\_3d

```python
def plot_3d(
    sim: simulation,
    extrusion_only: bool = True,
    scalar_value: str = "velocity",
    screenshot_path: pathlib.Path = None,
    camera_settings: dict = None,
    vtk_path: pathlib.Path = None,
    mesh: pv.MultiBlock = None,
    layer_select: int = None,
    window_size: tuple = (2048, 1536),
    mpl_subplot: bool = False,
    mpl_rcParams: Union[dict, None] = None,
    solid_color: str = "black",
    transparent_background: bool = True,
    parallel_projection: bool = False,
    lighting: bool = True,
    block_colorbar: bool = False,
    extra_plotting: callable = None,
    overwrite_labels: Union[dict, None] = None,
    scalar_value_bounds: Union[Tuple[float, float],
                               None] = None) -> pv.MultiBlock
```

3D Plot with PyVista.

**Arguments**:

- `extrusion_only` _bool, optional_ - Plot only parts where material is extruded.
  Defaults to True.
- `scalar_value` _str, optional_ - scalar value to plot. Defaults to Velocity (vel).
- `Options` - vel, rel_vel_err, or None.
- `screenshot_path` _pathlib.Path, optional_ - Path to screenshot to be saved.
  Prevents interactive plot. Defaults to None.
- `vtk_path` _pathlib.Path, optional_ - Path to vtk to be saved.
  Prevents interactive plot. Defaults to None.
- `mesh` _pv.MultiBlock, optional_ - A pyvista mesh from a previous run to
  avoid running the mesh generation again. Defaults to None.
- `layer_select` _int, optional_ - Select the layer to be plotted.
  Defaults to None, which plots all layers.
- `window_size` _tuple, optional_ - Size of the plot window.
  Defaults to (2048, 1536).
- `mpl_subplot` _bool, optional_ - Use matplotlib subplot for the screenshot.
  Defaults to False.
- `solid_color` _str, optional_ - Background color of the plot. Defaults to "black".
- `transparent_background` _bool, optional_ - Use a transparent background for
  the screenshot. Defaults to True.

**Returns**:

- `pv.MultiBlock` - The mesh used in the plot so it can be used (e.g. in subsequent plots).

<a id="pyGCodeDecode.plotter.plot_2d"></a>

#### plot\_2d

```python
def plot_2d(sim: simulation,
            filepath: pathlib.Path = pathlib.Path("trajectory_2D.png"),
            colvar="Velocity",
            show_points=False,
            colvar_spatial_resolution=1,
            dpi=400,
            scaled=True,
            show=False)
```

Plot 2D position (XY plane) with matplotlib (unmaintained).

<a id="pyGCodeDecode.plotter.plot_vel"></a>

#### plot\_vel

```python
def plot_vel(sim: simulation,
             axis: Tuple[str] = ("x", "y", "z", "e"),
             show: bool = True,
             show_planner_blocks: bool = True,
             show_segments: bool = False,
             show_jv: bool = False,
             time_steps: Union[int, str] = "constrained",
             filepath: pathlib.Path = None,
             dpi: int = 400) -> Figure
```

Plot axis velocity with matplotlib.

**Arguments**:

- `axis` - (tuple(string), default = ("x", "y", "z", "e")) select plot axis
- `show` - (bool, default = True) show plot and return plot figure
- `show_planner_blocks` - (bool, default = True) show planner_blocks as vertical lines
- `show_segments` - (bool, default = False) show segments as vertical lines
- `show_jv` - (bool, default = False) show junction velocity as x
- `time_steps` - (int or string, default = "constrained") number of time steps or constrain plot
  vertices to segment vertices
- `filepath` - (Path, default = None) save fig as image if filepath is provided
- `dpi` - (int, default = 400) select dpi


**Returns**:

  (optionally)
- `fig` - (figure)

<a id="pyGCodeDecode.result"></a>

## pyGCodeDecode.result

Result calculation for segments and planner blocks.

<a id="pyGCodeDecode.result.abstract_result"></a>

### abstract\_result Objects

```python
class abstract_result(ABC)
```

Abstract class for result calculation.

<a id="pyGCodeDecode.result.abstract_result.name"></a>

#### name

```python
@property
@abstractmethod
def name()
```

Name of the result. Has to be set in the derived class.

<a id="pyGCodeDecode.result.abstract_result.calc_pblock"></a>

#### calc\_pblock

```python
@abstractmethod
def calc_pblock(pblock: "planner_block", **kwargs)
```

Calculate the result for a planner block.

<a id="pyGCodeDecode.result.abstract_result.calc_segm"></a>

#### calc\_segm

```python
@abstractmethod
def calc_segm(segm: "segment", **kwargs)
```

Calculate the result for a segment.

<a id="pyGCodeDecode.result.acceleration_result"></a>

### acceleration\_result Objects

```python
class acceleration_result(abstract_result)
```

The acceleration.

<a id="pyGCodeDecode.result.acceleration_result.calc_segm"></a>

#### calc\_segm

```python
def calc_segm(segm: "segment", **kwargs)
```

Calculate the acceleration for a segment.

<a id="pyGCodeDecode.result.acceleration_result.calc_pblock"></a>

#### calc\_pblock

```python
def calc_pblock(pblock, **kwargs)
```

Calculate the acceleration for a planner block.

<a id="pyGCodeDecode.result.velocity_result"></a>

### velocity\_result Objects

```python
class velocity_result(abstract_result)
```

The velocity.

<a id="pyGCodeDecode.result.velocity_result.calc_segm"></a>

#### calc\_segm

```python
def calc_segm(segm: "segment", **kwargs)
```

Calculate the velocity for a segment.

<a id="pyGCodeDecode.result.velocity_result.calc_pblock"></a>

#### calc\_pblock

```python
def calc_pblock(pblock: "planner_block", **kwargs)
```

Calculate the velocity for a planner block.

<a id="pyGCodeDecode.result.get_all_result_calculators"></a>

#### get\_all\_result\_calculators

```python
def get_all_result_calculators()
```

Get all results.

<a id="pyGCodeDecode.result.has_private_results"></a>

#### has\_private\_results

```python
def has_private_results()
```

Check if private results are available.

<a id="pyGCodeDecode.result.get_result_info"></a>

#### get\_result\_info

```python
def get_result_info()
```

Get information about available result calculators.

<a id="pyGCodeDecode.state"></a>

## pyGCodeDecode.state

State module with state.

<a id="pyGCodeDecode.state.state"></a>

### state Objects

```python
class state()
```

State contains a Position and Printing Settings (p_settings) to apply for the corresponding move to this State.

<a id="pyGCodeDecode.state.state.p_settings"></a>

### p\_settings Objects

```python
class p_settings()
```

Store Printing Settings.

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

<a id="pyGCodeDecode.state.state.line_number"></a>

#### line\_number

```python
@property
def line_number()
```

Define property line_number.

<a id="pyGCodeDecode.state.state.line_number"></a>

#### line\_number

```python
@line_number.setter
def line_number(nmbr)
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

<a id="pyGCodeDecode.state_generator"></a>

## pyGCodeDecode.state\_generator

State generator module.

<a id="pyGCodeDecode.state_generator.arg_extract"></a>

#### arg\_extract

```python
def arg_extract(string: str, key_dict: dict) -> dict
```

Extract arguments from known command dictionaries.

**Arguments**:

- `string` - (str) string of Commands
- `key_dict` - (dict) dictionary with known commands and subcommands


**Returns**:

- `dict` - (dict) dictionary with all found keys and their arguments

<a id="pyGCodeDecode.state_generator.read_gcode_to_dict_list"></a>

#### read\_gcode\_to\_dict\_list

```python
def read_gcode_to_dict_list(filepath: pathlib.Path) -> List[dict]
```

Read gcode from .gcode file.

**Arguments**:

- `filepath` - (Path) filepath of the .gcode file


**Returns**:

- `dict_list` - (list[dict]) list with every line as dict

<a id="pyGCodeDecode.state_generator.dict_list_traveler"></a>

#### dict\_list\_traveler

```python
def dict_list_traveler(line_dict_list: List[dict],
                       initial_machine_setup: dict) -> List[state]
```

Convert the line dictionary to a state.

**Arguments**:

- `line_dict_list` - (dict) dict list with commands
- `initial_machine_setup` - (dict) dict with initial machine setup [absolute_position, absolute_extrusion, units, initial_position...]


**Returns**:

- `state_list` - (list[state]) all states in a list

<a id="pyGCodeDecode.state_generator.check_for_unsupported_commands"></a>

#### check\_for\_unsupported\_commands

```python
def check_for_unsupported_commands(line_dict_list: dict) -> dict
```

Search for unsupported commands used in the G-code, warn the user and return the occurrences.

**Arguments**:

- `line_dict_list` _dict_ - list of dicts containing all commands appearing


**Returns**:

- `dict` - a dict containing the appearing unsupported commands and how often they appear.

<a id="pyGCodeDecode.state_generator.generate_states"></a>

#### generate\_states

```python
def generate_states(filepath: pathlib.Path,
                    initial_machine_setup: dict) -> List[state]
```

Generate state list from GCode file.

**Arguments**:

- `filepath` - (Path) filepath to GCode
- `initial_machine_setup` - (dict) dictionary with machine setup


**Returns**:

- `states` - (list[states]) all states in a list

<a id="pyGCodeDecode.tools"></a>

## pyGCodeDecode.tools

Tools for pyGCD.

<a id="pyGCodeDecode.tools.save_layer_metrics"></a>

#### save\_layer\_metrics

```python
def save_layer_metrics(
        simulation: simulation,
        filepath: Optional[pathlib.Path] = pathlib.Path("./layer_metrics.csv"),
        locale: str = None,
        delimiter: str = ";") -> Optional[tuple[list, list, list, list]]
```

Print out print times, distance traveled and the average travel speed to a csv-file.

**Arguments**:

- `simulation` - (simulation) simulation instance
- `filepath` - (Path , default = "./layer_metrics.csv") file name
- `locale` - (string, default = None) select locale settings, e.g. "en_US.utf8", None = use system locale
- `delimiter` - (string, default = ";") select delimiter

  Layers are detected using the given layer cue.

<a id="pyGCodeDecode.tools.write_submodel_times"></a>

#### write\_submodel\_times

```python
def write_submodel_times(simulation: simulation,
                         sub_orig: list,
                         sub_side_x_len: float,
                         sub_side_y_len: float,
                         sub_side_z_len: float,
                         filename: Optional[pathlib.Path] = pathlib.Path(
                             "submodel_times.yaml"),
                         **kwargs) -> dict
```

Write the submodel entry and exit times to a yaml file.

**Arguments**:

- `simulation` - (simulation) the simulation instance to analyze
- `sub_orig` - (list with [xcoord, ycoord, zcoord]) the origin of the submodel control volume
- `sub_side_len` - (float) the side length of the submodel control volume
- `filename` - (string) yaml filename
- `**kwargs` - (any) provide additional info to write into the yaml file

<a id="pyGCodeDecode.utils"></a>

## pyGCodeDecode.utils

Utilitys.

Utils for the GCode Reader contains:
- vector 4D
    - velocity
    - position

<a id="pyGCodeDecode.utils.seconds"></a>

### seconds Objects

```python
class seconds(float)
```

A float subclass representing a time duration in seconds.

**Arguments**:

- `value` _float or int_ - The time duration in seconds.

**Examples**:

  >>> t = seconds(5)
  >>> str(t)
  '5.0 s'
  >>> t.seconds
  5.0

<a id="pyGCodeDecode.utils.seconds.seconds"></a>

#### seconds

```python
@property
def seconds()
```

Return the float value of the seconds instance.

<a id="pyGCodeDecode.utils.vector_4D"></a>

### vector\_4D Objects

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

<a id="pyGCodeDecode.utils.vector_4D.get_vec"></a>

#### get\_vec

```python
def get_vec(withExtrusion=False) -> List[float]
```

Return the 4D vector, optionally with extrusion.

**Arguments**:

- `withExtrusion` - (bool, default = False) choose if vec repr contains extrusion


**Returns**:

- `vec` - (list[3 or 4]) with (x,y,z,(optionally e))

<a id="pyGCodeDecode.utils.vector_4D.get_norm"></a>

#### get\_norm

```python
def get_norm(withExtrusion=False) -> float
```

Return the 4D vector norm. Optional with extrusion.

**Arguments**:

- `withExtrusion` - (bool, default = False) choose if norm contains extrusion


**Returns**:

- `norm` - (float) length/norm of 3D or 4D vector

<a id="pyGCodeDecode.utils.position"></a>

### position Objects

```python
class position(vector_4D)
```

4D - Position object for (Cartesian) 3D printer.

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

<a id="pyGCodeDecode.utils.velocity"></a>

### velocity Objects

```python
class velocity(vector_4D)
```

4D - Velocity object for (Cartesian) 3D printer.

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

<a id="pyGCodeDecode.utils.acceleration"></a>

### acceleration Objects

```python
class acceleration(vector_4D)
```

4D - Acceleration object for (Cartesian) 3D printer.

<a id="pyGCodeDecode.utils.segment"></a>

### segment Objects

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
- get_segm_len: returns the length of the segment.

**Class method**
- create_initial: returns the artificial initial segment where everything is at standstill, intervall length = 0
- self_check: returns True if all self checks have been successfull

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
def get_velocity(t: float) -> velocity
```

Get current velocity of segment at a certain time.

**Arguments**:

- `t` - (float) time


**Returns**:

- `current_vel` - (velocity) velocity at time t

<a id="pyGCodeDecode.utils.segment.get_velocity_by_dist"></a>

#### get\_velocity\_by\_dist

```python
def get_velocity_by_dist(dist)
```

Return the velocity at a certain local segment distance.

<a id="pyGCodeDecode.utils.segment.get_position"></a>

#### get\_position

```python
def get_position(t: float) -> position
```

Get current position of segment at a certain time.

**Arguments**:

- `t` - (float) time


**Returns**:

- `pos` - (position) position at time t

<a id="pyGCodeDecode.utils.segment.get_segm_len"></a>

#### get\_segm\_len

```python
def get_segm_len()
```

Return the length of the segment.

<a id="pyGCodeDecode.utils.segment.get_segm_duration"></a>

#### get\_segm\_duration

```python
def get_segm_duration()
```

Return the duration of the segment.

<a id="pyGCodeDecode.utils.segment.self_check"></a>

#### self\_check

```python
def self_check(p_settings: "state.p_settings" = None)
```

Check the segment for self consistency.

**Raises**:

- `ValueError` - if self check fails

**Arguments**:

- `p_settings` - (p_settings, default = None) printing settings to verify

<a id="pyGCodeDecode.utils.segment.is_extruding"></a>

#### is\_extruding

```python
def is_extruding() -> bool
```

Return true if the segment is pos. extruding.

**Returns**:

- `is_extruding` - (bool) true if positive extrusion

<a id="pyGCodeDecode.utils.segment.get_result"></a>

#### get\_result

```python
def get_result(key)
```

Return the requested result.

**Arguments**:

- `key` - (str) choose result


**Returns**:

- `result` - (list)

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
