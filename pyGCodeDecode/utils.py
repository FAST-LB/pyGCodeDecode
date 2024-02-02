# -*- coding: utf-8 -*-
"""
Utilitys.

Utils for the GCode Reader contains:
- vector 4D
    - velocity
    - position
"""

import numpy as np


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

        if type(args) is tuple and len(args) == 1:
            args = tuple(args[0])
        if type(args) is tuple and len(args) == 4:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.e = args[3]
        else:
            raise ValueError("4D object requires x,y,z,e or [x,y,z,e] as input.")

    def __str__(self) -> str:
        """Return string representation."""
        return f"[{self.x}, {self.y}, {self.z}, {self.e}]"

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
        if type(other) is float or type(other) is np.float64 or type(other) is int:
            x = self.x * other
            y = self.y * other
            z = self.z * other
            e = self.e * other
        else:
            raise TypeError("Mutiplication of 4D vectors only supports float and int.")
        return self.__class__(x, y, z, e)

    def __truediv__(self, other):
        """Scalar division functionality for 4D Vectors.

        Args:
            other: (float or int)

        Returns:
            div: (self) scalar division, scaling
        """
        if type(other) is float or type(other) is np.float64:
            x = self.x / other
            y = self.y / other
            z = self.z / other
            e = self.e / other
        else:
            raise TypeError("Division of 4D Vectors only supports float and int.")
        return self.__class__(x, y, z, e)

    def __eq__(self, other):
        """Check for equality and return True if equal.

        Args:
            other: (4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray')

        Returns:
            eq: (bool) true if equal (with tolerance)
        """
        import numpy as np

        if isinstance(other, type(self)):
            if (
                np.isclose(self.x, other.x)
                and np.isclose(self.y, other.y)
                and np.isclose(self.z, other.z)
                and np.isclose(self.e, other.e)
            ):
                return True

        elif (isinstance(other, np.ndarray) or isinstance(other, list) or isinstance(other, tuple)) and len(other) == 4:
            if (
                np.isclose(self.x, other[0])
                and np.isclose(self.y, other[1])
                and np.isclose(self.z, other[2])
                and np.isclose(self.e, other[3])
            ):
                return True

    def get_vec(self, withExtrusion=False):
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

    def get_norm(self, withExtrusion=False):
        """Return the 4D vector norm. Optional with extrusion.

        Args:
            withExtrusion: (bool, default = False) choose if norm contains extrusion

        Returns:
            norm: (float) length/norm of 3D or 4D vector
        """
        return np.linalg.norm(self.get_vec(withExtrusion=withExtrusion))


class velocity(vector_4D):
    """4D - Velocity object for (cartesian) 3D printer."""

    def __str__(self) -> str:
        """Print out velocity."""
        return "velocity: " + super().__str__()

    def get_norm_dir(self, withExtrusion=False):
        """Get normalized vector (regarding travel distance), if only extrusion occurs, normalize to extrusion length.

        Args:
            withExtrusion: (bool, default = False) choose if norm dir contains extrusion

        Returns:
            dir: (list[3 or 4]) normalized direction vector as list
        """
        abs_val = self.get_norm()
        if abs_val > 0:
            return self.get_vec(withExtrusion=withExtrusion) / abs_val
        elif withExtrusion and self.get_norm(withExtrusion=withExtrusion) > 0:
            return self.get_vec(withExtrusion=withExtrusion) / self.get_norm(withExtrusion=withExtrusion)
        else:
            return None

    def avoid_overspeed(self, p_settings):
        """Return velocity without any axis overspeed.

        Args:
            p_settings: (p_settings) printing settings

        Returns:
            vel: (velocity) constrained by max velocity
        """
        scale = 1.0
        scale = p_settings.Vx / self.Vx if self.Vx > 0 and p_settings.Vx / self.Vx < scale else scale
        scale = p_settings.Vy / self.Vy if self.Vy > 0 and p_settings.Vy / self.Vy < scale else scale
        scale = p_settings.Vz / self.Vz if self.Vz > 0 and p_settings.Vz / self.Vz < scale else scale
        scale = p_settings.Ve / self.Ve if self.Vz > 0 and p_settings.Ve / self.Ve < scale else scale

        return self * scale

    def not_zero(self):
        """Return True if velocity is not zero.

        Returns:
            not_zero: (bool) true if velocity is not zero
        """
        return True if np.linalg.norm(self.get_vec(withExtrusion=True)) > 0 else False

    def is_extruding(self):
        """Return True if extrusion velocity is not zero.

        Returns:
            is_extruding: (bool) true if positive extrusion velocity
        """
        return True if self.e > 0 else False


