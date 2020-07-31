from copy import deepcopy
from typing import List
from typescogomo.formula import LTL, InconsistentException
from typescogomo.variables import Variables, Boolean


class Contract:
    def __init__(self,
                 assumptions: LTL = None,
                 guarantees: LTL = None
                 ):

        """List of assumptions in conjunction"""
        if assumptions is None:
            self.__assumptions = LTL()
        else:
            self.__assumptions = assumptions

        """List of guarantees in conjunction. All guarantees are saturated"""
        if guarantees is None:
            self.__guarantees = LTL()
        else:
            self.__guarantees = guarantees

        self.__guarantees.saturation = self.__assumptions

        self.check_feasibility()

    @property
    def variables(self):
        return self.assumptions.variables | self.guarantees.variables

    @property
    def assumptions(self) -> LTL:
        return self.__assumptions

    @assumptions.setter
    def assumptions(self, values: LTL):
        if not isinstance(values, LTL):
            raise AttributeError
        self.__assumptions = values

    @property
    def guarantees(self) -> LTL:
        return self.__guarantees

    @property
    def context(self) -> LTL:
        return self.__guarantees.context

    @guarantees.setter
    def guarantees(self, values: LTL):
        if not isinstance(values, LTL):
            raise AttributeError
        self.__guarantees = values

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    """Contract refinement"""

    def __le__(self, other):
        """self <= other
        If has smaller guarantees and bigger assumptions"""
        if self.assumptions >= other.assumptions and self.guarantees <= other.guarantees:
            return True
        else:
            return False

    def merge_with(self, other: 'Contract'):

        try:
            self.assumptions &= other.assumptions
        except InconsistentException as e:
            raise IncompatibleContracts(e.conj_a, e.conj_b)

        try:
            self.guarantees &= other.guarantees
        except InconsistentException as e:
            raise InconsistentContracts(e.conj_a, e.conj_b)

        self.check_feasibility()

    def check_feasibility(self):
        if not self.assumptions.is_satisfiable_with(self.guarantees):
            raise UnfeasibleContracts(self.assumptions, self.guarantees)

    def propagate_assumptions_from(self, c: 'Contract'):

        self.assumptions &= c.assumptions

    def add_assumption(self, a: 'LTL'):
        self.assumptions &= a

    def set_context(self, context: LTL):
        self.guarantees.context = context


    def cost(self):
        """Used for component selection. Always [0, 1]
        Lower is better"""
        lg = len(self.guarantees.cnf)
        la = len(self.assumptions.cnf)

        """heuristic
        Low: guarantees while assuming little (assumption set is bigger)
        High: guarantees while assuming a lot (assumption set is smaller)"""

        return la / lg

    def add_domain_properties(self):
        pass

    def __str__(self):
        """Override the print behavior"""
        astr = '  variables:\t[ '
        for var in self.variables:
            astr += str(var) + ', '
        astr = astr[:-2] + ' ]\n  assumptions      :\t[ '
        for assumption in self.assumptions.cnf:
            astr += assumption.formula + ', '
        astr = astr[:-2] + ' ]\n  guarantees       :\t[ '
        for guarantee in self.guarantees.cnf:
            astr += guarantee.formula + ', '
        # astr = astr[:-2] + ' ]\n  guarantees_unsat :\t[ '
        # for guarantee in self.guarantees.cnf:
        #     astr += guarantee.unsaturated + ', '
        return astr[:-2] + ' ]\n'


class IncompatibleContracts(Exception):
    def __init__(self, assumptions_1: LTL, assumptions_2: LTL):
        self.assumptions_1 = assumptions_1
        self.assumptions_2 = assumptions_2


class InconsistentContracts(Exception):
    def __init__(self, guarantee_1: LTL, guarantee_2: LTL):
        self.guarantee_1 = guarantee_1
        self.guarantee_2 = guarantee_2


class UnfeasibleContracts(Exception):
    def __init__(self, assumptions: LTL, guarantees: LTL):
        self.assumptions = assumptions
        self.guarantees = guarantees


class BooleanContract(Contract):

    def __init__(self,
                 assumptions_str: List[str],
                 guarantees_str: List[str]):

        assumptions = set()
        guarantees = set()

        for a in assumptions_str:
            assumptions.add(LTL(a, Variables({Boolean(a)})))

        for g in guarantees_str:
            guarantees.add(LTL(g, Variables({Boolean(g)})))

        assumptions = LTL(cnf=assumptions)
        guarantees = LTL(cnf=guarantees)

        guarantees.saturate_with(assumptions)

        super().__init__(assumptions=assumptions,
                         guarantees=guarantees)


class SimpleContract(Contract):

    def __init__(self,
                 guarantees: List[str],
                 assumptions: List[str] = None):

        guarantees_obj = set()

        from typescogomo.variables import extract_variable

        for g in guarantees:
            guarantees_obj.add(LTL(g, extract_variable(g)))

        guarantees_obj = LTL(cnf=guarantees_obj)

        if assumptions is None:
            assumptions_obj = LTL()

        else:
            assumptions_obj = set()

            for a in assumptions:
                assumptions_obj.add(LTL(a, extract_variable(a)))

            assumptions_obj = LTL(cnf=assumptions_obj)
            guarantees_obj.saturate_with(assumptions_obj)

        super().__init__(assumptions=assumptions_obj,
                         guarantees=guarantees_obj)


class PContract(Contract):

    def __init__(self, patterns: List[LTL]):
        self.patterns = patterns

        variables = Variables()

        guarantees = set()
        for p in patterns:
            guarantees.add(p)
            # variables |= p.variables
            # guarantees.add(LTL(p.formula, p.variables))

        guarantees = LTL(cnf=guarantees)

        super().__init__(guarantees=guarantees)
