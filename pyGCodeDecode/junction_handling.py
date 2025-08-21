"""Junction handling module for calculating the velocity at junctions."""

import inspect
import sys

import numpy as np

from pyGCodeDecode.helpers import custom_print

from .state import state
from .utils import velocity


class junction_handling:
    """Junction handling super class."""

    def __init__(self, state_A: state, state_B: state):
        """Initialize the junction handling.

        Args:
            state_A: (state) start state
            state_B: (state)   end state
        """
        self.state_A = state_A
        self.state_B = state_B
        self.target_vel = self.connect_state(state_A=state_A, state_B=state_B)
        self.vel_next = self._calc_vel_next()

    def connect_state(self, state_A: state, state_B: state):
        """
        Connect two states and generates the velocity for the move from state_A to state_B.

        Args:
            state_A: (state) start state
            state_B: (state)   end state

        Returns:
            velocity: (float) the target velocity for that travel move
        """
        if state_A is None or state_B is None:
            return velocity(0, 0, 0, 0)

        travel_direction = np.asarray((state_B.state_position - state_A.state_position).get_vec(withExtrusion=True))
        self.t_distance = np.linalg.norm(travel_direction[:3])
        e_len = travel_direction[3]
        if abs(self.t_distance) > 0:  # regular travel mixed move
            travel_direction = travel_direction / self.t_distance
        elif abs(e_len) > 0:  # for extrusion only move
            travel_direction = travel_direction / abs(e_len)
        else:  # no move at all
            travel_direction = np.asarray([0, 0, 0, 0])
        target_vel = velocity(state_B.state_p_settings.speed * travel_direction)
        return target_vel

    def _calc_vel_next(self):
        """Return the target velocity for the following move."""
        next_next_state = self.state_B.next_state if self.state_B.next_state is not None else self.state_B
        while True:
            if (
                next_next_state.next_state is None
                or self.state_B.state_position != next_next_state.state_position
                # or self.state_B.state_position.get_t_distance(next_next_state.state_position, withExtrusion=True) > 0  # inefficient check
            ):
                vel_next = self.connect_state(
                    state_A=self.state_B, state_B=next_next_state
                )  # target velocity for next planner block
                break
            else:
                next_next_state = next_next_state.next_state
        return vel_next

    def get_target_vel(self):
        """Return target velocity."""
        return self.target_vel

    def get_junction_vel(self):
        """Return default junction velocity of zero.

        Returns:
            0: zero for default full stop junction handling
        """
        return 0


class prusa(junction_handling):
    """Prusa specific classic jerk junction handling (validated on Prusa Mini).

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
      #if HAS_LINEAR_E_JERK
        LOOP_XYZ(axis)
      #else
        LOOP_XYZE(axis)
      #endif
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
    """

    def __init__(self, state_A: state, state_B: state):
        """Marlin classic jerk specific junction velocity calculation.

        Args:
            state_A: (state) start state
            state_B: (state)   end state
        """
        super().__init__(state_A, state_B)

        self.calc_j_vel()

    def calc_j_vel(self):
        """Calculate the junction velocity."""
        vel_0 = self.target_vel
        vel_1 = self.vel_next
        self.jerk = self.state_B.state_p_settings.jerk

        v_max_junction = min(vel_0.get_norm(), vel_1.get_norm())
        smaller_speed_factor = v_max_junction / vel_0.get_norm() if v_max_junction > 0 else 0

        v_factor = 1.0
        limited = False

        for axis in range(4):  # Include extrusion axis
            v_exit = vel_0.get_vec(withExtrusion=True)[axis] * smaller_speed_factor
            v_entry = vel_1.get_vec(withExtrusion=True)[axis]

            if limited:
                v_exit *= v_factor
                v_entry *= v_factor

            # Calculate jerk depending on whether the axis is coasting in the same direction or reversing
            if v_exit > v_entry:
                # coasting: (v_entry > 0 or v_exit < 0), axis reversal: else
                jerk = (v_exit - v_entry) if (v_entry > 0 or v_exit < 0) else max(v_exit, -v_entry)
            else:
                # coasting: (v_entry < 0 or v_exit > 0), axis reversal: else
                jerk = (v_entry - v_exit) if (v_entry < 0 or v_exit > 0) else max(-v_exit, v_entry)

            if jerk > self.jerk:
                v_factor *= self.jerk / jerk
                limited = True

        if limited:
            v_max_junction *= v_factor

        self.junction_vel = v_max_junction

    def get_junction_vel(self):
        """Return the calculated junction velocity.

        Returns:
            junction_vel: (float) junction velocity
        """
        return self.junction_vel


