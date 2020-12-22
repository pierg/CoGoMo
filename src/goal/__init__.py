from __future__ import annotations

from typing import Union, Set

from contract import Contract, IncompatibleContracts, InconsistentContracts, UnfeasibleContracts
from goal.exceptions import GoalFailException, FailOperations, FailMotivations
from specification import Specification
from specification.formula import FormulaOutput
from tools.strings import StringMng


class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)


class ContractChangedObservable:
    def __init__(self):
        self.property_changed = Event()


class Goal:

    def __init__(self,
                 name: str = None,
                 description: str = None,
                 specification: Union[Specification, Contract] = None,
                 context: Specification = None):

        """Read only properties"""
        self.__realizable = None
        self.__controller = None
        self.__time_synthesis = None

        """Properties defined on first instantiation"""
        self.name: str = name
        self.description: str = description
        self.specification: Contract = specification
        self.context: Specification = context

    def __str__(self):
        return Goal.pretty_print_goal(self)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name, self.__id = StringMng.get_name_and_id(value)

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        if value is None:
            self.__description: str = ""
        else:
            self.__description: str = value

    @property
    def specification(self) -> Contract:
        return self.__specification

    @specification.setter
    def specification(self, value: Union[Contract, Specification]):
        if isinstance(value, Contract):
            self.__specification: Contract = value
        elif isinstance(value, Specification):
            self.__specification: Contract = Contract(guarantees=value)

    @property
    def context(self) -> Specification:
        return self.__context

    @context.setter
    def context(self, value: Specification):
        self.__context = value

    @property
    def realizable(self) -> bool:
        return self.__realizable

    @property
    def controller(self) -> str:
        return self.__controller

    @property
    def time_synthesis(self) -> int:
        return round(self.__time_synthesis, 2)

    @staticmethod
    def pretty_print_goal(goal: Goal, level=0):
        ret = "\t" * level + "|---GOAL\t" + repr(goal.name) + "\n"
        if goal.context is not None:
            ret += "\t" * level + "|\tCONTEXT:\t" + str(goal.context) + "\n"
        if not goal.specification.assumptions.is_valid():
            ret += "\t" * level + "|\tASSUMPTIONS:\n"
            ret += "\t" * level + "|\t" + goal.specification.assumptions.pretty_print(FormulaOutput.DNF) + "\n"
        ret += "\t" * level + "|\tGUARANTEES:\n"
        ret += "\t" * level + "|\t" + goal.specification.guarantees.pretty_print(FormulaOutput.CNF) + "\n"
        return ret

    @staticmethod
    def composition(goals: Set[Goal], name: str = None, description: str = None) -> Goal:
        if name is None:
            names = []
            for goal in goals:
                names.append(goal.name)
            names.sort()
            conj_name = ""
            for name in names:
                conj_name += name + "||"
            name = conj_name[:-2]

        set_of_contracts = set()
        for g in goals:
            set_of_contracts.add(g.specification)

        try:
            new_contract = Contract.composition(set_of_contracts)

        except IncompatibleContracts as e:
            goals_involved = []
            goals_failed = []
            for goal in goals:
                for contract in goal.specification.conjoined_by:
                    if e.assumptions_1 <= contract.assumptions:
                        goals_involved.append(goal)
                    if e.assumptions_2 <= contract.assumptions:
                        goals_failed.append(goal)
            raise GoalFailException(failed_operation=FailOperations.composition,
                                    faild_motivation=FailMotivations.incompatible,
                                    goals_involved_a=goals_involved,
                                    goals_involved_b=goals_failed)

        except InconsistentContracts as e:
            goals_involved = []
            goals_failed = []
            for goal in goals:
                for contract in goal.specification.conjoined_by:
                    if e.guarantee_1 <= contract.guarantees:
                        goals_involved.append(goal)
                    if e.guarantee_2 >= contract.guarantees:
                        goals_failed.append(goal)
            raise GoalFailException(failed_operation=FailOperations.composition,
                                    faild_motivation=FailMotivations.inconsistent,
                                    goals_involved_a=goals_involved,
                                    goals_involved_b=goals_failed)

        except UnfeasibleContracts as e:

            goals_involved = []
            goals_failed = []
            for goal in goals:
                for contract in goal.specification.conjoined_by:
                    if e.assumptions <= contract.assumptions:
                        goals_involved.append(goal)
                    if e.guarantees <= contract.assumptions:
                        goals_failed.append(goal)
            raise GoalFailException(failed_operation=FailOperations.composition,
                                    faild_motivation=FailMotivations.unfeasible,
                                    goals_involved_a=goals_involved,
                                    goals_involved_b=goals_failed)

        new_goal = Goal(name=name,
                        description=description,
                        specification=new_contract)

        return new_goal

    @staticmethod
    def conjunction(goals: Set[Goal], name: str = None, description: str = None) -> Goal:
        if name is None:
            names = []
            for goal in goals:
                names.append(goal.name)
            names.sort()
            conj_name = ""
            for name in names:
                conj_name += name + "^^"
            name = conj_name[:-2]

        set_of_contracts = set()
        for g in goals:
            set_of_contracts.add(g.specification)

        try:
            new_contract = Contract.conjunction(set_of_contracts)

        except InconsistentContracts as e:
            goals_involved = []
            goals_failed = []
            for goal in goals:
                for contract in goal.specification.conjoined_by:
                    if e.guarantee_1 <= contract.guarantees:
                        goals_involved.append(goal)
                    if e.guarantee_2 >= contract.guarantees:
                        goals_failed.append(goal)
            raise GoalFailException(failed_operation=FailOperations.conjunction,
                                    faild_motivation=FailMotivations.inconsistent,
                                    goals_involved_a=goals_involved,
                                    goals_involved_b=goals_failed)

        new_goal = Goal(name=name,
                        description=description,
                        specification=new_contract)

        return new_goal
