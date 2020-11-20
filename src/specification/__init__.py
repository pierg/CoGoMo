from __future__ import annotations
from abc import ABC

from tools.nuxmv import Nuxmv
from typeset import Typeset


class Specification(ABC):

    def formula(self) -> (str, Typeset):
        pass

    def is_satisfiable(self) -> bool:
        return Nuxmv.check_satisfiability(self.formula)

    def is_valid(self) -> bool:
        return Nuxmv.check_validity(self.formula)

    def is_realizable(self) -> bool:
        pass

    def __lt__(self, other: Specification):
        """self < other. True if self is a refinement but not equal to other"""
        return self.__le__(other) and self.__ne__(other)

    def __le__(self: Specification, other: Specification):
        """self <= other. True if self is a refinement of other"""
        if other.is_valid():
            return True

        """Check if self -> other is valid"""
        return Nuxmv.check_validity(self >> other)

    def __eq__(self, other: Specification):
        """Check if self -> other and other -> self"""
        if self.formula == other.formula:
            return True
        else:
            return self.__le__(other) and self.__ne__(other)

    def __ne__(self, other: Specification):
        """Check if self -> other and other -> self"""
        return not self.__eq__(other)

    def __gt__(self, other: Specification):
        pass

    def __ge__(self, other: Specification):
        pass