class marlin(junction_handling):
    """Marlin classic jerk specific junction handling.

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
    """

    """"    **Reference**
    [https://github.com/MarlinFirmware/Marlin/pull/8887](https://github.com/MarlinFirmware/Marlin/pull/8887)
    [https://github.com/MarlinFirmware/Marlin/pull/8888](https://github.com/MarlinFirmware/Marlin/pull/8888)
    [https://github.com/MarlinFirmware/Marlin/issues/367#issuecomment-12505768](https://github.com/MarlinFirmware/Marlin/issues/367#issuecomment-12505768)
    """

    def __init__(self, state_A: state, state_B: state):
        """Marlin classic jerk specific junction velocity calculation.

        Args:
            state_A: (state) start state
            state_B: (state)   end state
        """
        super().__init__(state_A, state_B)

        self.calc_j_vel()

    def calc_j_vel(self):
        """Calculate the junction velocity."""
        vel_0 = self.target_vel
        vel_1 = self.vel_next
        self.jerk = self.state_B.state_p_settings.jerk

        vel_diff = vel_0 - vel_1

        scale = 1.0
        for axx in range(4):
            ax_jerk = abs(vel_diff.get_vec(withExtrusion=True)[axx])
            if ax_jerk * scale > self.jerk:
                scale = self.jerk / ax_jerk

        if scale < 1:
            self.junction_vel = (vel_0 * scale).get_norm()
        else:
            self.junction_vel = vel_0.get_norm()

    def get_junction_vel(self):
        """Return the calculated junction velocity.

        Returns:
            junction_vel: (float) junction velocity
        """
        return self.junction_vel


class ultimaker(junction_handling):
    """Ultimaker specific junction handling.

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
    """

    def __init__(self, state_A: state, state_B: state):
        """Ultimaker specific junction velocity calculation.

        Args:
            state_A: (state) start state
            state_B: (state)   end state
        """
        super().__init__(state_A, state_B)
        self.calc_j_vel()

    def calc_j_vel(self):
        """Calculate the junction velocity."""
        vel_0 = self.target_vel
        vel_1 = self.vel_next
        p_settings = self.state_B.state_p_settings

        # max jerk values
        max_xy_jerk = p_settings.jerk
        max_z_jerk = getattr(p_settings, "jerk_z", p_settings.jerk)
        max_e_jerk = getattr(p_settings, "jerk_e", p_settings.jerk)

        # current and previous speeds
        curr_speed = vel_1.get_vec(withExtrusion=True)
        prev_speed = vel_0.get_vec(withExtrusion=True)

        # XY jerk
        xy_jerk = np.sqrt((curr_speed[0] - prev_speed[0]) ** 2 + (curr_speed[1] - prev_speed[1]) ** 2)
        z_jerk = abs(curr_speed[2] - prev_speed[2])
        e_jerk = abs(curr_speed[3] - prev_speed[3])

        # Initial vmax_junction
        vmax_junction = max_xy_jerk / 2.0
        vmax_junction_factor = 1.0

        if abs(curr_speed[2]) > max_z_jerk / 2.0:
            vmax_junction = min(vmax_junction, max_z_jerk / 2.0)
        if abs(curr_speed[3]) > max_e_jerk / 2.0:
            vmax_junction = min(vmax_junction, max_e_jerk / 2.0)

        vmax_junction = min(vmax_junction, vel_1.get_norm())
        # safe_speed = vmax_junction

        # If there is a previous move (simulate moves_queued > 1)
        if vel_0.get_norm() > 0.0001:
            vmax_junction = vel_1.get_norm()
            if xy_jerk > max_xy_jerk:
                vmax_junction_factor = max_xy_jerk / xy_jerk
            if z_jerk > max_z_jerk:
                vmax_junction_factor = min(vmax_junction_factor, max_z_jerk / z_jerk)
            if e_jerk > max_e_jerk:
                vmax_junction_factor = min(vmax_junction_factor, max_e_jerk / e_jerk)
            vmax_junction = min(vel_0.get_norm(), vmax_junction * vmax_junction_factor)

        self.junction_vel = vmax_junction

    def get_junction_vel(self):
        """Return the calculated junction velocity.

        Returns:
            junction_vel: (float) junction velocity
        """
        return self.junction_vel


