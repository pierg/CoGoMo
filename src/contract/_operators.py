from __future__ import annotations

from typing import TYPE_CHECKING

from contract import IncompatibleContracts, InconsistentContracts
from specification.formula import NotSatisfiableException

if TYPE_CHECKING:
    from contract import Contract


def __iand__(self: Contract, other: Contract):
    """self &= other. And of assumptions and guarantees"""
    """ A = a1 & a2
        G = (a1 & a2) -> ((a1 -> g1) & (a2 -> g2)) = (a1 & a2 ) -> (g1 & g2)"""

    try:
        self.assumptions &= other.assumptions
    except NotSatisfiableException as e:
        raise IncompatibleContracts(e.conj_a, e.conj_b)

    try:
        self.guarantees &= other.guarantees
    except NotSatisfiableException as e:
        raise InconsistentContracts(e.conj_a, e.conj_b)

    return self


def __ior__(self: Contract, other: Contract):
    """self |= other. Or of assumptions and  And of (saturated) guarantees"""
    try:
        self.assumptions |= other.assumptions
    except NotSatisfiableException as e:
        raise IncompatibleContracts(e.conj_a, e.conj_b)
    try:
        self.guarantees &= other.guarantees
    except NotSatisfiableException as e:
        raise InconsistentContracts(e.conj_a, e.conj_b)

    return self

