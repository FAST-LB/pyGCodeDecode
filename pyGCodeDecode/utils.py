"""
Utilities.

Utils for the GCode Reader contains:
- vector 4D
    - velocity
    - position
"""

from typing import TYPE_CHECKING, List, Optional, Union

import numpy as np

if TYPE_CHECKING:
    from pyGCodeDecode.state import state


class seconds(float):
    """A float subclass representing a time duration in seconds.

    Args:
        value (float or int): The time duration in seconds.
    Examples:
    ```python
    >>> from pyGCodeDecode.utils import seconds
    >>> t = seconds(5)
    >>> str(t)
    '5.0 s'
    >>> t.seconds
    5.0
    ```
    """

    """Time class for storing time, behaves like a float with additional methods."""

    def __new__(cls, value):
        """Create a new instance of seconds."""
        return float.__new__(cls, value)

    def __str__(self) -> str:
        """Return string representation of the time in seconds."""
        return f"{float(self)} s"

    def __sub__(self, other) -> "seconds":
        """Subtract seconds or float and return a new seconds instance."""
        return seconds(float(self) - float(other))

    def __add__(self, other) -> "seconds":
        """Add seconds or float and return a new seconds instance."""
        return seconds(float(self) + float(other))

    def __repr__(self) -> str:
        """Return a string representation of the seconds object."""
        return self.__str__()

    @property
    def seconds(self) -> float:
        """Return the float value of the seconds instance."""
        return float(self)


class vector_4D:
    """The vector_4D class stores 4D vector in x,y,z,e.

    **Supports:**
    - str
    - add
    - sub
    - mul (scalar)
    - truediv (scalar)
    - eq
    """

    def __init__(self, *args):
        """Store 3D position + extrusion axis.

        Args:
            args: coordinates as arguments x,y,z,e or (tuple or list) [x,y,z,e]

        """
        self.x = None
        self.y = None
        self.z = None
        self.e = None

        if isinstance(args[0], (tuple, list, np.ndarray)) and len(args) == 1 and len(args[0]) == 4:
            args = tuple(args[0])
        if len(args) == 4:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.e = args[3]
        else:
            raise ValueError("4D object requires x,y,z,e or [x,y,z,e] as input.")

    def __str__(self) -> str:
        """Return string representation."""
        return f"[{self.x}, {self.y}, {self.z}, {self.e}]"

    def __repr__(self):
        """Return a string representation of the 4D vector."""
        return self.__str__()

    def __add__(self, other):
        """Add functionality for 4D vectors.

        Args:
            other: (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')

        Returns:
            add: (self) component wise addition
        """
        if isinstance(other, self.__class__):
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
            e = self.e + other.e
            return self.__class__(x, y, z, e)
        elif (isinstance(other, np.ndarray) or isinstance(other, list) or isinstance(other, tuple)) and len(other) == 4:
            x = self.x + other[0]
            y = self.y + other[1]
            z = self.z + other[2]
            e = self.e + other[3]
            return self.__class__(x, y, z, e)
        else:
            raise ValueError(
                "Addition with __add__ is only possible with other 4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'"
                f" got {type(other)} instead."
            )

    def __sub__(self, other):
        """Sub functionality for 4D vectors.

        Args:
            other: (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')

        Returns:
            sub: (self) component wise subtraction
        """
        if isinstance(other, self.__class__):
            x = self.x - other.x
            y = self.y - other.y
            z = self.z - other.z
            e = self.e - other.e
            return self.__class__(x, y, z, e)
        elif (isinstance(other, np.ndarray) or isinstance(other, list) or isinstance(other, tuple)) and len(other) == 4:
            x = self.x - other[0]
            y = self.y - other[1]
            z = self.z - other[2]
            e = self.e - other[3]
            return self.__class__(x, y, z, e)
        else:
            raise ValueError(
                "Addition with __sub__ is only possible with other 4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'"
            )

    def __mul__(self, other):
        """Scalar multiplication functionality for 4D vectors.

        Args:
            other: (float or int)

        Returns:
            mul: (self) scalar multiplication, scaling
        """
        if isinstance(other, (float, int, np.floating, np.integer)):
            x = self.x * other
            y = self.y * other
            z = self.z * other
            e = self.e * other
        else:
            raise TypeError("Multiplication of 4D vectors only supports float and int.")
        return self.__class__(x, y, z, e)

    def __truediv__(self, other):
        """Scalar division functionality for 4D Vectors.

        Args:
            other: (float or int)

        Returns:
            div: (self) scalar division, scaling
        """
        if isinstance(other, (float, int, np.floating, np.integer)):
            x = self.x / other
            y = self.y / other
            z = self.z / other
            e = self.e / other
        else:
            raise TypeError("Division of 4D Vectors only supports float and int.")
        return self.__class__(x, y, z, e)

    def __eq__(self, other) -> bool:
        """Check for equality and return True if equal.

        Args:
            other: (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')

        Returns:
            eq: (bool) true if equal
        """
        if isinstance(other, type(self)):
            other_vec = [other.x, other.y, other.z, other.e]
        elif isinstance(other, (np.ndarray, list, tuple)) and len(other) == 4:
            other_vec = list(other)
        else:
            return False

        self_vec = [self.x, self.y, self.z, self.e]
        return other_vec == self_vec
        # return np.allclose(self_vec, other_vec)

    def __gt__(self, other) -> bool:
        """Check for greater than and return True if greater.

        Args:
            other: (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')

        Returns:
            gt: (bool) true if greater
        """
        if isinstance(other, type(self)):
            return self.get_norm() > other.get_norm()
        elif (isinstance(other, np.ndarray)) or (isinstance(other, (list, tuple)) and len(other) == 4):
            return self.get_norm() > np.linalg.norm(other)
        elif isinstance(other, (float, int)):
            return self.get_norm() > other
        else:
            return False

    def get_vec(self, withExtrusion: bool = False) -> List[float]:
        """Return the 4D vector, optionally with extrusion.

        Args:
            withExtrusion: (bool, default = False) choose if vec repr contains extrusion

        Returns:
            vec: (list[3 or 4]) with (x,y,z,(optionally e))
        """
        if withExtrusion:
            return [self.x, self.y, self.z, self.e]
        else:
            return [self.x, self.y, self.z]

    def get_norm(self, withExtrusion: bool = False) -> float:
        """Return the 4D vector norm. Optional with extrusion.

        Args:
            withExtrusion: (bool, default = False) choose if norm contains extrusion

        Returns:
            norm: (float) length/norm of 3D or 4D vector
        """
        return np.linalg.norm(self.get_vec(withExtrusion=withExtrusion))


