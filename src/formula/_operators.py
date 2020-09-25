from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Union
from tools.logic import And, Implies, Not, Or

from formula import InconsistentException
from formula.exceptions import DifferentContextException
from typeset.types.basic import Boolean
from tools.nusmv import check_validity


if TYPE_CHECKING:
    from formula import LTL



"""Refinement operators"""


def __lt__(self, other: LTL):
    """Check if the set of behaviours is smaller in the other set of behaviours"""
    if self.formula == other.formula:
        return False
    lt = self <= other
    neq = self != other
    return lt and neq


def __le__(self, other: LTL):
    if other.is_true():
        return True
    """Create a new LTL self -> other and check its validity"""
    implication_formula = self >> other
    return check_validity(implication_formula.variables.get_nusmv_names(), implication_formula.formula)


def __eq__(self, other: LTL):
    """Check if the set of behaviours is equal to the other set of behaviours"""
    if self.formula == other.formula:
        return True
    implied_a = self >= other
    implied_b = self <= other
    return implied_a and implied_b


def __ne__(self, other: LTL):
    """Check if the set of behaviours is different from the other set of behaviours"""
    return not (self == other)


def __gt__(self, other: LTL):
    """Check if the set of behaviours is bigger than the other set of behaviours"""
    gt = self >= other
    neq = self != other
    return gt and neq


def __ge__(self, other: LTL):
    if self.assign_true():
        return True
    """Create a new LTL self -> other anche check its validity"""
    implication_formula = other >> self
    return check_validity(implication_formula.variables.get_nusmv_names(), implication_formula.formula)