class mka(prusa):
    """Anisoprint Composer models using MKA Firmware junction handling.

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

    """

    # MKA is similar to Prusa jerk handling


class junction_deviation(junction_handling):
    """Marlin specific junction handling with Junction Deviation.

    **Reference:**
    1: [Developer Blog](https://onehossshay.wordpress.com/2011/09/24/improving_grbl_cornering_algorithm/)
    2: [Kynetic CNC Blog](http://blog.kyneticcnc.com/2018/10/computing-junction-deviation-for-marlin.html)
    """

    def calc_JD(self, vel_0: velocity, vel_1: velocity, p_settings: state.p_settings):
        """Calculate junction deviation velocity from 2 velocities.

        Args:
            vel_0: (velocity) entry
            vel_1: (velocity) exit
            p_settings: (state.p_settings) print settings

        Returns:
            velocity: (float) velocity abs value
        """
        # Junction deviation settings
        JD_acc = p_settings.p_acc
        if p_settings.jerk == 0:
            return 0
        JD_delta = 0.414 * p_settings.jerk * p_settings.jerk / JD_acc  # [2]
        JD_minAngle = 18
        JD_maxAngle = 180 - 18
        vel_0_vec = vel_0.get_vec()
        vel_1_vec = vel_1.get_vec()
        if vel_0.get_norm() == 0 or vel_1.get_norm() == 0:
            return 0
        # calculate junction angle
        JD_cos_theta = np.dot(-np.asarray(vel_0_vec), np.asarray(vel_1_vec)) / (
            np.linalg.norm(vel_0_vec) * np.linalg.norm(vel_1_vec)
        )  # cos of theta, theta: small angle between velocity vectors
        if JD_cos_theta < 1:  # catch numerical errors where cos theta is slightly larger than one
            JD_sin_theta_half = np.sqrt((1 - JD_cos_theta) / 2)
        else:
            JD_sin_theta_half = 0
        if JD_sin_theta_half < np.sin(JD_maxAngle * np.pi / (2 * 180)):  # smaller than max angle
            if JD_sin_theta_half > np.sin(
                JD_minAngle * np.pi / (2 * 180)
            ):  # and larger than min angle --> apply Junction Deviation Calculation
                # calculate scalar junction velocity
                JD_Radius = JD_delta * JD_sin_theta_half / (1 - JD_sin_theta_half)
                JD_velocity_scalar = np.sqrt(JD_acc * JD_Radius)

                # return JD_velocity_scalar if JD_velocity_scalar < vel_0.get_norm() else vel_0.get_norm()
                return JD_velocity_scalar if JD_velocity_scalar < p_settings.speed else p_settings.speed
            else:
                return 0  # angle smaller than min angle, stop completely
        else:
            return p_settings.speed  # angle larger than max angle, full speed pass

    def __init__(self, state_A: state, state_B: state):
        """Marlin specific junction velocity calculation with Junction Deviation.

        Args:
            state_A: (state) start state
            state_B: (state)   end state
        """
        super().__init__(state_A, state_B)
        self.junction_vel = self.calc_JD(
            vel_0=self.target_vel, vel_1=self.vel_next, p_settings=self.state_B.state_p_settings
        )

    def get_junction_vel(self):
        """Return junction velocity.

        Returns:
            junction_vel: (float) junction velocity
        """
        return self.junction_vel


# class junction_handling_klipper(junction_handling):

#     """Klipper specific junction handling.

#     - similar junction deviation calc
#     - corner vel set by: square_corner_velocity
#         end_velocity^2 = start_velocity^2 + 2*accel*move_distance
#       for 90deg turn
#     - todo: smoothed look ahead