class position(vector_4D):
    """4D - Position object for (Cartesian) 3D printer."""

    def __str__(self) -> str:
        """Print out position."""
        return "Position: " + super().__str__()

    def is_travel(self, other) -> bool:
        """Return True if there is travel between self and other position.

        Args:
            other: (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')

        Returns:
            is_travel: (bool) true if between self and other is distance
        """
        if abs(other.x - self.x) + abs(other.y - self.y) + abs(other.z - self.z) > 0:
            return True
        else:
            return False

    def is_extruding(self, other: "position", ignore_retract: bool = True) -> bool:
        """Return True if there is extrusion between self and other position.

        Args:
            other: (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')
            ignore_retract: (bool, default = True) if true ignore retract movements else retract is also extrusion

        Returns:
            is_extruding: (bool) true if between self and other is extrusion
        """
        extrusion = other.e - self.e if ignore_retract else abs(other.e - self.e)

        if extrusion > 0:
            return True
        else:
            return False

    def get_t_distance(self, other=None, withExtrusion: bool = False) -> float:
        """Calculate the travel distance between self and other position. If none is provided, zero will be used.

        Args:
            other: (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray', default = None)
            withExtrusion: (bool, default = False) use or ignore extrusion

        Returns:
            travel: (float) travel or extrusion and travel distance
        """
        if other is None:
            other = position(0, 0, 0, 0)
        return np.linalg.norm(
            np.subtract(self.get_vec(withExtrusion=withExtrusion), other.get_vec(withExtrusion=withExtrusion))
        )

    def __truediv__(self, other):
        """Divide position by seconds to get velocity."""
        if isinstance(other, seconds):
            return velocity(
                self.x / other.seconds,
                self.y / other.seconds,
                self.z / other.seconds,
                self.e / other.seconds,
            )
        else:
            return super().__truediv__(other)


