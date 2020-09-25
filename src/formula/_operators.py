from __future__ import annotations
from typing import TYPE_CHECKING, Union

from formula import InconsistentException
from typeset.types.basic import Boolean

if TYPE_CHECKING:
    from formula import LTL




    """Logic Operators"""

    def __iand__(self, other: Union[LTL, Boolean]) -> LTL:
        """self &= other
        Modifies self with the conjunction with other"""
        if isinstance(other, Boolean):
            other = other.is_true()

        if self.context is not None and other.context is not None:
            if self.context != other.context:
                raise DifferentContextException(self.context, other.context)

        if self.context is None and other.context is not None:
            raise DifferentContextException(self.context, other.context)

        """Contexts must be equal"""

        if self.__formula == "TRUE":
            self.__formula = deepcopy(other.formula)
            self.__variables = deepcopy(other.variables)
            self.__cnf = deepcopy(other.cnf)
            return self

        if other.formula == "TRUE":
            return self
        if other.formula == "FALSE":
            self.__formula = "FALSE"
            self.__cnf |= other.cnf
            return self

        self.__formula = And([self.__formula, other.unsaturated])
        self.__variables |= other.variables
        self.__cnf |= other.cnf

        if not self.is_satisfiable():
            raise InconsistentException(self, other)
        return self

    def __ior__(self, other: Union[LTL, Boolean]) -> LTL:
        """self |= other
        Modifies self with the disjunction with other"""
        if isinstance(other, Boolean):
            other = other.is_true()

        if self.__formula == "TRUE":
            return self

        if other.formula == "FALSE":
            return self
        if other.formula == "TRUE":
            self.__formula = "TRUE"
            self.__cnf |= other.cnf
            return self

        self.__formula = Or([self.formula, other.formula])
        self.__variables = self.variables | other.variables

        return self

    def __and__(self, other: Union[LTL, Boolean]) -> LTL:
        """self & other
        Returns a new LTL with the conjunction with other"""
        if isinstance(other, Boolean):
            other = other.is_true()

        return LTL(cnf={self, other})

    def __or__(self, other: Union[LTL, Boolean]) -> LTL:
        """self | other
        Returns a new LTL with the disjunction with other"""
        if isinstance(other, Boolean):
            other = other.is_true()

        formula = Or([self.formula, other.formula])
        variables = self.variables | other.variables

        return LTL(formula=formula, variables=variables)

    def __invert__(self: LTL) -> LTL:
        """Returns a new LTL with the negation of self"""

        formula = Not(self.formula)

        return LTL(formula=formula, variables=self.variables)

    def __rshift__(self, other: Union[LTL, Boolean]) -> LTL:
        """>>
        Returns a new LTL that is the result of self -> other (implies)"""
        if isinstance(other, Boolean):
            other = other.is_true()
        return LTL(
            formula=Implies(self.formula, other.formula),
            variables=self.variables | other.variables
        )

    def __lshift__(self, other: Union[LTL, Boolean]) -> LTL:
        """<<
        Returns a new LTL that is the result of other -> self (implies)"""
        if isinstance(other, Boolean):
            other = other.is_true()
        return LTL(
            formula=Implies(other.formula, self.formula),
            variables=self.variables | other.variables
        )

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
        if self.is_true():
            return True
        """Create a new LTL self -> other anche check its validity"""
        implication_formula = other >> self
        return check_validity(implication_formula.variables.get_nusmv_names(), implication_formula.formula)