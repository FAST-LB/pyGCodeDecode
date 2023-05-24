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

    Supports
        str, add, sub, mul (scalar), truediv (scalar),eq
    Additional methods
        get_vec:        returns vector as a 1x3 or 1x4 list [x,y,z(,e)], optional argument withExtrusion: default = False
        get_norm:       returns norm of vector, optional argument withExtrusion: default = False
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
            raise ValueError("4D object requires x,y,z,e or [x,y,z,e] as input.")

    def __str__(self) -> str:
        """Return string representation."""
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ", " + str(self.e) + "]"

    def __add__(self, other):
        """Add functionality for 4D vectors.

        Possible input: 4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'.
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

        Possible input: 4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'.
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

        Possible input: float and int
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
        """Check for equality and return True if equal. Optional tolerance.

        Possible input: 4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'.
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
                    "Equality check failed, only possible with other 4D vector, 1x4 'list', 1x4 'tuple' or 1x4 'numpy.ndarray'"
                )
            if dist <= tolerance:
                return True

        else:
            return False

    def get_vec(self, withExtrusion=False):
        """Return the 4D vector, optionally with extrusion."""
        if withExtrusion:
            return [self.x, self.y, self.z, self.e]
        else:
            return [self.x, self.y, self.z]

    def get_norm(self, withExtrusion=False):
        """Return the 4D vector norm. Optional with extrusion."""
        return np.linalg.norm(self.get_vec(withExtrusion=withExtrusion))


class velocity(vector_4D):
    """4D - Velocity object for (cartesian) 3D printer."""

    def __str__(self) -> str:
        """Print out velocity."""
        return "velocity: " + super().__str__()

    def get_norm_dir(self, withExtrusion=False):
        """Get normalized vector (regarding travel distance), if only extrusion occurs, normalize to extrusion length."""
        abs_val = self.get_norm()
        if abs_val > 0:
            return self.get_vec(withExtrusion=withExtrusion) / abs_val
        elif withExtrusion and self.get_norm(withExtrusion=withExtrusion) > 0:
            return self.get_vec(withExtrusion=withExtrusion) / self.get_norm(withExtrusion=withExtrusion)
        else:
            return None

    def avoid_overspeed(self, p_settings):
        """Return velocity without any axis overspeed."""
        scale = 1.0
        scale = p_settings.Vx / self.Vx if self.Vx > 0 and p_settings.Vx / self.Vx < scale else scale
        scale = p_settings.Vy / self.Vy if self.Vy > 0 and p_settings.Vy / self.Vy < scale else scale
        scale = p_settings.Vz / self.Vz if self.Vz > 0 and p_settings.Vz / self.Vz < scale else scale
        scale = p_settings.Ve / self.Ve if self.Vz > 0 and p_settings.Ve / self.Ve < scale else scale

        return self * scale

    def not_zero(self):
        """Return True if velocity is not zero."""
        return True if np.linalg.norm(self.get_vec(withExtrusion=True)) > 0 else False

    def is_extruding(self):
        """Return True if extrusion velocity is not zero."""
        return True if self.e > 0 else False


class position(vector_4D):
    """4D - Position object for (cartesian) 3D printer."""

    def __str__(self) -> str:
        """Print out position."""
        return "position: " + super().__str__()

    def is_travel(self, other) -> bool:
        """Return True if there is travel between self and other position."""
        if abs(other.x - self.x) + abs(other.y - self.y) + abs(other.z - self.z) > 0:
            return True
        else:
            return False

    def is_extruding(self, other) -> bool:
        """Return True if there is positive extrusion between self and other position."""
        if abs(other.e - self.e) > 0:
            return True
        else:
            return False

    def get_t_distance(self, other=None, withExtrusion=False) -> float:
        """Calculate the travel distance between self and other position. If none is provided, zero will be used."""
        if other is None:
            other = position(0, 0, 0, 0)
        return np.linalg.norm(
            np.subtract(self.get_vec(withExtrusion=withExtrusion), other.get_vec(withExtrusion=withExtrusion))
        )
