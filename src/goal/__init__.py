from __future__ import annotations

from typing import Union, Set

from graphviz import Source

from contract import Contract, IncompatibleContracts, InconsistentContracts, UnfeasibleContracts
from controller import Controller
from controller.exceptions import ControllerException
from goal.exceptions import GoalException, GoalFailOperations, GoalFailMotivations, GoalAlgebraOperationFail, \
    GoalSynthesisFail
from specification import Specification
from specification.atom.pattern.basic import GF
from specification.formula import FormulaOutput
from tools.storage import Store
from tools.strings import StringMng
from worlds import World


class Goal:

    def __init__(self,
                 name: str = None,
                 description: str = None,
                 specification: Union[Specification, Contract] = None,
                 context: Specification = None,
                 world: World = None):

        """Read only properties"""
        self.__realizable = None
        self.__controller = None
        self.__time_synthesis = None

        """Properties defined on first instantiation"""
        self.name: str = name
        self.description: str = description
        self.specification: Contract = specification
        self.context: Specification = context
        self.world: World = world

        self.__session_name = None
        self.__goal_folder_name = f"goals/{self.__id}"

    def __str__(self):
        return Goal.pretty_print_goal(self)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> str:
        return self.__id

    @property
    def goal_folder_name(self) -> str:
        if self.__session_name is None:
            return self.__goal_folder_name
        else:
            return f"{self.session_name}/{self.__goal_folder_name}"

    @property
    def session_name(self) -> str:
        return self.__session_name

    @session_name.setter
    def session_name(self, value: str):
        if value is None:
            self.__session_name: str = ""
        else:
            self.__session_name: str = value

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

        """Adding (by conjunction) the context as a G(context) as contract assumption"""
        if value is not None:
            self.__specification.assumptions &= GF(value)

    @property
    def world(self) -> World:
        return self.__world

    @world.setter
    def world(self, value: World):
        self.__world = value

    @property
    def realizable(self) -> bool:
        return self.__realizable

    @property
    def controller(self) -> Controller:
        return self.__controller

    @property
    def time_synthesis(self) -> int:
        if self.__time_synthesis is not None:
            return round(self.__time_synthesis, 2)
        else:
            return -1

    def translate_to_buchi(self, cgg_path: str = None):

        if cgg_path is None:
            folder_path = self.goal_folder_name
        else:
            folder_path = f"{cgg_path}/{self.__goal_folder_name}"

        self.specification.assumptions.translate_to_buchi("assumptions", folder_path)
        self.specification.guarantees.translate_to_buchi("guarantees", folder_path)

    def realize_to_controller(self, cgg_path: str = None):
        """Realize the goal into a Controller object"""

        if cgg_path is None:
            folder_path = self.goal_folder_name
        else:
            folder_path = f"{cgg_path}/{self.__goal_folder_name}"

        if self.__world is not None:
            controller_info = self.specification.get_controller_info(world_ts=self.__world)
        else:
            controller_info = self.specification.get_controller_info()

        a, g, i, o = controller_info.get_strix_inputs()

        try:
            controller_synthesis_input = StringMng.get_controller_synthesis_str(controller_info)

            Store.save_to_file(controller_synthesis_input, "controller_specs.txt", folder_path)

            realized, dot_mealy, time = Controller.generate_controller(a, g, i, o)

            self.__realizable = realized
            self.__time_synthesis = time

            if realized:
                source = Store.generate_eps_from_dot(dot_mealy, "controller", folder_path)
            else:
                source = Store.generate_eps_from_dot(dot_mealy, "controller_inverted", folder_path)

            self.__controller = Controller(source=source)

        except ControllerException as e:
            raise GoalSynthesisFail(self, e)

    @staticmethod
    def pretty_print_goal(goal: Goal, level=0):
        ret = "\t" * level + f"|---GOAL\t {goal.id} {repr(goal.name)}\n"
        if goal.context is not None:
            ret += "\t" * level + f"|\tCONTEXT:\t {str(goal.context)}\n"
        if not goal.specification.assumptions.is_true():
            ret += "\t" * level + "|\t  ASSUMPTIONS:\n"
            ret += "\t" * level + f"|\t  {goal.specification.assumptions.pretty_print(FormulaOutput.DNF)} \n"
        ret += "\t" * level + "|\t  GUARANTEES:\n"
        ret += "\t" * level + f"|\t  {goal.specification.guarantees.pretty_print(FormulaOutput.CNF)} \n"
        if goal.realizable is not None:
            if goal.realizable:
                ret += "\t" * level + f"|\t  REALIZABLE:\tYES\t{goal.time_synthesis} seconds\n"
            else:
                ret += "\t" * level + f"|\t  REALIZABLE:\tNO\n"
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
        new_goal_world = None
        for g in goals:
            set_of_contracts.add(g.specification)
            if g.world is not None:
                if new_goal_world is None:
                    new_goal_world = g.world
                else:
                    if new_goal_world is not g.world:
                        raise GoalException("conjoining goals that have different 'worlds'")

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
                        specification=new_contract,
                        world=new_goal_world)

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

        new_goal_world = None
        for g in goals:
            set_of_contracts.add(g.specification)
            if g.world is not None:
                if new_goal_world is None:
                    new_goal_world = g.world
                else:
                    if new_goal_world is not g.world:
                        raise GoalException("conjoining goals that have different 'worlds'")

        try:
            new_contract = Contract.conjunction(set_of_contracts)

        except InconsistentContracts as e:

            raise GoalAlgebraOperationFail(goals=goals, operation=GoalFailOperations.conjunction, contr_ex=e)

        new_goal = Goal(name=name,
                        description=description,
                        specification=new_contract,
                        world=new_goal_world)

        return new_goal

    @staticmethod
    def disjunction(goals: Set[Goal], name: str = None, description: str = None) -> Goal:
        if name is None:
            names = []
            for goal in goals:
                names.append(goal.name)
            names.sort()
            conj_name = ""
            for name in names:
                conj_name += name + "vv"
            name = conj_name[:-2]

        set_of_contracts = set()

        new_goal_world = None
        for g in goals:
            set_of_contracts.add(g.specification)
            if g.world is not None:
                if new_goal_world is None:
                    new_goal_world = g.world
                else:
                    if new_goal_world is not g.world:
                        raise GoalException("disjoining goals that have different 'worlds'")

        try:
            new_contract = Contract.disjunction(set_of_contracts)

        except InconsistentContracts as e:

            raise GoalAlgebraOperationFail(goals=goals, operation=GoalFailOperations.conjunction, contr_ex=e)

        new_goal = Goal(name=name,
                        description=description,
                        specification=new_contract,
                        world=new_goal_world)

        return new_goal
