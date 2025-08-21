# pyGCodeDecode API Reference

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

The pyGCodeDecode CLI Module.

Interact with pyGCodeDecode via the command line to run examples and plot GCode files.

Features:

- Run built-in examples: `brace`, `benchy`
- Plot GCode files with printer presets and output options
- Save simulation summaries, metrics, screenshots, and VTK files

Usage Examples:

- `pygcd --help`
- `pygcd run_example brace`
- `pygcd plot -g myfile.gcode`
- `pygcd plot -g myfile.gcode -p presets.yaml -pn my_printer`
- `pygcd plot -g myfile.gcode -o ./outputs -lc ";LAYER"`

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

<a id="pyGCodeDecode.gcode_interpreter.simulation.__init__"></a>

#### simulation.\_\_init\_\_

```python
def __init__(gcode_path: Path,
             machine_name: str = None,
             initial_machine_setup: "setup" = None,
             output_unit_system: str = "SI (mm)",
             verbosity_level: Optional[int] = None)
```

Initialize the Simulation of a given G-code with initial machine setup or default machine.

- Generate all states from GCode.
- Connect states with planner blocks, consisting of segments
- Self correct inconsistencies.

**Arguments**:

- `gcode_path` - (Path) path to GCode
- `machine_name` - (string, default = None) name of the default machine to use
- `initial_machine_setup` - (setup, default = None) setup instance
- `output_unit_system` - (string, default = "SI (mm)") available unit systems: SI, SI (mm) & inch
- `verbosity_level` - (int, default = None) set verbosity level (0: no output, 1: warnings, 2: info, 3: debug)


**Example**:

```python
gcode_interpreter.simulation(gcode_path=r"path/to/part.gcode", initial_machine_setup=printer_setup)
```

<a id="pyGCodeDecode.gcode_interpreter.simulation.__getattr__"></a>

#### simulation.\_\_getattr\_\_

```python
def __getattr__(name)
```

Get result by name.

<a id="pyGCodeDecode.gcode_interpreter.simulation.trajectory_self_correct"></a>

#### simulation.trajectory\_self\_correct

```python
def trajectory_self_correct()
```

Self correct all blocks in the blocklist with self_correction() method.

<a id="pyGCodeDecode.gcode_interpreter.simulation.calc_results"></a>

#### simulation.calc\_results

```python
def calc_results()
```

Calculate the results.

<a id="pyGCodeDecode.gcode_interpreter.simulation.calculate_averages"></a>

#### simulation.calculate\_averages

```python
def calculate_averages()
```

Calculate averages for averageable results.

<a id="pyGCodeDecode.gcode_interpreter.simulation.get_values"></a>

#### simulation.get\_values

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

#### simulation.get\_width

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

#### simulation.print\_summary

```python
def print_summary(start_time: float)
```

Print simulation summary to console.

**Arguments**:

- `start_time` _float_ - time when the simulation run was started

<a id="pyGCodeDecode.gcode_interpreter.simulation.refresh"></a>

#### simulation.refresh

```python
def refresh(new_state_list: List[state] = None)
```

Refresh simulation. Either through new state list or by rerunning the self.states as input.

**Arguments**:

- `new_state_list` - (list[state], default = None) new list of states,
  if None is provided, existing states get resimulated

<a id="pyGCodeDecode.gcode_interpreter.simulation.extrusion_extent"></a>

#### simulation.extrusion\_extent

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

#### simulation.extrusion\_max\_vel

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

#### simulation.save\_summary

```python
def save_summary(filepath: Union[Path, str])
```

Save summary to .yaml file.

**Arguments**:

- `filepath` _Path | str_ - path to summary file

  Saved data keys:
  - filename (string, filename)
  - t_end (float, end time)
  - x/y/z _min/_max (float, extent where positive extrusion)
  - max_extrusion_travel_velocity (float, maximum travel velocity where positive extrusion)

<a id="pyGCodeDecode.gcode_interpreter.simulation.get_scaling_factor"></a>

#### simulation.get\_scaling\_factor

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

<a id="pyGCodeDecode.gcode_interpreter.setup.__init__"></a>

#### setup.\_\_init\_\_

