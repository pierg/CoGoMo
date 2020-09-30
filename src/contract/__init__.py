from __future__ import annotations
from formula import LTL
from contract.exceptions import UnfeasibleContracts
from typing import TypeVar, List, Set

from typeset import Typeset

LTL_types = TypeVar('LTL_types', bound=LTL)


class Contract:
    def __init__(self,
                 assumptions: LTL_types = None,
                 guarantees: LTL_types = None):

        self.__assumptions = None
        self.__guarantees = None

        """Properties"""
        self.guarantees = guarantees
        self.assumptions = assumptions

        self.composed_by = {self}
        self.conjoined_by = {self}

    """Imported methods"""
    from ._printing import __str__
    from ._copying import __deepcopy__
    from ._operators import __iand__, __ior__
    # from ._functions import propagate_assumptions_from

    @property
    def assumptions(self) -> LTL_types:
        return self.__assumptions

    @assumptions.setter
    def assumptions(self, value: LTL_types):
        if value is None:
            self.__assumptions = LTL("TRUE")
        else:
            if not isinstance(value, LTL):
                raise AttributeError
            self.__assumptions = value
            self.__guarantees.saturation = value
        """Check Feasibility"""
        if not self.assumptions.is_satisfiable_with(self.guarantees):
            raise UnfeasibleContracts(self.assumptions, self.guarantees)

    @property
    def guarantees(self) -> LTL_types:
        return self.__guarantees

    @guarantees.setter
    def guarantees(self, value: LTL_types):
        if value is None:
            self.__guarantees = LTL("TRUE")
        else:
            if not isinstance(value, LTL):
                raise AttributeError
            self.__guarantees = value
        """Check Feasibility"""
        if self.assumptions is not None:
            if not self.assumptions.is_satisfiable_with(self.guarantees):
                raise UnfeasibleContracts(self.assumptions, self.guarantees)

    @property
    def context(self) -> LTL_types:
        return self.__guarantees.context

    @context.setter
    def context(self, value: LTL_types):
        self.guarantees.context = value

    @property
    def composed_by(self) -> Set[Contract]:
        return self.__composed_by

    @composed_by.setter
    def composed_by(self, value: Set[Contract]):
        self.__composed_by = value

    @property
    def conjoined_by(self) -> List[Contract]:
        return self.__conjoined_by

    @conjoined_by.setter
    def conjoined_by(self, value: List[Contract]):
        self.__conjoined_by = value

    @property
    def variables(self) -> Typeset:
        return self.guarantees.variables | self.assumptions.variables

    @property
    def cost(self):
        """Used for component selection. Always [0, 1]
        Lower is better"""
        lg = len(self.guarantees.cnf)
        la = len(self.assumptions.cnf)

        """heuristic
        Low: guarantees while assuming little (assumption set is bigger)
        High: guarantees while assuming a lot (assumption set is smaller)"""

        return la / lg

    def propagate_assumptions_from(self: Contract, other: Contract):
        self.assumptions &= other.assumptions
