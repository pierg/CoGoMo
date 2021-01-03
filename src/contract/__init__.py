from __future__ import annotations

from copy import deepcopy
from typing import Set, Tuple, List

from contract.exceptions import *
from controller.controllerinfo import ControllerInfo
from specification import FormulaOutput
from specification.atom import Atom
from specification.exceptions import NotSatisfiableException
from specification.formula import Specification, Formula
from typeset import Typeset


class Contract:
    def __init__(self,
                 assumptions: Specification = None,
                 guarantees: Specification = None,
                 saturate: bool = True):

        self.__assumptions = None
        self.__guarantees = None

        self.__setassumptions(assumptions)
        self.__setguarantees(guarantees, saturate)
        self.__checkfeasibility()

        self.composed_by = {self}
        self.conjoined_by = {self}

    from ._copying import __deepcopy__
    from ._printing import __str__

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
            self.__assumptions = Formula("TRUE")
        else:
            if not isinstance(value, Specification):
                raise AttributeError
            """Every contracts assigns a **copy** of A and G"""
            if isinstance(value, Atom):
                self.__assumptions = Formula(deepcopy(value))
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
                self.__guarantees = Formula(deepcopy(value))
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
            except NotSatisfiableException as e:
                raise UnfeasibleContracts(self, e)

    def extract_controller_info(self) -> ControllerInfo:
        """Extract All Info Needed to Build a Controller from the Contract"""

        """Assumptions"""
        assumptions = []
        a_mutex = []
        a_liveness = []

        """Guarantees"""
        guarantees = []
        g_mutex = []
        g_adjacency = []

        a_typeset = Typeset()
        g_typeset = Typeset()

        list, typeset = self.assumptions.formula(FormulaOutput.ListCNF)
        assumptions.extend(list)
        a_typeset |= typeset

        list, typeset = self.guarantees.formula(FormulaOutput.ListCNF)
        guarantees.extend(list)
        g_typeset |= typeset

        """Adding Mutex Rules"""
        ret = Atom.extract_mutex_rules(a_typeset, output=FormulaOutput.ListCNF)
        if ret is not None:
            rules, typeset = ret
            a_mutex.extend(rules)
            a_typeset |= typeset

        ret = Atom.extract_mutex_rules(g_typeset, output=FormulaOutput.ListCNF)
        if ret is not None:
            rules, typeset = ret
            g_mutex.extend(rules)
            g_typeset |= typeset

        """Adding Adjacency Rules"""
        ret = Atom.extract_adjacency_rules(g_typeset, output=FormulaOutput.ListCNF)
        if ret is not None:
            rules, typeset = ret
            g_adjacency.extend(rules)
            g_typeset |= typeset

        alltypes = a_typeset | g_typeset

        """Adding Liveness To Sensors (input)"""
        ret = Atom.extract_liveness_rules(alltypes, output=FormulaOutput.ListCNF)
        if ret is not None:
            rules, typeset = ret
            a_liveness.extend(rules)

        """Extract Inputs and Outputs"""
        inputs = [t.name for t in alltypes.extract_inputs()]
        outputs = [t.name for t in alltypes.extract_outputs()]

        return ControllerInfo(assumptions=assumptions,
                              a_liveness=a_liveness,
                              a_mutex=a_mutex,
                              guarantees=guarantees,
                              g_mutex=g_mutex,
                              g_adjacency=g_adjacency,
                              inputs=inputs,
                              outputs=outputs)

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
                raise IncompatibleContracts(contract, e)

            try:
                new_guarantees &= contract.guarantees
            except NotSatisfiableException as e:
                raise InconsistentContracts(contract, e)

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

        contract_list = list(contracts)
        new_assumptions = deepcopy(contract_list[0].assumptions)
        new_guarantees = deepcopy(contract_list[0].guarantees)

        """Populate the data structure while checking for compatibility and consistency"""
        for contract in contract_list[1:]:

            new_assumptions |= contract.assumptions

            try:
                new_guarantees &= contract.guarantees
            except NotSatisfiableException as e:
                raise InconsistentContracts(contract, e)

        print("The conjunction is compatible and consistent")

        """New contracts without saturation cause it was already saturated"""
        new_contract = Contract(assumptions=new_assumptions, guarantees=new_guarantees, saturate=False)

        new_contract.conjoined_by = contracts

        return new_contract
