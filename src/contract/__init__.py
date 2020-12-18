from __future__ import annotations

from copy import deepcopy
from typing import Tuple, Set, Union

from contract.exceptions import *
from specification.atom import Atom
from specification.exceptions import NotSatisfiableException
from specification.formula import Specification, Formula, FormulaOutput
from typeset import Typeset


class Contract:
    def __init__(self,
                 assumptions: Union[Formula, Atom] = None,
                 guarantees: Union[Formula, Atom] = None,
                 saturate: bool = True):

        self.__assumptions = None
        self.__guarantees = None

        self.__setassumptions(assumptions)
        self.__setguarantees(guarantees, saturate)
        self.__checkfeasibility()

        self.composed_by = {self}
        self.conjoined_by = {self}

    def __str__(self: Contract):
        """Override the print behavior"""
        ret = "\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        if isinstance(self.assumptions, Formula):
            ret += '  assumption'
            ret += '\n  DNF:\t' + self.assumptions.print(FormulaOutput.DNF) + ""
            ret += '\n  CNF:\t' + self.assumptions.print(FormulaOutput.CNF) + "\n"
        else:
            ret += '\n  ATM:\t' + str(self.assumptions) + "\n"

        if isinstance(self.guarantees, Formula):
            ret += '\n  guarantees'
            ret += '\n  DNF:\t' + self.guarantees.print(FormulaOutput.DNF) + ""
            ret += '\n  CNF:\t' + self.guarantees.print(FormulaOutput.CNF) + "\n"
        else:
            ret += '\n  ATM:\t' + str(self.guarantees) + "\n"
        ret += "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"

        return ret

    def formula(self) -> Tuple[str, Typeset]:
        """Generate the contract formula A->G"""

        return (self.assumptions >> self.guarantees).formula()

    @property
    def assumptions(self) -> Formula:
        return self.__assumptions

    @assumptions.setter
    def assumptions(self, value: Specification):
        self.__setassumptions(value)
        self.__checkfeasibility()

    @property
    def guarantees(self) -> Formula:
        """Returning saturated guarantee"""
        return self.__guarantees

    @guarantees.setter
    def guarantees(self, value: Specification):
        self.__setguarantees(value)
        self.__checkfeasibility()

    def __setassumptions(self, value: Specification):
        """Setting Assumptions"""
        if value is None:
            self.__assumptions = Formula()
        else:
            if not isinstance(value, Specification):
                raise AttributeError
            """Every contracts assigns a **copy** of A and G"""
            if isinstance(value, Atom):
                self.__assumptions = Formula(value)
            elif isinstance(value, Formula):
                self.__assumptions = deepcopy(value)

    def __setguarantees(self, value: Specification, saturate=True):
        if value is None:
            self.__guarantees = Formula()
        else:
            if not isinstance(value, Specification):
                raise AttributeError
            """Every contracts assigns a **copy** of A and G"""
            if isinstance(value, Atom):
                self.__guarantees = Formula(value)
            elif isinstance(value, Formula):
                self.__guarantees = deepcopy(value)
        """Saturate the guarantees"""
        if saturate:
            self.__guarantees.saturate(self.__assumptions)

    def __checkfeasibility(self):
        """Check Feasibility"""
        if self.assumptions is not None:
            try:
                self.__assumptions & self.__guarantees
            except NotSatisfiableException:
                raise UnfeasibleContracts(self.assumptions, self.guarantees)

    @staticmethod
    def composition(contracts: Set[Contract]) -> Contract:
        if len(contracts) == 1:
            return next(iter(contracts))
        if len(contracts) == 0:
            raise Exception("No contract specified in the composition")

        contract_list = list(contracts)
        new_assumptions = deepcopy(contract_list[0].assumptions)
        new_guarantees = deepcopy(contract_list[0].guarantees)

        """Populate the data structure while checking for compatibility and consistency"""
        for contract in contract_list[1:]:

            try:
                new_assumptions &= contract.assumptions
            except NotSatisfiableException as e:
                print("Contracts inconsistent")
                print(e.conj_a)
                print("unsatisfiable with")
                print(e.conj_b)
                raise IncompatibleContracts(e.conj_a, e.conj_b)

            try:
                new_guarantees &= contract.guarantees
            except NotSatisfiableException as e:
                print("Contracts incompatible")
                print(e.conj_a)
                print("unsatisfiable with")
                print(e.conj_b)
                raise InconsistentContracts(e.conj_a, e.conj_b)

        print("The composition is compatible and consistent")

        """Assumption relaxation"""
        new_assumptions.relax_by(new_guarantees)

        """New contracts without saturation cause it was already saturated"""
        new_contract = Contract(assumptions=new_assumptions, guarantees=new_guarantees, saturate=False)

        new_contract.composed_by = contracts

        return new_contract

    @staticmethod
    def conjunction(contracts: Set[Contract]) -> Contract:
        if len(contracts) == 1:
            return next(iter(contracts))
        if len(contracts) == 0:
            raise Exception("No contract specified in the composition")

        contracts_list = list(contracts)

        new_contract: Contract = contracts_list[0]

        """Populate the data structure while checking for compatibility and consistency"""
        for contract in contracts_list[1:]:

            try:
                new_contract.assumptions &= contract.assumptions
            except NotSatisfiableException as e:
                print("Contracts inconsistent")
                print(e.conj_a)
                print("unsatisfiable with")
                print(e.conj_b)
                raise IncompatibleContracts(e.conj_a, e.conj_b)

            try:
                new_contract.guarantees &= contract.guarantees
            except NotSatisfiableException as e:
                print("Contracts incompatible")
                print(e.conj_a)
                print("unsatisfiable with")
                print(e.conj_b)
                raise InconsistentContracts(e.conj_a, e.conj_b)

            try:
                new_contract.assumptions & new_contract.guarantees
            except NotSatisfiableException as e:
                print("Contracts unfeasible")
                print(e.conj_a)
                print("unsatisfiable with")
                print(e.conj_b)
                raise UnfeasibleContracts(e.conj_a, e.conj_b)

        print("The composition is compatible, consistent and feasible")

        """Assumption relaxation"""
        new_contract.__assumptions |= ~ new_contract.__guarantees

        new_contract.composed_by = contracts
        return new_contract