```python
def __init__(presets_file: str,
             printer: str = None,
             verbosity_level: Optional[int] = None,
             **kwargs)
```

Initialize the setup for the printing simulation.

**Arguments**:

- `presets_file` _str_ - Path to the YAML file containing printer presets.
- `printer` _str, optional_ - Name of the printer to select from the preset file. Defaults to None.
- `verbosity_level` _int, optional_ - Verbosity level for logging (0: no output, 1: warnings, 2: info, 3: debug). Defaults to None.
- `**kwargs` - Additional properties to set or override in the setup.


**Raises**:

- `ValueError` - If multiple printers are found in the preset file but none is selected.

<a id="pyGCodeDecode.gcode_interpreter.setup.__getattr__"></a>

#### setup.\_\_getattr\_\_

```python
def __getattr__(name)
```

Access to setup_dict content.

<a id="pyGCodeDecode.gcode_interpreter.setup.__setattr__"></a>

#### setup.\_\_setattr\_\_

```python
def __setattr__(name, value)
```

Set setup_dict keys.

<a id="pyGCodeDecode.gcode_interpreter.setup.load_setup"></a>

#### setup.load\_setup

```python
def load_setup(filepath, printer=None)
```

Load setup from file.

**Arguments**:

- `filepath` - (string) specify path to setup file

<a id="pyGCodeDecode.gcode_interpreter.setup.check_initial_setup"></a>

#### setup.check\_initial\_setup

```python
def check_initial_setup()
```

Check the printer Dict for typos or missing parameters and raise errors if invalid.

<a id="pyGCodeDecode.gcode_interpreter.setup.set_initial_position"></a>

#### setup.set\_initial\_position

```python
def set_initial_position(initial_position: Union[tuple, dict],
                         input_unit_system: str = None)
```

Set initial Position.

**Arguments**:

- `initial_position` - (tuple or dict) set initial position as tuple of len(4)
  or dictionary with keys: {X, Y, Z, E} or "first" to use first occuring absolute position in GCode.
- `input_unit_system` _str, optional_ - Wanted input unit system.
  Uses the one specified for the setup if None is specified.


**Example**:

```python
setup.set_initial_position((1, 2, 3, 4))
setup.set_initial_position({"X": 1, "Y": 2, "Z": 3, "E": 4})
setup.set_initial_position("first") # use first GCode position
```

<a id="pyGCodeDecode.gcode_interpreter.setup.set_property"></a>

#### setup.set\_property

```python
def set_property(property_dict: dict)
```

Overwrite or add a property to the printer dictionary.

**Arguments**:

- `property_dict` - (dict) set or add property to the setup


**Example**:

```python
setup.set_property({"layer_cue": "LAYER_CHANGE"})
```

<a id="pyGCodeDecode.gcode_interpreter.setup.get_dict"></a>

#### setup.get\_dict

```python
def get_dict() -> dict
```

Return the setup for the selected printer.

**Returns**:

- `return_dict` - (dict) setup dictionary

<a id="pyGCodeDecode.gcode_interpreter.setup.get_scaling_factor"></a>

#### setup.get\_scaling\_factor

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

#### pyGCodeDecode.helpers.VERBOSITY\_LEVEL

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

<a id="pyGCodeDecode.helpers.ProgressBar.__init__"></a>

#### ProgressBar.\_\_init\_\_

```python
def __init__(name: str = "Percent",
             barLength: int = 4,
             verbosity_level: int = 2)
```

Initialize a progress bar.

<a id="pyGCodeDecode.helpers.ProgressBar.update"></a>

#### ProgressBar.update

```python
def update(progress: float) -> None
```

Display or update a console progress bar.

**Arguments**:

- `progress` - float between 0 and 1 for percentage, < 0 represents a 'halt', > 1 represents 100%

<a id="pyGCodeDecode.junction_handling"></a>

## pyGCodeDecode.junction\_handling

Junction handling module for calculating the velocity at junctions.

<a id="pyGCodeDecode.junction_handling.junction_handling"></a>

### junction\_handling Objects

```python
class junction_handling()
```

Junction handling super class.

<a id="pyGCodeDecode.junction_handling.junction_handling.__init__"></a>

#### junction\_handling.\_\_init\_\_

