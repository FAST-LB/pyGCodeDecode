"""Test the result calculation."""

import numpy as np

from pyGCodeDecode.utils import acceleration, position, seconds, velocity


def test_4d_vectors():
    """Test the 4d vector functions."""
    pos1 = position(1, 2, 3, 4)
    pos2 = position(4, 5, 6, 7)
    t = seconds(6)

    dist = pos2 - pos1
    # Check the distance vector
    assert np.isclose(dist.x, 3)
    assert np.isclose(dist.y, 3)
    assert np.isclose(dist.z, 3)
    assert np.isclose(dist.e, 3)

    vel = dist / t
    # Check the velocity vector
    assert isinstance(vel, velocity)
    assert np.isclose(vel.x, 0.5)
    assert np.isclose(vel.y, 0.5)
    assert np.isclose(vel.z, 0.5)
    assert np.isclose(vel.e, 0.5)

    # Check the norm of the velocity vector
    assert np.isclose(vel.get_norm(), np.sqrt(0.5**2 + 0.5**2 + 0.5**2))
    assert np.isclose(vel.get_norm(withExtrusion=True), np.sqrt(0.5**2 + 0.5**2 + 0.5**2 + 0.5**2))

    # Check the acceleration vector
    acc = vel / seconds(0.5)

    assert isinstance(acc, acceleration)
    assert np.isclose(acc.x, 1.0)
    assert np.isclose(acc.y, 1.0)
    assert np.isclose(acc.z, 1.0)
    assert np.isclose(acc.e, 1.0)
