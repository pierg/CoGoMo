from __future__ import annotations

from typing import Union, Set

from graphviz import Source

from contract import Contract, IncompatibleContracts, InconsistentContracts, UnfeasibleContracts
from controller import Controller
from controller.exceptions import ControllerException
from goal.exceptions import GoalFailOperations, GoalFailMotivations, GoalAlgebraOperationFail, GoalSynthesisFail
from specification import Specification
from specification.formula import FormulaOutput
from tools.storage import Store
from tools.strings import StringMng


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

        self.__folder_path = f"goals/{self.__id}"

    def __str__(self):
        return Goal.pretty_print_goal(self)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def folder_path(self) -> str:
        return self.__folder_path

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
    def controller(self) -> Controller:
        return self.__controller

    @property
    def time_synthesis(self) -> int:
        return round(self.__time_synthesis, 2)

    def realize_to_controller(self):
        """Realize the goal into a Controller object"""

        controller_info = self.specification.get_controller_info()

        a, g, i, o = controller_info.get_strix_inputs()

        try:
            controller_synthesis_input = StringMng.get_controller_synthesis_str(controller_info)

            Store.save_to_file(controller_synthesis_input, self.__folder_path, "controller_specs.txt")

            realized, dot_mealy, time = Controller.generate_controller(a, g, i, o)

            self.__realizable = realized
            self.__time_synthesis = time

            if realized:
                source = Store.generate_eps_from_dot(dot_mealy, self.__folder_path, "controller")
            else:
                source = Store.generate_eps_from_dot(dot_mealy, self.__folder_path, "controller_inverted")

            self.__controller = Controller(source=source)

        except ControllerException as e:
            raise GoalSynthesisFail(self, e)

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

            raise GoalAlgebraOperationFail(goals=goals, operation=GoalFailOperations.composition, contr_ex=e)

        except InconsistentContracts as e:

            raise GoalAlgebraOperationFail(goals=goals, operation=GoalFailOperations.composition, contr_ex=e)

        except UnfeasibleContracts as e:

            raise GoalAlgebraOperationFail(goals=goals, operation=GoalFailOperations.composition, contr_ex=e)

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

            raise GoalAlgebraOperationFail(goals=goals, operation=GoalFailOperations.conjunction, contr_ex=e)

        new_goal = Goal(name=name,
                        description=description,
                        specification=new_contract)

        return new_goal
