# -*- coding: utf-8 -*-
"""
Utilitys.

Utils for the GCode Reader contains:
- Vector 4D
    - velocity
    - position
- Segment
"""
from typing import List

import numpy as np


class vector_4D:
    """The vector_4D class stores 4D Vector in x,y,z,e.

    Supports
        str, add, sub, eq
    Additional methods
        get_vec:        returns Position as a 1x3 or 1x4 list [x,y,z(,e)], optional argument withExtrusion: default = False
        https://stackoverflow.com/questions/73388831/python-method-that-returns-instance-of-class-or-subclass-while-keeping-subclass second answer was useful
    """

    def __init__(self, *args):
        """Store args = x,y,z,e or [x,y,z,e]."""
        self.x = None
        self.y = None
        self.z = None
        self.e = None

        if type(args) == tuple and len(args) == 1:
            args = tuple(args[0])
        if type(args) == tuple and len(args) == 4:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.e = args[3]
        else:
            raise ValueError("4D Spatial Object requires x,y,z,e or [x,y,z,e] as input.")

    def __str__(self) -> str:
        """Return string representation."""
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ", " + str(self.e) + "]"

    def __add__(self, other):
        """Add functionality for 4D Vectors.

        Possible input: 4D Vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'.
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
                "Addition with __add__ is only possible with other 4D Vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'"
            )

    def __sub__(self, other):
        """Sub functionality for 4D Vectors.

        Possible input: 4D Vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'.
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
                "Addition with __sub__ is only possible with other 4D Vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'"
            )

    def __mul__(self, other):
        """Scalar multiplication functionality for 4D Vectors.

        Possible input: float and int
        """
        if type(other) is float or type(other) is np.float64 or type(other) is int:
            x = self.x * other
            y = self.y * other
            z = self.z * other
            e = self.e * other
        else:
            raise TypeError("Mutiplication of 4D Vectors only supports float and int.")
        return self.__class__(x, y, z, e)

    def __truediv__(self, other):
        """Scalar division functionality for 4D Vectors.

        Possible input: float and int
        """
        if type(other) is float or type(other) is np.float64:
            x = self.x / other
            y = self.y / other
            z = self.z / other
            e = self.e / other
        else:
            raise TypeError("Division of 4D Vectors only supports float and int.")
        return self.__class__(x, y, z, e)

    def __eq__(self, other, tolerance=None):
        """Check for Equality and Return True if equal. Optional tolerance.

        Possible input: 4D Vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'.
        """
        if isinstance(other, type(self)):
            if self.x == other.x and self.y == other.y and self.z == other.z and self.e == other.e:
                return True

        elif (isinstance(other, np.ndarray) or isinstance(other, list) or isinstance(other, tuple)) and len(other) == 4:
            if self.x == other[0] and self.y == other[1] and self.z == other[2] and self.e == other[3]:
                return True

        if tolerance is not None:
            if isinstance(other, type(self)):
                dist = np.linalg.norm(self - other)  # calculate distance through __sub__
            elif (isinstance(other, np.ndarray) or isinstance(other, list) or isinstance(other, tuple)) and len(
                other
            ) == 4:
                dist = np.linalg.norm(
                    self.x - other[0], self.y - other[1], self.z - other[2], self.e - other[3]
                )  # calculate distance manually
            else:
                raise ValueError(
                    "Equality check failed, only possible with other 4D Vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'"
                )
            if dist <= tolerance:
                return True

        else:
            return False

    def get_vec(self, withExtrusion=False):
        """Return the 4D Vector, optionally with Extrusion."""
        if withExtrusion:
            return [self.x, self.y, self.z, self.e]
        else:
            return [self.x, self.y, self.z]

    def get_norm(self, withExtrusion=False):
        """Return the 4D Vector norm."""
        return np.linalg.norm(self.get_vec(withExtrusion=withExtrusion))


