from __future__ import annotations

from copy import deepcopy
from typing import Tuple, Set

from contract.exceptions import *
from specification.atom import Atom
from specification.exceptions import NotSatisfiableException
from specification.formula import Specification, Formula
from typeset import Typeset


class Contract:
    def __init__(self,
                 assumptions: Specification = None,
                 guarantees: Specification = None):

        self.__assumptions = None
        self.__guarantees = None

        """Setting Assumptions"""
        if assumptions is None:
            self.__assumptions = Formula()
        else:
            if not isinstance(assumptions, Specification):
                raise AttributeError
            """Every contracts assigns a **copy** of A and G"""
            self.__assumptions = deepcopy(assumptions)

        """Setting Guarantees"""
        if guarantees is None:
            self.__guarantees = Formula()
        else:
            if not isinstance(assumptions, Specification):
                raise AttributeError
            """Every contracts assigns a **copy** of A and G"""
            self.__guarantees = deepcopy(guarantees)

            """Saturating the guarantees
            a -> ((g1 | g2) & (g3 | g4)) === (((a ->g1) | (a ->g2)) & ((a ->g3) | (a ->g4)))
            """
            if isinstance(self.__guarantees, Atom):
                self.__guarantees.saturation = self.__assumptions
            elif isinstance(self.__guarantees, Formula):
                for clause in self.__guarantees.cnf:
                    for g in clause:
                        g.saturation = self.__assumptions

        """Check Feasibility"""
        try:
            self.__assumptions & self.__guarantees
        except NotSatisfiableException:
            raise UnfeasibleContracts(self.assumptions, self.guarantees)

        self.composed_by = {self}
        self.conjoined_by = {self}

        """Imported methods"""
        from ._printing import __str__
        from ._copying import __deepcopy__
        from ._operators import __ior__, __iand__

    def formula(self) -> Tuple[str, Typeset]:
        """Generate the contract formula A->G"""

        return (self.assumptions >> self.guarantees).formula()

    @property
    def assumptions(self) -> Specification:
        return self.__assumptions

    @assumptions.setter
    def assumptions(self, value: Specification):
        if value is None:
            self.__assumptions = Specification()
        else:
            if not isinstance(value, Specification):
                raise AttributeError
            """Every contracts assigns a **copy** of A and G, so each contract has its saturated G"""
            self.__assumptions = deepcopy(value)
        """Check Feasibility"""
        if not (self.assumptions & self.guarantees).is_satisfiable():
            raise UnfeasibleContracts(self.assumptions, self.guarantees)

    @property
    def guarantees(self) -> Specification:
        """Returning saturated guarantee"""
        return self.__guarantees

    @guarantees.setter
    def guarantees(self, value: Specification):
        if value is None:
            self.__guarantees = Specification()
        else:
            if not isinstance(value, Specification):
                raise AttributeError
            """Every contracts assigns a **copy** of A and G, so each contract has its saturated G"""
            self.__guarantees = deepcopy(value)
        """Check Feasibility"""
        if self.assumptions is not None:
            if not (self.assumptions & self.guarantees).is_satisfiable():
                raise UnfeasibleContracts(self.assumptions, self.guarantees)

    @staticmethod
    def composition(contracts: Set[Contract]) -> Contract:
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
        cnf = new_contract.assumptions.cnf
        dnf = new_contract.assumptions.dnf
        new_contract.__assumptions |= ~ new_contract.__guarantees

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
