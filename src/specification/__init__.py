from __future__ import annotations
from abc import ABC, abstractmethod
from specification.enums import *
from specification.exceptions import NotSatisfiableException
from tools.nuxmv import Nuxmv
from typeset import Typeset


class Specification(ABC):

    @property
    def string(self) -> str:
        return self.formula()[0]

    @property
    def typeset(self) -> Typeset:
        return self.formula()[1]

    def __hash__(self):
        return hash(self.string)

    """Abstract Operators, must be implemented can be conly confronted with equal subtypes"""

    @abstractmethod
    def formula(self) -> (str, Typeset):
        pass

    @property
    @abstractmethod
    def spec_kind(self) -> SpecKind:
        pass

    @abstractmethod
    def __and__(self, other: Specification) -> Specification:
        """self & other
        Returns a new Specification with the conjunction with other"""
        pass

    @abstractmethod
    def __or__(self, other: Specification) -> Specification:
        """self | other
        Returns a new Specification with the disjunction with other"""
        pass

    @abstractmethod
    def __invert__(self: Specification) -> Specification:
        """Returns a new Specification with the negation of self"""
        pass

    @abstractmethod
    def __rshift__(self, other: Specification) -> Specification:
        """>>
        Returns a new Specification that is the result of self -> other (implies)"""
        pass

    @abstractmethod
    def __lshift__(self, other: Specification) -> Specification:
        """<<
        Returns a new Specification that is the result of other -> self (implies)"""
        pass

    @abstractmethod
    def __iand__(self, other: Specification) -> Specification:
        """self &= other
        Modifies self with the conjunction with other"""
        pass

    @abstractmethod
    def __ior__(self, other: Specification) -> Specification:
        """self |= other
        Modifies self with the disjunction with other"""
        pass

    @abstractmethod
    def contains_rule(self, other: AtomKind = None) -> bool:
        pass

    """"Comparing Specifications"""

    def is_satisfiable(self) -> bool:
        if self.is_valid():
            return True

        sat_check_formula = self

        if not (self.contains_rule()):
            from specification.formula import Formula
            mutex_rules = Formula.extract_mutex_rules(self.typeset)
            try:
                self & mutex_rules
                return True
            except NotSatisfiableException:
                return False
        return Nuxmv.check_satisfiability(sat_check_formula.formula())

    def is_valid(self) -> bool:
        return Nuxmv.check_validity(self.formula())

    def __lt__(self, other: Specification):
        """self < other. True if self is a refinement but not equal to other"""
        return self.__le__(other) and self.__ne__(other)

    def __le__(self: Specification, other: Specification):
        """self <= other. True if self is a refinement of other"""
        if other.is_valid():
            return True

        """Check if self -> other is valid, considering the refinement rules r"""
        """((r & s1) -> s2) === r -> (s1 -> s2)"""
        from specification.formula import Formula
        refinement_rules = Formula.extract_refinement_rules(self.typeset | other.typeset)
        ref_check_formula = (self & refinement_rules) >> other
        return Nuxmv.check_validity(ref_check_formula.formula())

    def __gt__(self, other: Specification):
        """self > other. True if self is an abstraction but not equal to other"""
        return self.__ge__(other) and self.__ne__(other)

    def __ge__(self, other: Specification):
        """self >= other. True if self is an abstraction of other"""
        if self.is_valid():
            return True

        """Check if other -> self is valid, considering the refinement rules r"""
        """((r & s1) -> s2) === r -> (s1 -> s2)"""
        from specification.formula import Formula
        refinement_rules = Formula.extract_refinement_rules(self.typeset | other.typeset)
        ref_check_formula = (other & refinement_rules) << self
        return Nuxmv.check_validity(ref_check_formula.formula())

    def __eq__(self, other: Specification):
        """Check if self -> other and other -> self"""
        if self.string == other.string:
            return True
        else:
            return self.__le__(other) and self.__ge__(other)

    def __ne__(self, other: Specification):
        """Check if self -> other and other -> self"""
        return not self.__eq__(other)
