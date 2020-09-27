from __future__ import annotations
from enum import Enum
from copy import deepcopy
from typing import Union, Dict, Set

from contract import Contract
from formula import LTL
from tools.strings_generation import get_name_and_id
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

        """Graph properties"""
        self.__parents = {}
        self.__children = {}

        """Read only properties"""
        self.__realizable = None
        self.__controller = None
        self.__time_synthesis = None

        """Properties defined on first instantiation"""
        self.name: str = name
        self.description: str = description
        self.specification: Contract = specification
        self.context: LTL = context

    """Imported methods"""
    from ._graph import get_parent_link, get_children_link, get_all_leaf_nodes, get_goals_by_name, get_all_nodes, \
        get_goal_by_id
    from ._printing import __str__, pretty_print_cgt_summary, print_cgt_CROME, print_cgt_detailed, print_cgt_summary
    from ._copying import __copy__, __deepcopy__, __hash__
    from ._operators import __le__, refine_by

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
    def specification(self) -> Contract:
        return self.__specification

    @specification.setter
    def specification(self, value: Union[Contract, LTL_types]):
        if isinstance(value, Contract):
            self.__specification: Contract = value
        elif isinstance(value, LTL):
            self.__specification: Contract = Contract(guarantees=value)

    @property
    def context(self) -> LTL:
        return self.specification.context

    @context.setter
    def context(self, value: Union[LTL, List[LTL]]):
        if value is not None:
            if isinstance(value, list):
                """If we have a list of context we connect the current goal to a conjunction of goals, each goal is 
                instantiated in a context in the list """
                goals = set()
                for ctx in value:
                    goals.add(Goal(
                        name=self.name + " & " + ctx.formula(),
                        description=self.description + " in " + ctx.formula(),
                        specification=deepcopy(self.specification),
                        context=ctx
                    ))
                from goal.operations import conjunction
                new_goal = conjunction(goals)
                self.update_with(new_goal)
            else:
                """Add context to guarantees as G(context -> guarantee)"""
                self.specification.context = value

    @property
    def parents(self) -> Dict[Link, Set[Goal]]:
        return self.__parents

    @property
    def children(self) -> Dict[Link, Set[Goal]]:
        return self.__children

    def add_parents(self, link: Link, goals: Set[Goal]):
        if link in self.__parents.keys():
            self.__parents[link] |= goals
        else:
            self.__parents[link] = goals

    def add_children(self, link: Link, goals: Set[Goal]):
        if link == Link.COMPOSITION or link == Link.CONJUNCTION:
            if link in self.__children.keys():
                raise Exception("A composition/conjunction children link already exists!")
            self.__children[link] = goals
        else:
            if link in self.__children.keys():
                self.__children[link] |= goals
            else:
                self.__children[link] = goals
        for goal in self.__children[link]:
            goal.add_parents(link=link, goals={self})

    @property
    def realizable(self) -> bool:
        return self.__realizable

    @property
    def controller(self) -> str:
        return self.__controller

    @property
    def time_synthesis(self) -> int:
        return round(self.__time_synthesis, 2)

    def consolidate_bottom_up(self: Goal):
        """It recursivly re-perfom composition and conjunction and refinement operations up to the rood node"""

        from .operations import conjunction, composition
        if len(self.parents) > 0:
            for link_1, parents in self.parents.items():
                for parent in parents:
                    for link_2, children in parent.children:
                        if link_2 == Link.CONJUNCTION:
                            new_goal = conjunction(children)
                            parent.update_with(new_goal, consolidate=False)

                        if link_2 == Link.COMPOSITION:
                            new_goal = composition(children)
                            parent.update_with(new_goal, consolidate=False)

                        if link_2 == Link.REFINEMENT:
                            parent.refine_by(children, consolidate=False)
                    parent.consolidate_bottom_up()
        else:
            return

    def update_with(self: Goal, other: Goal, consolidate=True):
        """Update the current node of the CGT with a new goal that has not parent"""

        if len(other.parents) > 0:
            raise Exception("Cannot update with goal belonging to other CGT")

        """Updating fields"""
        self.name = other.name
        self.description = other.description
        self.specification = other.specification
        for link, children in other.children.items():
            self.add_children(link, children)

        if consolidate:
            self.consolidate_bottom_up()
