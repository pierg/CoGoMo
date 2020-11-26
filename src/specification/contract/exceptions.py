from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from specification.formula import Formula
    from typing import TypeVar
    Formula_types = TypeVar('Formula_types', bound=Formula)


class IncompatibleContracts(Exception):
    def __init__(self, assumptions_1: Formula_types, assumptions_2: Formula_types):
        self.assumptions_1 = assumptions_1
        self.assumptions_2 = assumptions_2


class InconsistentContracts(Exception):
    def __init__(self, guarantee_1: Formula_types, guarantee_2: Formula_types):
        self.guarantee_1 = guarantee_1
        self.guarantee_2 = guarantee_2


class UnfeasibleContracts(Exception):
    def __init__(self, assumptions: Formula_types, guarantees: Formula_types):
        self.assumptions = assumptions
        self.guarantees = guarantees