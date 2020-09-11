from enum import Enum
import hashlib
import string
from copy import deepcopy
from random import random
from typing import List, Union, Dict
from specification import Specification
from typescogomo.formula import LTL


class Link(Enum):
    REFINEMENT = 0
    COMPOSITION = 1
    CONJUNCTION = 2


class Goal(object):

    def __init__(self,
                 name: str = None,
                 description: str = None,
                 specification: Specification = None,
                 context: Union[LTL, List[LTL]] = None):
        """Parent goal"""
        self.__connected_to = None

        """Properties defined on first instantiation"""
        self.name: str = name
        self.description: str = description
        self.specification: Specification = specification
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

    @property
    def id(self):
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if value is None:
            self.__name: str = ""

            """5 character ID generated from a random string"""
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            self.__id = hashlib.sha1(random_string.encode("UTF-8")).hexdigest()[:5]
        else:
            self.__name: str = value

            """5 character ID generated from the name"""
            self.__id: str = hashlib.sha1(value.encode("UTF-8")).hexdigest()[:5]

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
                list_of_goals = []
                for ctx in value:
                    list_of_goals.append(Goal(
                        name=self.name + " & " + ctx.formula,
                        description=self.description + " in " + ctx.formula,
                        specification=deepcopy(self.specification),
                        context=ctx
                    ))
                from goals.operations import conjunction
                conjunction(list_of_goals, connect_to=self)
            else:
                """Add context to guarantees as G(context -> guarantee)"""
                self.specification.context = value

    @property
    def parents(self) -> Dict['Goal', Link]:
        return self.__parents

    @parents.setter
    def parents(self, value: Dict['Goal', Link]):
        self.__parents = value

    @property
    def children(self) -> Dict['Goal', Link]:
        return self.__children

    @children.setter
    def children(self, goals: Dict['Goal', Link]):
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

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