```python
def __init__(state_A: state, state_B: state)
```

Initialize the junction handling.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state

<a id="pyGCodeDecode.junction_handling.junction_handling.connect_state"></a>

#### junction\_handling.connect\_state

```python
def connect_state(state_A: state, state_B: state)
```

Connect two states and generates the velocity for the move from state_A to state_B.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state


**Returns**:

- `velocity` - (float) the target velocity for that travel move

<a id="pyGCodeDecode.junction_handling.junction_handling.get_target_vel"></a>

#### junction\_handling.get\_target\_vel

```python
def get_target_vel()
```

Return target velocity.

<a id="pyGCodeDecode.junction_handling.junction_handling.get_junction_vel"></a>

#### junction\_handling.get\_junction\_vel

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

<a id="pyGCodeDecode.junction_handling.prusa.__init__"></a>

#### prusa.\_\_init\_\_

```python
def __init__(state_A: state, state_B: state)
```

Marlin classic jerk specific junction velocity calculation.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state

<a id="pyGCodeDecode.junction_handling.prusa.calc_j_vel"></a>

#### prusa.calc\_j\_vel

```python
def calc_j_vel()
```

Calculate the junction velocity.

<a id="pyGCodeDecode.junction_handling.prusa.get_junction_vel"></a>

#### prusa.get\_junction\_vel

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

<a id="pyGCodeDecode.junction_handling.marlin.__init__"></a>

#### marlin.\_\_init\_\_

```python
def __init__(state_A: state, state_B: state)
```

Marlin classic jerk specific junction velocity calculation.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state

<a id="pyGCodeDecode.junction_handling.marlin.calc_j_vel"></a>

#### marlin.calc\_j\_vel

```python
def calc_j_vel()
```

Calculate the junction velocity.

<a id="pyGCodeDecode.junction_handling.marlin.get_junction_vel"></a>

#### marlin.get\_junction\_vel

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

<a id="pyGCodeDecode.junction_handling.ultimaker.__init__"></a>

#### ultimaker.\_\_init\_\_

```python
def __init__(state_A: state, state_B: state)
```

Ultimaker specific junction velocity calculation.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state

<a id="pyGCodeDecode.junction_handling.ultimaker.calc_j_vel"></a>

#### ultimaker.calc\_j\_vel

```python
def calc_j_vel()
```

Calculate the junction velocity.

<a id="pyGCodeDecode.junction_handling.ultimaker.get_junction_vel"></a>

#### ultimaker.get\_junction\_vel

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

Anisoprint Composer models using MKA Firmware junction handling.

The MKA firmware uses a similar approach to Prusa's classic jerk handling.

