from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from goal import Goal


def __le__(self: Goal, other: Goal):
    """Goal refinement"""
    """self <= other
    If has smaller guarantees and bigger assumptions"""
    if self.specification.assumptions >= other.specification.assumptions and self.specification.guarantees <= other.specification.guarantees:
        return True
    else:
        return False


