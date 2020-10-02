from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

from contract.exceptions import IncompatibleContracts, InconsistentContracts
from formula import InconsistentException, LTL
from tools.logic import And

if TYPE_CHECKING:
    from contract import Contract


def __iand__(self: Contract, other: Contract):
    """self &= other. And of assumptions and guarantees"""
    """ A = a1 & a2
        G = (a1 & a2) -> ((a1 -> g1) & (a2 -> g2)) = (a1 & a2 ) -> (g1 & g2)"""

    try:
        self.assumptions &= other.assumptions
    except InconsistentException as e:
        raise IncompatibleContracts(e.conj_a, e.conj_b)

    base_self = self.guarantees.base_formula
    base_other = other.guarantees.base_formula
    try:
        self.guarantees &= other.guarantees
    except InconsistentException as e:
        raise InconsistentContracts(e.conj_a, e.conj_b)

    old_guarantees = deepcopy(self.guarantees)
    old_guarantees.base_formula = And([base_self, base_other])
    old_guarantees.saturation = self.assumptions

    self.guarantees.saturation = self.assumptions

    if old_guarantees == self.guarantees:
        self.guarantees.base_formula = And([base_self, base_other])

    return self


def __ior__(self: Contract, other: Contract):
    """self |= other. Or of assumptions and  And of (saturated) guarantees"""
    try:
        self.assumptions |= other.assumptions
    except InconsistentException as e:
        raise IncompatibleContracts(e.conj_a, e.conj_b)
    try:
        self.guarantees &= other.guarantees
    except InconsistentException as e:
        raise InconsistentContracts(e.conj_a, e.conj_b)

    return self

