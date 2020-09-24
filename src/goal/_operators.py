from __future__ import annotations
from typing import TYPE_CHECKING

from goal.exceptions import GoalFailException, FailOperations, FailMotivations

if TYPE_CHECKING:
    from goal import Goal, Link


def __le__(self: Goal, other: Goal):
    """Goal refinement"""
    """self <= other
    If has smaller guarantees and bigger assumptions"""
    if self.specification.assumptions >= other.specification.assumptions and self.specification.guarantees <= other.specification.guarantees:
        return True
    else:
        return False


def refine_by(self: Goal, other: Goal, consolidate: True):
    """Refine self by other"""

    """Propagate assumptions from other to self"""
    self.specification.propagate_assumptions_from(other.specification)

    if other <= self:
        self.children[other] = Link.REFINEMENT
    else:
        raise GoalFailException(
            failed_operation=FailOperations.refinement,
            faild_motivation=FailMotivations.wrong_refinement,
            goals_involved_a=[self],
            goals_involved_b=[other]
        )

    if consolidate:
        self.consolidate_bottom_up()