class velocity(vector_4D):
    """4D - Velocity object for (cartesian) 3D Printer
    Supports
        str, add, sub, mul (scalar), truediv (scalar),eq
    Additional methods
        get_vec:        returns Velocity as a 1x3 or 1x4 list [Vx,Vy,Vz(,Ve)], optional argument withExtrusion: default = False
        get_norm:        returns the absolute 3D movement Velocity, extrusion is ignored
        get_norm dir:   returns the normalized direction as 1x3 or 1x4 list [Vx,Vy,Vz(,Ve)], optional argument withExtrusion: default = False
        avoid_overspeed:returns Velocity with all axis kept below their max travel speed
    Class method
        convert_vector_to_velocity: returns a Velocity object with a 1x4 list as input [Vx,Vy,Vz,Ve]
    """

    def __str__(self) -> str:
        return "velocity: " + super().__str__()

    def get_norm_dir(self, withExtrusion=False):
        # get (regarding travel distance) normalized vector, if only extrusion occurs, normalize to extrusion length
        abs_val = self.get_norm()
        if abs_val > 0:
            return self.get_vec(withExtrusion=withExtrusion) / abs_val
        elif withExtrusion and self.get_norm(withExtrusion=withExtrusion) > 0:
            return self.get_vec(withExtrusion=withExtrusion) / self.get_norm(withExtrusion=withExtrusion)
        else:
            return None

    def avoid_overspeed(self, p_settings):
        """Returns velocity without any axis overspeed"""
        scale = 1.0
        scale = p_settings.Vx / self.Vx if self.Vx > 0 and p_settings.Vx / self.Vx < scale else scale
        scale = p_settings.Vy / self.Vy if self.Vy > 0 and p_settings.Vy / self.Vy < scale else scale
        scale = p_settings.Vz / self.Vz if self.Vz > 0 and p_settings.Vz / self.Vz < scale else scale
        scale = p_settings.Ve / self.Ve if self.Vz > 0 and p_settings.Ve / self.Ve < scale else scale

        return self * scale

    def not_zero(self):
        return True if np.linalg.norm(self.get_vec(withExtrusion=True)) > 0 else False


class position(vector_4D):
    """The Position stores 4D spatial data in x,y,z,e.
    Supports
        str, add (pos+pos, pos+(list 1x4), pos+(numpy.ndarray 1x4))
    Additional methods
        is_travel:      returns True if there is a travel move between self and another given Position
        is_extruding:   returns True if there is an extrusion between self and another given Position
        get_vec:        returns Position as a 1x3 or 1x4 list [x,y,z(,e)], optional argument withExtrusion: default = False
        get_t_distance: returns the absolute travel distance between self and another given Position (3D)
    Class method
        new:            returns an updated Position from given old Position and optional changing positional values
        convert_vector_to_position: returns a Position object with a 1x4 list as input [Vx,Vy,Vz,Ve]
    """

    def __str__(self) -> str:
        return "position: " + super().__str__()

    def is_travel(self, old_position) -> bool:
        if abs(old_position.x - self.x) + abs(old_position.y - self.y) + abs(old_position.z - self.z) > 0:
            return True
        else:
            return False

    def is_extruding(self, old_position) -> bool:
        if abs(old_position.e - self.e) > 0:
            return True
        else:
            return False

    def get_vec(self, withExtrusion=False):
        if withExtrusion:
            return [self.x, self.y, self.z, self.e]
        else:
            return [self.x, self.y, self.z]

    def get_t_distance(self, old_position=None, withExtrusion=False) -> float:
        if old_position is None:
            old_position = position(0, 0, 0, 0)
        return np.linalg.norm(
            np.subtract(self.get_vec(withExtrusion=withExtrusion), old_position.get_vec(withExtrusion=withExtrusion))
        )

    @classmethod
    def new(cls, old_position, x: float = None, y: float = None, z: float = None, e: float = None, absMode=True):
        if x is None:
            x = old_position.x
        if y is None:
            y = old_position.y
        if z is None:
            z = old_position.z
        if not absMode and e is not None:  # if rel mode, extrusion needs to be summed
            e = old_position.e + e
        if e is None:
            e = old_position.e
        return cls(x, y, z, e)

    @classmethod
    def convert_vector_to_position(cls, vector: List[float]):
        return cls(x=vector[0], y=vector[1], z=vector[2], e=vector[3])
