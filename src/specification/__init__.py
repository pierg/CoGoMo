from __future__ import annotations
from abc import ABC

from tools.nuxmv import Nuxmv
from tools.logic import LogicTuple
from typeset import Typeset


class Specification(ABC):

    def formula(self) -> (str, Typeset):
        pass

    def is_satisfiable(self) -> bool:
        return Nuxmv.check_satisfiability(self.formula())

    def is_valid(self) -> bool:
        return Nuxmv.check_validity(self.formula())

    def is_realizable(self) -> bool:
        pass

    def saturate(self, spec: Specification):
        pass

    def __hash__(self):
        return hash(self.formula()[0])

    def __lt__(self, other: Specification):
        """self < other. True if self is a refinement but not equal to other"""
        return self.__le__(other) and self.__ne__(other)

    def __le__(self: Specification, other: Specification):
        """self <= other. True if self is a refinement of other"""
        if other.is_valid():
            return True

        """Check if self -> other is valid"""
        return Nuxmv.check_validity(LogicTuple.implies_(self.formula(), other.formula(), brackets=True))

    def __gt__(self, other: Specification):
        """self > other. True if self is an abstraction but not equal to other"""
        return self.__ge__(other) and self.__ne__(other)

    def __ge__(self, other: Specification):
        """self >= other. True if self is an abstraction of other"""
        if self.is_valid():
            return True

        """Check if self -> other is valid"""
        return Nuxmv.check_validity(LogicTuple.implies_(other.formula(), self.formula(), brackets=True))

    def __eq__(self, other: Specification):
        """Check if self -> other and other -> self"""
        if self.formula()[0] == other.formula()[0]:
            return True
        else:
            return self.__le__(other) and self.__ge__(other)

    def __ne__(self, other: Specification):
        """Check if self -> other and other -> self"""
        return not self.__eq__(other)

    """Abstract Operators, must be implemented can be conly confronted with equal subtypes"""

    def __and__(self, other: Specification) -> Specification:
        """self & other
        Returns a new Specification with the conjunction with other"""
        raise NotImplementedError

    def __or__(self, other: Specification) -> Specification:
        """self | other
        Returns a new Specification with the disjunction with other"""
        raise NotImplementedError

    def __invert__(self: Specification) -> Specification:
        """Returns a new Specification with the negation of self"""
        raise NotImplementedError

    def __rshift__(self, other: Specification) -> Specification:
        """>>
        Returns a new Specification that is the result of self -> other (implies)"""
        raise NotImplementedError

    def __lshift__(self, other: Specification) -> Specification:
        """<<
        Returns a new Specification that is the result of other -> self (implies)"""
        raise NotImplementedError

    def __iand__(self, other: Specification) -> Specification:
        """self &= other
        Modifies self with the conjunction with other"""
        raise NotImplementedError

    def __ior__(self, other: Specification) -> Specification:
        """self |= other
        Modifies self with the disjunction with other"""
        raise NotImplementedError
