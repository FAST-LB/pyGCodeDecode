"""Result calculation for segments and planner blocks."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyGCodeDecode.planner_block import planner_block

from pyGCodeDecode.utils import segment


# new segment class spanned by pos, rest is "result"
class abstract_result(ABC):
    """Abstract class for result calculation."""

    @property
    @abstractmethod
    def name(self):
        """Name of the result. Has to be set in the derived class."""
        pass

    @abstractmethod
    def calc_pblock(self, pblock: "planner_block", **kwargs):
        """Calculate the result for a planner block."""
        pass

    @abstractmethod
    def calc_segm(self, segm: "segment", **kwargs):
        """Calculate the result for a segment."""
        pass


class acceleration_result(abstract_result):
    """The acceleration."""

    name = "acceleration"

    def calc_segm(self, segm: "segment", **kwargs):
        """Calculate the acceleration for a segment."""
        delta_v = segm.vel_end.get_norm() - segm.vel_begin.get_norm()
        delta_t = segm.get_segm_duration()

        if delta_t > 0:
            acc = delta_v / delta_t
        else:
            acc = 0
        segm.result[self.name] = acc

    def calc_pblock(self, pblock, **kwargs):
        """Calculate the acceleration for a planner block."""
        for segm in pblock.segments:
            self.calc_segm(segm, **kwargs)


class velocity_result(abstract_result):
    """The velocity."""

    name = "velocity"

    def calc_segm(self, segm: "segment", **kwargs):
        """Calculate the velocity for a segment."""
        segm.result[self.name] = [
            segm.vel_begin.get_norm(),
            segm.vel_end.get_norm(),
        ]

    def calc_pblock(self, pblock: "planner_block", **kwargs):
        """Calculate the velocity for a planner block."""
        for segm in pblock.segments:
            self.calc_segm(segm, **kwargs)


def get_all_result_calculators():
    """Get all results."""
    public_results = [
        acceleration_result(),
        velocity_result(),
    ]

    private_results = []
    # Try to import private results if the module exists
    try:
        from pyGCodeDecode.private_result import get_private_result_calculators

        private_results = get_private_result_calculators()
    except ImportError:
        # Private results module not available, continue with only public results
        pass

    return public_results + private_results


def has_private_results():
    """Check if private results are available."""
    try:
        from pyGCodeDecode.private_result import (  # noqa: F401
            get_private_result_calculators,
        )

        return True
    except ImportError:
        return False


def get_result_info():
    """Get information about available result calculators."""
    all_calcs = get_all_result_calculators()
    public_count = 2  # acceleration_result and velocity_result
    private_count = len(all_calcs) - public_count

    return {
        "total_count": len(all_calcs),
        "public_count": public_count,
        "private_count": private_count,
        "has_private": has_private_results(),
        "result_names": [calc.name for calc in all_calcs],
    }


if __name__ == "__main__":
    pass
