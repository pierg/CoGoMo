from __future__ import annotations
from enum import Enum
from copy import deepcopy
from typing import Union, Dict

from contract import Contract
from formula import LTL
from tools.strings_generation import get_name_and_id
from contract.specification import Specification
from typing import TypeVar, List
LTL_types = TypeVar('LTL_types', bound=LTL)

class Link(Enum):
    REFINEMENT = 0
    COMPOSITION = 1
    CONJUNCTION = 2


class Goal(object):

    def __init__(self,
                 name: str = None,
                 description: str = None,
                 specification: Union[Contract, LTL_types] = None,
                 context: Union[LTL, List[LTL]] = None):
        """Parent goal"""
        self.__connected_to = None

        """Properties defined on first instantiation"""
        self.name: str = name
        self.description: str = description
        self.specification: Specification = Specification(specification)
        self.context: LTL = context

        """Other properties"""
        self.parents = None
        self.children = None

        """Read only properties"""
        self.__realizable = None
        self.__controller = None
        self.__time_synthesis = None

    """Imported methods"""
    from ._graph import get_parent_link, get_children_link, get_all_leaf_nodes, get_goals_by_name, get_all_nodes, \
        get_goal_by_id
    from ._printing import __str__, pretty_print_cgt_summary, print_cgt_CROME, print_cgt_detailed, print_cgt_summary
    from ._copying import __copy__, __deepcopy__

    @property
    def id(self):
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name, self.__id = get_name_and_id(value)

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
    def specification(self) -> Specification:
        return self.__specification

    @specification.setter
    def specification(self, value: Specification):
        self.__specification: Specification = value

    @property
    def context(self) -> LTL:
        return self.specification.context

    @context.setter
    def context(self, value: Union[LTL, List[LTL]]):
        if value is not None:
            if isinstance(value, list):
                """If we have a list of context we connect the current goal to a conjunction of goals, each goal is 
                instantiated in a context in the list """
                goals = []
                for ctx in value:
                    goals.append(Goal(
                        name=self.name + " & " + ctx.formula,
                        description=self.description + " in " + ctx.formula,
                        specification=deepcopy(self.specification),
                        context=ctx
                    ))
                from goal.operations import conjunction
                conjunction(goals)
            else:
                """Add context to guarantees as G(context -> guarantee)"""
                self.specification.context = value

    @property
    def parents(self) -> Dict[Goal, Link]:
        return self.__parents

    @parents.setter
    def parents(self, value: Dict[Goal, Link]):
        self.__parents = value

    @property
    def children(self) -> Dict[Goal, Link]:
        return self.__children

    @children.setter
    def children(self, goals: Dict[Goal, Link]):
        self.__children = goals
        if goals is not None:
            for goal in goals:
                goal.parent = self

    @property
    def realizable(self) -> bool:
        return self.__realizable

    @property
    def controller(self) -> str:
        return self.__controller

    @property
    def time_synthesis(self) -> int:
        return round(self.__time_synthesis, 2)