class velocity(vector_4D):
    """4D - Velocity object for (Cartesian) 3D printer."""

    def __str__(self) -> str:
        """Print out velocity."""
        return "velocity: " + super().__str__()

    def get_norm_dir(self, withExtrusion: bool = False) -> Optional[np.ndarray]:
        """Get normalized direction vector as numpy array.

        If only extrusion occurs and withExtrusion=True, normalize to the extrusion length.

        Returns None if both travel and extrusion are zero.
        """
        # travel_vec = np.asarray(self.get_vec(withExtrusion=False), dtype=float)
        # travel_norm = np.linalg.norm(travel_vec)
        travel_norm = self.get_norm()
        if travel_norm > 0:
            vec = np.asarray(self.get_vec(withExtrusion=withExtrusion), dtype=float)
            return vec / travel_norm
        elif withExtrusion:
            vec_e = np.asarray(self.get_vec(withExtrusion=True), dtype=float)
            full_norm = np.linalg.norm(vec_e)
            if full_norm > 0:
                return vec_e / full_norm
        return None

    # def avoid_overspeed(self, p_settings: "state.p_settings") -> "velocity":
    #     """Return velocity scaled to avoid any axis overspeed.

    #     Scales the velocity uniformly so that no axis exceeds its configured maximum.
    #     """
    #     scale = 1.0
    #     scale = p_settings.Vx / self.Vx if self.Vx > 0 and (p_settings.Vx / self.Vx) < scale else scale
    #     scale = p_settings.Vy / self.Vy if self.Vy > 0 and (p_settings.Vy / self.Vy) < scale else scale
    #     scale = p_settings.Vz / self.Vz if self.Vz > 0 and (p_settings.Vz / self.Vz) < scale else scale
    #     scale = p_settings.Ve / self.Ve if self.Ve > 0 and (p_settings.Ve / self.Ve) < scale else scale

    #     return self * scale

    def not_zero(self) -> bool:
        """Return True if velocity is not zero.

        Returns:
            not_zero: (bool) true if velocity is not zero
        """
        return True if np.linalg.norm(self.get_vec(withExtrusion=True)) > 0 else False

    def is_extruding(self) -> bool:
        """Return True if extrusion velocity is greater than zero.

        Returns:
            is_extruding: (bool) true if positive extrusion velocity
        """
        return True if self.e > 0 else False

    def __mul__(self, other):
        """Multiply velocity by a time to get position, or by scalar."""
        if isinstance(other, seconds):
            # velocity * seconds = position
            return position(
                self.x * other.seconds,
                self.y * other.seconds,
                self.z * other.seconds,
                self.e * other.seconds,
            )
        elif isinstance(other, (float, int, np.floating, np.integer)):
            return self.__class__(
                self.x * other,
                self.y * other,
                self.z * other,
                self.e * other,
            )
        else:
            raise TypeError("Multiplication only supports seconds, float, or int.")

    def __truediv__(self, other):
        """Divide velocity by scalar."""
        if isinstance(other, seconds):
            # velocity / seconds = acceleration
            return acceleration(
                self.x / other.seconds,
                self.y / other.seconds,
                self.z / other.seconds,
                self.e / other.seconds,
            )
        else:
            return super().__truediv__(other)


class acceleration(vector_4D):
    """4D - Acceleration object for (Cartesian) 3D printer."""

    def __str__(self) -> str:
        """Print out acceleration."""
        return "acceleration: " + super().__str__()

    def __mul__(self, other):
        """Multiply acceleration by a time to get velocity, or by scalar."""
        if isinstance(other, seconds):
            # acceleration * time = velocity
            return velocity(
                self.x * other.seconds,
                self.y * other.seconds,
                self.z * other.seconds,
                self.e * other.seconds,
            )
        elif isinstance(other, (float, int, np.floating, np.integer)):
            return self.__class__(
                self.x * other,
                self.y * other,
                self.z * other,
                self.e * other,
            )
        else:
            raise TypeError("Multiplication only supports seconds, float, or int.")

    def __truediv__(self, other):
        """Divide acceleration by scalar."""
        return super().__truediv__(other)


