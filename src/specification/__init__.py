from __future__ import annotations
from abc import ABC

from tools.nuxmv import Nuxmv
from typeset import Typeset


class Specification(ABC):

    def formula(self) -> (str, Typeset): pass

    def is_satisfiable(self) -> bool:
        return Nuxmv.check_satisfiability(self.formula)

    def is_realizable(self) -> bool: pass

    def __lt__(self, other: Specification):
        a = self.formula
        b = other.formula
        return a + b

    def __le__(self: Specification, other: Specification): pass

    def __eq__(self, other: Specification): pass

    def __ne__(self, other: Specification): pass

    def __gt__(self, other: Specification): pass

    def __ge__(self, other: Specification): pass