class position(vector_4D):
    """4D - Position object for (cartesian) 3D printer."""

    def __str__(self) -> str:
        """Print out position."""
        return "position: " + super().__str__()

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
        extr = other.e - self.e if ignore_retract else abs(other.e - self.e)

        if extr > 0:
            return True
        else:
            return False

    def get_t_distance(self, other=None, withExtrusion=False) -> float:
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


class segment:
    """Store Segment data for linear 4D Velocity function segment.

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
    """

    def __init__(
        self,
        t_begin: float,
        t_end: float,
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
        self.t_begin = t_begin
        self.t_end = t_end
        self.pos_begin = pos_begin
        self.pos_end = pos_end
        self.vel_begin = vel_begin
        self.vel_end = vel_end
        self.self_check()

    def __str__(self) -> str:
        """Create string from segment."""
        return f"\nSegment from: \n{self.pos_begin} to \n{self.pos_end} Self check: {self.self_check()}.\n"

    def __repr__(self):
        """Segment representation."""
        return self.__str__()

    def move_segment_time(self, delta_t: float):
        """Move segment in time.

        Args:
            delta_t: (float) time to be shifted
        """
        self.t_begin = self.t_begin + delta_t
        self.t_end = self.t_end + delta_t

    def get_velocity(self, t: float) -> velocity:
        """Get current velocity of segment at a certain time.

        Args:
            t: (float) time

        Returns:
            current_vel: (velocity) velocity at time t
        """
        if t < self.t_begin or t > self.t_end:
            raise ValueError("Segment not defined for this point in time.")
        else:
            # linear interpolation of velocity in Segment
            delt_vel = self.vel_end - self.vel_begin
            delt_t = self.t_end - self.t_begin
            slope = delt_vel / delt_t if delt_t > 0 else velocity(0, 0, 0, 0)
            current_vel = self.vel_begin + slope * (t - self.t_begin)
            return current_vel

    def get_position(self, t: float) -> position:
        """Get current position of segment at a certain time.

        Args:
            t: (float) time

        Returns:
            pos: (position) position at time t
        """
        if t < self.t_begin or t > self.t_end:
            raise ValueError(f"Segment not defined for this point in time. {t} -->({self.t_begin}, {self.t_end})")
        else:
            current_vel = self.get_velocity(t=t)
            position = self.pos_begin + ((self.vel_begin + current_vel) * (t - self.t_begin) / 2.0).get_vec(
                withExtrusion=True
            )
            return position

    def self_check(self, p_settings=None):  # ,, state:state=None):
        """Check the segment for self consistency.

        todo:
        - max acceleration

        Args:
            p_settings: (p_setting, default = None) printing settings to verify
        """
        # position self check:
        tolerance = float("1e-6")
        position = self.pos_begin + ((self.vel_begin + self.vel_end) * (self.t_end - self.t_begin) / 2.0).get_vec(
            withExtrusion=True
        )
        error_distance = np.linalg.norm(np.asarray(self.pos_end.get_vec()) - np.asarray(position.get_vec()))

        if error_distance > tolerance:
            raise ValueError("Error distance: " + str(error_distance))

        # time consistency
        if self.t_begin > self.t_end:
            raise ValueError(f"Inconsistent segment time (t_begin/t_end): ({self.t_begin}/{self.t_end}) \n ")

        # max velocity
        if p_settings is not None:
            if self.vel_begin.get_norm() > p_settings.speed and not np.isclose(
                self.vel_begin.get_norm(), p_settings.speed
            ):
                raise ValueError(f"Target Velocity of {p_settings.speed} exceeded with {self.vel_begin.get_norm()}.")
            if self.vel_end.get_norm() > p_settings.speed and not np.isclose(self.vel_end.get_norm(), p_settings.speed):
                raise ValueError(f"Target Velocity of {p_settings.speed} exceeded with {self.vel_end.get_norm()}.")

    def is_extruding(self) -> bool:
        """Return true if the segment is pos. extruding.

        Returns:
            is_extruding: (bool) true if positive extrusion
        """
        return self.pos_begin.e < self.pos_end.e

    @classmethod
    def create_initial(cls, initial_position: position = None):
        """Create initial static segment with (optionally) initial position else start from Zero.

        Args:
            initial_position: (postion, default = None) position to begin segment series

        Returns:
            segment: (segment) initial beginning segment
        """
        velocity_0 = velocity(0, 0, 0, 0)
        pos_0 = position(x=0, y=0, z=0, e=0) if initial_position is None else initial_position
        return cls(t_begin=0, t_end=0, pos_begin=pos_0, vel_begin=velocity_0, pos_end=pos_0, vel_end=velocity_0)