#     **Reference:**
#     [https://www.klipper3d.org/Kinematics.html](https://www.klipper3d.org/Kinematics.html)
#     [https://github.com/Klipper3d/klipper/blob/ea2f6bc0f544132738c7f052ffcc586fa884a19a/klippy/toolhead.py](https://github.com/Klipper3d/klipper/blob/ea2f6bc0f544132738c7f052ffcc586fa884a19a/klippy/toolhead.py)
#     """
#     import math

#     def __init__(self, state_A: state, state_B: state):
#         """Klipper specific junction velocity calculation.

#         Args:
#             state_A: (state) start state
#             state_B: (state)   end state
#         """
#         super().__init__(state_A, state_B)

#         self.calc_j_delta()
#         self.calc_j_vel()

#     def calc_j_delta(self):
#         """Calculate the junction deviation with klipper specific values.

#         The jerk value represents the square_corner_velocity!
#         """
#         sc_vel = (self.state_B.state_p_settings.jerk) ** 2
#         self.j_delta = sc_vel * (math.sqrt(2.0) - 1.0) / self.state_B.state_p_settings.p_acc

#     def calc_j_vel(self):
#         """Calculate the junction velocity."""
#         vel_0 = self.target_vel
#         vel_1 = self.vel_next

#         if vel_0.get_norm() == 0 or vel_1.get_norm() == 0:
#             self.junction_vel = 0
#             return

#         # calculate junction angle
#         dir0 = vel_0.get_norm_dir()
#         dir1 = vel_1.get_norm_dir()
#         j_cos_theta = -(
#             dir0[0] * dir1[0] + dir0[1] * dir1[1] + dir0[2] * dir1[2]
#         )  # cos of theta, theta: small angle between velocity vectors

#         j_cos_theta = max(j_cos_theta, -0.999999)  # limit
#         if j_cos_theta > 0.999999:
#             self.junction_vel = 0  # self.target_vel.get_norm()  # if self.target_vel.get_norm() is not None else 0
#             return
#         j_sin_theta_d2 = math.sqrt(0.5 * (1.0 - j_cos_theta))

#         j_R = self.j_delta * j_sin_theta_d2 / (1.0 - j_sin_theta_d2)

#         # [from klipper]: Approximated circle must contact moves no further away than mid-move
#         j_tan_theta_d2 = j_sin_theta_d2 / math.sqrt(0.5 * (1.0 + j_cos_theta))

#         move_centripetal_v2 = 0.5 * self.t_distance * j_tan_theta_d2 * self.state_B.state_p_settings.p_acc

#         self.junction_vel = math.sqrt(
#             min(self.state_B.state_p_settings.p_acc * j_R, move_centripetal_v2, self.state_B.state_p_settings.speed**2)
#         )

#     def get_junction_vel(self):
#         """Return the calculated junction velocity.

#         Returns:
#             junction_vel: (float) junction velocity
#         """
#         return self.junction_vel


def get_handler(firmware_name: str) -> type[junction_handling]:
    """Get the junction handling class for the given firmware name.

    Args:
        firmware_name: (str) name of the firmware

    Returns:
        junction_handling: (type[junction_handling]) junction handling class
    """
    if firmware_name == "prusa":
        return prusa
    elif firmware_name == "junction_deviation":
        return junction_deviation
    elif firmware_name == "marlin":
        return marlin
    elif firmware_name == "ultimaker":
        return ultimaker
    elif firmware_name == "mka":
        return mka
    else:
        custom_print(
            f"Using NO (zero interfacing velocity) junction handling handling for provided '{firmware_name}' firmware name.",
            f"Use one of the following: {', '.join(_get_handler_names())} for proper junction handling.",
            lvl=1,
        )
        return junction_handling


def _get_handler_names() -> list[str]:
    """Get the names of all available junction handling classes.

    Returns:
        list[str]: List of junction handling class names.
    """
    # Get all classes defined in this module that are subclasses of junction_handling (excluding the base itself)
    current_module = sys.modules[__name__]
    return [
        name
        for name, obj in inspect.getmembers(current_module, inspect.isclass)
        if issubclass(obj, junction_handling) and obj is not junction_handling
    ]
