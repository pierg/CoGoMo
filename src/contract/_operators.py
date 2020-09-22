from __future__ import annotations
from typing import TYPE_CHECKING

from contract.exceptions import IncompatibleContracts, InconsistentContracts
from formula import InconsistentException

if TYPE_CHECKING:
    from contract import Contract


def __iand__(self, other: Contract):
    """self &= other. And of assumptions and guarantees"""
    try:
        self.assumptions &= other.assumptions
    except InconsistentException as e:
        raise IncompatibleContracts(e.conj_a, e.conj_b)

    try:
        self.guarantees &= other.guarantees
    except InconsistentException as e:
        raise InconsistentContracts(e.conj_a, e.conj_b)


def __ior__(self, other: Contract):
    """self |= other. Or of assumptions and  And of (saturated) guarantees"""
    try:
        self.assumptions |= other.assumptions
    except InconsistentException as e:
        raise IncompatibleContracts(e.conj_a, e.conj_b)
    try:
        self.guarantees &= other.guarantees
    except InconsistentException as e:
        raise InconsistentContracts(e.conj_a, e.conj_b)