class segment:
    """Store Segment data for linear 4D Velocity function segment.

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
    """

    def __init__(
        self,
        t_begin: Union[float, seconds],
        t_end: Union[float, seconds],
        pos_begin: position,
        vel_begin: velocity,
        pos_end: position = None,
        vel_end: velocity = None,
    ):
        """Initialize a segment.

        Args:
            t_begin: (float) begin of segment
            t_end: (float) end of segment
            pos_begin: (position) beginning position of segment
            vel_begin: (velocity) beginning velocity of segment
            pos_end: (position, default = None) ending position of segment
            vel_end: (velocity, default = None) ending velocity of segment

        """
        self.t_begin: seconds = seconds(t_begin)
        self.t_end: seconds = seconds(t_end)
        self.pos_begin: position = pos_begin
        self.pos_end: position = pos_end
        self.vel_begin: velocity = vel_begin
        self.vel_end: velocity = vel_end
        # self.self_check()

        self.result = {}

    def __str__(self) -> str:
        """Create string from segment."""
        return f"\nSegment from: \n{self.pos_begin} to \n{self.pos_end} Self check: {self.self_check()}.\n"

    def __repr__(self):
        """Segment representation."""
        return self.__str__()

    def move_segment_time(self, delta_t: Union[float, seconds]) -> None:
        """Move segment in time.

        Args:
            delta_t: (float) time to be shifted
        """
        self.t_begin = self.t_begin + delta_t
        self.t_end = self.t_end + delta_t

    def get_velocity(self, t: Union[float, seconds]) -> velocity:
        """Get current velocity of segment at a certain time.

        Args:
            t: (float) time

        Returns:
            current_vel: (velocity) velocity at time t
        """
        if not isinstance(t, seconds):
            t = seconds(t)

        if t < self.t_begin or t > self.t_end:
            raise ValueError("Segment not defined for this point in time.")
        else:
            delt_t = self.t_end - self.t_begin
            if delt_t == 0:
                return self.vel_begin
            # linear interpolation of velocity in Segment
            delt_vel = self.vel_end - self.vel_begin
            slope = delt_vel / delt_t
            current_vel = self.vel_begin + (slope * (t - self.t_begin))
            return current_vel

    def get_velocity_by_dist(self, dist: float) -> float:
        """Return the velocity magnitude at a certain local segment distance.

        Args:
            dist: (float) distance from segment start
        """
        dt = self.t_end - self.t_begin
        a = 0.0 if dt == 0 else (self.vel_end.get_norm() - self.vel_begin.get_norm()) / dt

        v_sq = 2 * a * dist + self.vel_begin.get_norm() ** 2
        v = np.sqrt(v_sq) if v_sq > 0 else 0

        return float(v)

    def get_position(self, t: Union[float, seconds]) -> position:
        """Get current position of segment at a certain time.

        Args:
            t: (float) time

        Returns:
            pos: (position) position at time t
        """
        if not isinstance(t, seconds):
            t = seconds(t)
        if t < self.t_begin or t > self.t_end:
            raise ValueError(f"Segment not defined for this point in time. {t} -->({self.t_begin}, {self.t_end})")
        else:
            current_vel = self.get_velocity(t=t)
            # displacement = average velocity * dt
            displacement_vec = ((self.vel_begin + current_vel) * (t - self.t_begin) / 2.0).get_vec(withExtrusion=True)
            position_val = self.pos_begin + displacement_vec
            return position_val

    def get_segm_len(self) -> float:
        """Return the length of the segment."""
        return (self.pos_end - self.pos_begin).get_norm()

    def get_segm_duration(self) -> seconds:
        """Return the duration of the segment."""
        return self.t_end - self.t_begin

    def self_check(self, p_settings: "state.p_settings" = None) -> bool:
        """Check the segment for self consistency.

        Raises:
            ValueError: if self check fails
        Args:
            p_settings: (p_settings, default = None) printing settings to verify
        Returns:
            True if all checks pass
        """
        # position self check:
        tolerance = 1e-6
        position_calc = self.pos_begin + ((self.vel_begin + self.vel_end) * (self.t_end - self.t_begin) / 2.0)
        error_distance = self.pos_end - position_calc
        if error_distance.get_norm(withExtrusion=True) > tolerance:
            raise ValueError("Error distance: " + str(error_distance))

        # time consistency
        if self.t_begin > self.t_end:
            raise ValueError(f"Inconsistent segment time (t_begin/t_end): ({self.t_begin}/{self.t_end}) \n ")

        if p_settings is not None:
            # max velocity
            if self.vel_begin.get_norm() > p_settings.speed and not np.isclose(
                self.vel_begin.get_norm(), p_settings.speed
            ):
                raise ValueError(f"Target Velocity of {p_settings.speed} exceeded with {self.vel_begin.get_norm()}.")
            if self.vel_end.get_norm() > p_settings.speed and not np.isclose(self.vel_end.get_norm(), p_settings.speed):
                raise ValueError(f"Target Velocity of {p_settings.speed} exceeded with {self.vel_end.get_norm()}.")

            # max acceleration
            if self.t_end - self.t_begin > 0:
                acc = (self.vel_end - self.vel_begin) / (self.t_end - self.t_begin)

                # Scale tolerance based on time delta to handle numerical precision issues
                dt = self.t_end - self.t_begin
                base_rtol = 1e-5  # Standard relative tolerance
                base_atol = 0.1  # Absolute tolerance in mm/s²

                # Scale tolerance inversely with time delta (smaller dt = larger tolerance)
                dt_scale = min(1e-6 / max(dt, 1e-12), 1000.0)
                scaled_rtol = base_rtol * dt_scale
                scaled_atol = base_atol * dt_scale
                acc_norm = acc.get_norm()

                if acc_norm > p_settings.p_acc and not np.isclose(
                    acc_norm, p_settings.p_acc, rtol=scaled_rtol, atol=scaled_atol
                ):
                    raise ValueError(
                        f"Maximum acceleration of {p_settings.p_acc} exceeded with {acc_norm}. "
                        f"Delta t: {dt:.2e}, tolerance used: rtol={scaled_rtol:.2e}, atol={scaled_atol:.2e}"
                    )
        return True

    def is_extruding(self) -> bool:
        """Return true if the segment is pos. extruding.

        Returns:
            is_extruding: (bool) true if positive extrusion
        """
        return self.pos_begin.e < self.pos_end.e

    def _interpolate_time_to_space(self, scalar_begin, scalar_end, x) -> float:
        """
        Interpolate from linear time dependant to nonlinear space dependant.

        Args:
            scalar_begin: (float) begin value
            scalar_end: (float) end value
            x: (float) x position
        """

        def lin_scalar(t):
            slope = (scalar_end - scalar_begin) / (self.t_end - self.t_begin)
            return slope * t + scalar_begin

        def get_time(x):
            a = (self.vel_end - self.vel_begin).get_norm() / (self.t_end - self.t_begin)
            if a > 0:
                v_sq = 2 * a * x + self.vel_begin.get_norm() ** 2
                t = (np.sqrt(v_sq) - self.vel_begin.get_norm()) / a if v_sq > 0 else 0
                if v_sq <= 0:
                    raise ValueError("Could not map time dependant scalar to space.")
            elif a == 0:
                t = x / self.vel_begin.get_norm()
            return t

        t = get_time(x)
        scalar = lin_scalar(t)

        return scalar

    def get_result(self, key: str):
        """Return the requested result.

        Args:
            key: (str) choose result

        Returns:
            result: (list)
        """
        if key in self.result:
            return self.result[key]
        else:
            raise ValueError(f"Key: {key} not found.")

    @classmethod
    def create_initial(cls, initial_position: Optional[position] = None) -> "segment":
        """Create initial static segment with (optionally) initial position else start from Zero.

        Args:
            initial_position: (postion, default = None) position to begin segment series

        Returns:
            segment: (segment) initial beginning segment
        """
        velocity_0 = velocity(0, 0, 0, 0)
        pos_0 = position(0, 0, 0, 0) if initial_position is None else initial_position
        return cls(t_begin=0, t_end=0, pos_begin=pos_0, vel_begin=velocity_0, pos_end=pos_0, vel_end=velocity_0)