**Code reference:**
[anisoprint/MKA-firmware/src/core/planner/planner.cpp](https://github.com/anisoprint/MKA-firmware/blob/6e02973b1b8f325040cc3dbf66ac545ffc5c06b3/src/core/planner/planner.cpp#L1830)
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

#### junction\_deviation.calc\_JD

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

<a id="pyGCodeDecode.junction_handling.junction_deviation.__init__"></a>

#### junction\_deviation.\_\_init\_\_

```python
def __init__(state_A: state, state_B: state)
```

Marlin specific junction velocity calculation with Junction Deviation.

**Arguments**:

- `state_A` - (state) start state
- `state_B` - (state)   end state

<a id="pyGCodeDecode.junction_handling.junction_deviation.get_junction_vel"></a>

#### junction\_deviation.get\_junction\_vel

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

#### planner\_block.move\_maker

```python
def move_maker(v_end)
```

Calculate the correct move type (trapezoidal,triangular or singular) and generate the corresponding segments.

**Arguments**:

- `v_end` - (velocity) target velocity for end of move

<a id="pyGCodeDecode.planner_block.planner_block.self_correction"></a>

#### planner\_block.self\_correction

```python
def self_correction(tolerance=float("1e-12"))
```

Check for interfacing vel and self correct.

<a id="pyGCodeDecode.planner_block.planner_block.timeshift"></a>

#### planner\_block.timeshift

```python
def timeshift(delta_t: float)
```

Shift planner block in time.

**Arguments**:

- `delta_t` - (float) time to be shifted

<a id="pyGCodeDecode.planner_block.planner_block.extrusion_block_max_vel"></a>

#### planner\_block.extrusion\_block\_max\_vel

```python
def extrusion_block_max_vel() -> Union[np.ndarray, None]
```

Return max vel from planner block while extruding.

**Returns**:

- `block_max_vel` - (np.ndarray 1x4) maximum axis velocity while extruding in block or None
  if no extrusion is happening

<a id="pyGCodeDecode.planner_block.planner_block.calc_results"></a>

#### planner\_block.calc\_results

```python
def calc_results(*additional_calculators: abstract_result)
```

Calculate the result of the planner block.

<a id="pyGCodeDecode.planner_block.planner_block.__init__"></a>

#### planner\_block.\_\_init\_\_

```python
def __init__(state: state, prev_block: "planner_block", firmware=None)
```

Calculate and store planner block consisting of one or multiple segments.

**Arguments**:

- `state` - (state) the current state
- `prev_block` - (planner_block) previous planner block
- `firmware` - (string, default = None) firmware selection for junction

<a id="pyGCodeDecode.planner_block.planner_block.prev_block"></a>

#### planner\_block.prev\_block

```python
@property
def prev_block()
```

Define prev_block as property.

<a id="pyGCodeDecode.planner_block.planner_block.next_block"></a>

#### planner\_block.next\_block

```python
@property
def next_block()
```

Define next_block as property.

<a id="pyGCodeDecode.planner_block.planner_block.__str__"></a>

#### planner\_block.\_\_str\_\_

```python
def __str__() -> str
```

Create string from planner block.

<a id="pyGCodeDecode.planner_block.planner_block.__repr__"></a>

#### planner\_block.\_\_repr\_\_

```python
def __repr__() -> str
```

Represent planner block.

<a id="pyGCodeDecode.planner_block.planner_block.get_segments"></a>

#### planner\_block.get\_segments

```python
def get_segments()
```

Return segments, contained by the planner block.

<a id="pyGCodeDecode.planner_block.planner_block.get_block_travel"></a>

#### planner\_block.get\_block\_travel

```python
def get_block_travel()
```

Return the travel length of the planner block.

<a id="pyGCodeDecode.planner_block.planner_block.inverse_time_at_pos"></a>

#### planner\_block.inverse\_time\_at\_pos

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

<a id="pyGCodeDecode.plotter.plot_3d"></a>

#### plot\_3d

```python
def plot_3d(sim: simulation,
            extrusion_only: bool = True,
            scalar_value: str = "velocity",
            screenshot_path: pathlib.Path = None,
            camera_settings: dict = None,
            vtk_path: pathlib.Path = None,
            mesh: pv.MultiBlock = None,
            layer_select: int = None,
            z_scaler: float = None,
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
            scalar_value_bounds: Union[Tuple[float, float], None] = None,
            return_type: str = "mesh") -> pv.MultiBlock
```

Plot a 3D visualization of G-code simulation data using PyVista.

**Arguments**:

- `sim` _simulation_ - The simulation object containing blocklist and segment data.
- `extrusion_only` _bool, optional_ - If True, plot only segments where extrusion occurs. Defaults to True.
- `scalar_value` _str, optional_ - Scalar value to color the plot. Options: "velocity", "rel_vel_err", "acceleration", or None. Defaults to "velocity".
- `screenshot_path` _pathlib.Path, optional_ - If provided, saves a screenshot to this path and disables interactive plotting. Defaults to None.
- `camera_settings` _dict, optional_ - Camera settings for the plotter. Keys: "camera_position", "elevation", "azimuth", "roll". Defaults to None.
- `vtk_path` _pathlib.Path, optional_ - If provided, saves the mesh as a VTK file to this path. Defaults to None.
- `mesh` _pv.MultiBlock, optional_ - Precomputed PyVista mesh to use instead of generating a new one. Defaults to None.
- `layer_select` _int, optional_ - If provided, only plot the specified layer. Defaults to None (all layers).
- `z_scaler` _float, optional_ - Scaling factor for the z-axis layer squishing (z_scaler = width/height of extrusion). Defaults to None (automatic scaling).
- `window_size` _tuple, optional_ - Size of the plot window in pixels. Defaults to (2048, 1536).
- `mpl_subplot` _bool, optional_ - If True, use matplotlib for screenshot and colorbar. Defaults to False.
- `mpl_rcParams` _dict or None, optional_ - Custom matplotlib rcParams for styling. Defaults to None.
- `solid_color` _str, optional_ - Background color for the plot. Defaults to "black".
- `transparent_background` _bool, optional_ - If True, screenshot background is transparent. Defaults to True.
- `parallel_projection` _bool, optional_ - If True, enables parallel projection in PyVista. Defaults to False.
- `lighting` _bool, optional_ - If True, enables lighting in the plot. Defaults to True.
- `block_colorbar` _bool, optional_ - If True, removes the scalar colorbar from the plot. Defaults to False.
- `extra_plotting` _callable, optional_ - Function to add extra plotting to the PyVista plotter. Signature: (plotter, mesh). Defaults to None.
- `overwrite_labels` _dict or None, optional_ - Dictionary to overwrite colorbar labels. Defaults to None.
- `scalar_value_bounds` _tuple or None, optional_ - Tuple (min, max) to set scalar colorbar range. Defaults to None.
- `return_type` _str, optional_ - Return type, "mesh" or "image". Defaults to "mesh".


**Returns**:

- `pv.MultiBlock` - The PyVista mesh used for plotting.
  or
- `np.ndarray` - The screenshot image if `screenshot_path` is provided and `return_type` is "image".

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

#### abstract\_result.name

```python
@property
@abstractmethod
def name()
```

Name of the result. Has to be set in the derived class.

<a id="pyGCodeDecode.result.abstract_result.calc_pblock"></a>

#### abstract\_result.calc\_pblock

```python
@abstractmethod
def calc_pblock(pblock: "planner_block", **kwargs)
```

Calculate the result for a planner block.

<a id="pyGCodeDecode.result.abstract_result.calc_segm"></a>

#### abstract\_result.calc\_segm

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

#### acceleration\_result.calc\_segm

```python
def calc_segm(segm: "segment", **kwargs)
```

Calculate the acceleration for a segment.

<a id="pyGCodeDecode.result.acceleration_result.calc_pblock"></a>

#### acceleration\_result.calc\_pblock

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

#### velocity\_result.calc\_segm

```python
def calc_segm(segm: "segment", **kwargs)
```

Calculate the velocity for a segment.

<a id="pyGCodeDecode.result.velocity_result.calc_pblock"></a>

#### velocity\_result.calc\_pblock

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

<a id="pyGCodeDecode.state.state.p_settings.__init__"></a>

#### p\_settings.\_\_init\_\_

```python
def __init__(p_acc, jerk, vX, vY, vZ, vE, speed, units="SI (mm)")
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
- `units` - (string, default = "SI (mm)") unit settings

<a id="pyGCodeDecode.state.state.p_settings.__str__"></a>

#### p\_settings.\_\_str\_\_

```python
def __str__() -> str
```

Create summary string for p_settings.

<a id="pyGCodeDecode.state.state.p_settings.__repr__"></a>

#### p\_settings.\_\_repr\_\_

```python
def __repr__() -> str
```

Define representation.

<a id="pyGCodeDecode.state.state.__init__"></a>

#### state.\_\_init\_\_

```python
def __init__(state_position: position = None,
             state_p_settings: p_settings = None)
```

Initialize a state.

**Arguments**:

- `state_position` - (position) state position
- `state_p_settings` - (p_settings) state printing settings

<a id="pyGCodeDecode.state.state.state_position"></a>

#### state.state\_position

```python
@property
def state_position()
```

Define property state_position.

<a id="pyGCodeDecode.state.state.state_p_settings"></a>

#### state.state\_p\_settings

```python
@property
def state_p_settings()
```

Define property state_p_settings.

<a id="pyGCodeDecode.state.state.line_number"></a>

#### state.line\_number

```python
@property
def line_number()
```

Define property line_number.

<a id="pyGCodeDecode.state.state.line_number"></a>

#### state.line\_number

```python
@line_number.setter
def line_number(nmbr)
```

Set line number.

**Arguments**:

- `nmbr` - (int) line number

<a id="pyGCodeDecode.state.state.next_state"></a>

#### state.next\_state

```python
@property
def next_state()
```

Define property next_state.

<a id="pyGCodeDecode.state.state.next_state"></a>

#### state.next\_state

```python
@next_state.setter
def next_state(state: "state")
```

Set next state.

**Arguments**:

- `state` - (state) next state

<a id="pyGCodeDecode.state.state.prev_state"></a>

#### state.prev\_state

```python
@property
def prev_state()
```

Define property prev_state.

<a id="pyGCodeDecode.state.state.prev_state"></a>

#### state.prev\_state

```python
@prev_state.setter
def prev_state(state: "state")
```

Set previous state.

**Arguments**:

- `state` - (state) previous state

<a id="pyGCodeDecode.state.state.__str__"></a>

#### state.\_\_str\_\_

```python
def __str__() -> str
```

Generate string for representation.

<a id="pyGCodeDecode.state.state.__repr__"></a>

#### state.\_\_repr\_\_

```python
def __repr__() -> str
```

Call __str__() for representation.

<a id="pyGCodeDecode.state_generator"></a>

## pyGCodeDecode.state\_generator

State generator module.

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

Utilities.

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

```python
>>> from pyGCodeDecode.utils import seconds
>>> t = seconds(5)
>>> str(t)
'5.0 s'
>>> t.seconds
5.0
```

<a id="pyGCodeDecode.utils.seconds.__new__"></a>

#### seconds.\_\_new\_\_

```python
def __new__(cls, value)
```

Create a new instance of seconds.

<a id="pyGCodeDecode.utils.seconds.__str__"></a>

#### seconds.\_\_str\_\_

```python
def __str__() -> str
```

Return string representation of the time in seconds.

<a id="pyGCodeDecode.utils.seconds.__sub__"></a>

#### seconds.\_\_sub\_\_

```python
def __sub__(other) -> "seconds"
```

Subtract seconds or float and return a new seconds instance.

<a id="pyGCodeDecode.utils.seconds.__add__"></a>

#### seconds.\_\_add\_\_

```python
def __add__(other) -> "seconds"
```

Add seconds or float and return a new seconds instance.

<a id="pyGCodeDecode.utils.seconds.__repr__"></a>

#### seconds.\_\_repr\_\_

```python
def __repr__() -> str
```

Return a string representation of the seconds object.

<a id="pyGCodeDecode.utils.seconds.seconds"></a>

#### seconds.seconds

```python
@property
def seconds() -> float
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

<a id="pyGCodeDecode.utils.vector_4D.__init__"></a>

#### vector\_4D.\_\_init\_\_

```python
def __init__(*args)
```

Store 3D position + extrusion axis.

**Arguments**:

- `args` - coordinates as arguments x,y,z,e or (tuple or list) [x,y,z,e]

<a id="pyGCodeDecode.utils.vector_4D.__str__"></a>

#### vector\_4D.\_\_str\_\_

```python
def __str__() -> str
```

Return string representation.

<a id="pyGCodeDecode.utils.vector_4D.__repr__"></a>

#### vector\_4D.\_\_repr\_\_

```python
def __repr__()
```

Return a string representation of the 4D vector.

<a id="pyGCodeDecode.utils.vector_4D.__add__"></a>

#### vector\_4D.\_\_add\_\_

```python
def __add__(other)
```

Add functionality for 4D vectors.

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')


**Returns**:

- `add` - (self) component wise addition

<a id="pyGCodeDecode.utils.vector_4D.__sub__"></a>

#### vector\_4D.\_\_sub\_\_

```python
def __sub__(other)
```

Sub functionality for 4D vectors.

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')


**Returns**:

- `sub` - (self) component wise subtraction

<a id="pyGCodeDecode.utils.vector_4D.__mul__"></a>

#### vector\_4D.\_\_mul\_\_

```python
def __mul__(other)
```

Scalar multiplication functionality for 4D vectors.

**Arguments**:

- `other` - (float or int)


**Returns**:

- `mul` - (self) scalar multiplication, scaling

<a id="pyGCodeDecode.utils.vector_4D.__truediv__"></a>

#### vector\_4D.\_\_truediv\_\_

```python
def __truediv__(other)
```

Scalar division functionality for 4D Vectors.

**Arguments**:

- `other` - (float or int)


**Returns**:

- `div` - (self) scalar division, scaling

<a id="pyGCodeDecode.utils.vector_4D.__eq__"></a>

#### vector\_4D.\_\_eq\_\_

```python
def __eq__(other) -> bool
```

Check for equality and return True if equal (with tolerance).

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')


**Returns**:

- `eq` - (bool) true if equal (with tolerance)

<a id="pyGCodeDecode.utils.vector_4D.__gt__"></a>

#### vector\_4D.\_\_gt\_\_

```python
def __gt__(other) -> bool
```

Check for greater than and return True if greater.

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')


**Returns**:

- `gt` - (bool) true if greater

<a id="pyGCodeDecode.utils.vector_4D.get_vec"></a>

#### vector\_4D.get\_vec

```python
def get_vec(withExtrusion: bool = False) -> List[float]
```

Return the 4D vector, optionally with extrusion.

**Arguments**:

- `withExtrusion` - (bool, default = False) choose if vec repr contains extrusion


**Returns**:

- `vec` - (list[3 or 4]) with (x,y,z,(optionally e))

<a id="pyGCodeDecode.utils.vector_4D.get_norm"></a>

#### vector\_4D.get\_norm

```python
def get_norm(withExtrusion: bool = False) -> float
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

<a id="pyGCodeDecode.utils.position.__str__"></a>

#### position.\_\_str\_\_

```python
def __str__() -> str
```

Print out position.

<a id="pyGCodeDecode.utils.position.is_travel"></a>

#### position.is\_travel

```python
def is_travel(other) -> bool
```

Return True if there is travel between self and other position.

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')


**Returns**:

- `is_travel` - (bool) true if between self and other is distance

<a id="pyGCodeDecode.utils.position.is_extruding"></a>

#### position.is\_extruding

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

#### position.get\_t\_distance

```python
def get_t_distance(other=None, withExtrusion: bool = False) -> float
```

Calculate the travel distance between self and other position. If none is provided, zero will be used.

**Arguments**:

- `other` - (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray', default = None)
- `withExtrusion` - (bool, default = False) use or ignore extrusion


**Returns**:

- `travel` - (float) travel or extrusion and travel distance

<a id="pyGCodeDecode.utils.position.__truediv__"></a>

#### position.\_\_truediv\_\_

```python
def __truediv__(other)
```

Divide position by seconds to get velocity.

<a id="pyGCodeDecode.utils.velocity"></a>

### velocity Objects

```python
class velocity(vector_4D)
```

4D - Velocity object for (Cartesian) 3D printer.

<a id="pyGCodeDecode.utils.velocity.__str__"></a>

#### velocity.\_\_str\_\_

```python
def __str__() -> str
```

Print out velocity.

<a id="pyGCodeDecode.utils.velocity.get_norm_dir"></a>

#### velocity.get\_norm\_dir

```python
def get_norm_dir(withExtrusion: bool = False) -> Optional[np.ndarray]
```

Get normalized direction vector as numpy array.

If only extrusion occurs and withExtrusion=True, normalize to the extrusion length.

Returns None if both travel and extrusion are zero.

<a id="pyGCodeDecode.utils.velocity.not_zero"></a>

#### velocity.not\_zero

```python
def not_zero() -> bool
```

Return True if velocity is not zero.

**Returns**:

- `not_zero` - (bool) true if velocity is not zero

<a id="pyGCodeDecode.utils.velocity.is_extruding"></a>

#### velocity.is\_extruding

```python
def is_extruding() -> bool
```

Return True if extrusion velocity is greater than zero.

**Returns**:

- `is_extruding` - (bool) true if positive extrusion velocity

<a id="pyGCodeDecode.utils.velocity.__mul__"></a>

#### velocity.\_\_mul\_\_

```python
def __mul__(other)
```

Multiply velocity by a time to get position, or by scalar.

<a id="pyGCodeDecode.utils.velocity.__truediv__"></a>

#### velocity.\_\_truediv\_\_

```python
def __truediv__(other)
```

Divide velocity by scalar.

<a id="pyGCodeDecode.utils.acceleration"></a>

### acceleration Objects

```python
class acceleration(vector_4D)
```

4D - Acceleration object for (Cartesian) 3D printer.

<a id="pyGCodeDecode.utils.acceleration.__str__"></a>

#### acceleration.\_\_str\_\_

```python
def __str__() -> str
```

Print out acceleration.

<a id="pyGCodeDecode.utils.acceleration.__mul__"></a>

#### acceleration.\_\_mul\_\_

```python
def __mul__(other)
```

Multiply acceleration by a time to get velocity, or by scalar.

<a id="pyGCodeDecode.utils.acceleration.__truediv__"></a>

#### acceleration.\_\_truediv\_\_

```python
def __truediv__(other)
```

Divide acceleration by scalar.

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

<a id="pyGCodeDecode.utils.segment.__init__"></a>

#### segment.\_\_init\_\_

```python
def __init__(t_begin: Union[float, seconds],
             t_end: Union[float, seconds],
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

#### segment.\_\_str\_\_

```python
def __str__() -> str
```

Create string from segment.

<a id="pyGCodeDecode.utils.segment.__repr__"></a>

#### segment.\_\_repr\_\_

```python
def __repr__()
```

Segment representation.

<a id="pyGCodeDecode.utils.segment.move_segment_time"></a>

#### segment.move\_segment\_time

```python
def move_segment_time(delta_t: Union[float, seconds]) -> None
```

Move segment in time.

**Arguments**:

- `delta_t` - (float) time to be shifted

<a id="pyGCodeDecode.utils.segment.get_velocity"></a>

#### segment.get\_velocity

```python
def get_velocity(t: Union[float, seconds]) -> velocity
```

Get current velocity of segment at a certain time.

**Arguments**:

- `t` - (float) time


**Returns**:

- `current_vel` - (velocity) velocity at time t

<a id="pyGCodeDecode.utils.segment.get_velocity_by_dist"></a>

#### segment.get\_velocity\_by\_dist

```python
def get_velocity_by_dist(dist: float) -> float
```

Return the velocity magnitude at a certain local segment distance.

**Arguments**:

- `dist` - (float) distance from segment start

<a id="pyGCodeDecode.utils.segment.get_position"></a>

#### segment.get\_position

```python
def get_position(t: Union[float, seconds]) -> position
```

Get current position of segment at a certain time.

**Arguments**:

- `t` - (float) time


**Returns**:

- `pos` - (position) position at time t

<a id="pyGCodeDecode.utils.segment.get_segm_len"></a>

#### segment.get\_segm\_len

```python
def get_segm_len() -> float
```

Return the length of the segment.

<a id="pyGCodeDecode.utils.segment.get_segm_duration"></a>

#### segment.get\_segm\_duration

```python
def get_segm_duration() -> seconds
```

Return the duration of the segment.

<a id="pyGCodeDecode.utils.segment.self_check"></a>

#### segment.self\_check

```python
def self_check(p_settings: "state.p_settings" = None) -> bool
```

Check the segment for self consistency.

**Raises**:

- `ValueError` - if self check fails

**Arguments**:

- `p_settings` - (p_settings, default = None) printing settings to verify

**Returns**:

  True if all checks pass

<a id="pyGCodeDecode.utils.segment.is_extruding"></a>

#### segment.is\_extruding

```python
def is_extruding() -> bool
```

Return true if the segment is pos. extruding.

**Returns**:

- `is_extruding` - (bool) true if positive extrusion

<a id="pyGCodeDecode.utils.segment.get_result"></a>

#### segment.get\_result

```python
def get_result(key: str)
```

Return the requested result.

**Arguments**:

- `key` - (str) choose result


**Returns**:

- `result` - (list)

<a id="pyGCodeDecode.utils.segment.create_initial"></a>

#### segment.create\_initial

```python
@classmethod
def create_initial(cls,
                   initial_position: Optional[position] = None) -> "segment"
```

Create initial static segment with (optionally) initial position else start from Zero.

**Arguments**:

- `initial_position` - (postion, default = None) position to begin segment series


**Returns**:

- `segment` - (segment) initial beginning segment
