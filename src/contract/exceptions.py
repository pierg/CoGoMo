from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from formula import LTL
    from typing import TypeVar
    LTL_types = TypeVar('LTL_types', bound=LTL)


class IncompatibleContracts(Exception):
    def __init__(self, assumptions_1: LTL_types, assumptions_2: LTL_types):
        self.assumptions_1 = assumptions_1
        self.assumptions_2 = assumptions_2


class InconsistentContracts(Exception):
    def __init__(self, guarantee_1: LTL_types, guarantee_2: LTL_types):
        self.guarantee_1 = guarantee_1
        self.guarantee_2 = guarantee_2


class UnfeasibleContracts(Exception):
    def __init__(self, assumptions: LTL_types, guarantees: LTL_types):
        self.assumptions = assumptions
        self.guarantees = guarantees