from __future__ import annotations

from copy import copy
from itertools import combinations
from typing import Set, Dict, Union, TypeVar

from type import Types

AllTypes = TypeVar('AllTypes', bound=Types)


class Typeset(dict):
    """Set of identifier -> AllTypes"""

    def __init__(self, types: Set[AllTypes] = None):

        """Indicates the supertypes relationships for each type in the typeset"""
        self.__super_types: Dict[AllTypes, Set[AllTypes]] = {}

        """Indicates the mutex relationships for the type in the typeset"""
        self.__mutex_types: Set[Set[AllTypes]] = set()

        """Indicates the adjacency relationships for the type in the typeset"""
        self.__adjacent_types: Dict[AllTypes, Set[AllTypes]] = dict()

        if types is not None:
            self.add_elements(types)
        else:
            super(Typeset, self).__init__()

    def __str__(self):
        ret = ""
        for (key, elem) in self.items():
            ret += f"{key}:\t{elem.name}"
            if elem in self.super_types:
                ret += " -> "
                for supertypes in self.super_types[elem]:
                    ret += supertypes.name
            ret += "\n"
        return ret[:-1]

    def __or__(self, element: Union[Typeset, AllTypes]) -> Typeset:
        """ Returns self |= element """
        if isinstance(element, Types):
            element = Typeset({element})
        """Shallow copy"""
        new_dict = copy(self)
        new_dict |= element
        return new_dict

    def __and__(self, element: Typeset) -> Typeset:
        """ Returns self &= element """
        pass

    def __ior__(self, element: Union[Typeset, AllTypes]):
        """ Updates self with self |= element """
        if isinstance(element, Types):
            element = Typeset({element})
        for key, value in element.items():
            if key in self:
                if value is not self[key]:
                    raise Exception("Type Mismatch")
            if key not in self:
                self.add_elements({value})
        return self

    def __iand__(self, element: Typeset):
        """ Updates self with self &= element """
        pass

    def __isub__(self, element):
        """ Updates self with self -= element """
        pass

    def add_elements(self, types: Set[AllTypes]):
        if types is not None:
            for elem in types:
                super(Typeset, self).__setitem__(elem.name, elem)

        self.update_subtypes()
        self.update_mutextypes()
        self.update_adjacenttypes()

    def update_subtypes(self):
        if len(self.values()) > 1:
            for (a, b) in combinations(self.values(), 2):
                if isinstance(a, type(b)):
                    if a in self.__super_types:
                        self.__super_types[a].add(b)
                    else:
                        self.__super_types[a] = {b}
                if isinstance(b, type(a)):
                    if b in self.__super_types:
                        self.__super_types[b].add(a)
                    else:
                        self.__super_types[b] = {a}

    def update_mutextypes(self):
        if len(self.values()) > 1:
            mutex_classes_checked = set()
            self.__mutex_types = set()
            for variable in self.values():
                base_classes = variable.__class__.__bases__
                mutex = False
                mutex_class = None
                for base in base_classes:
                    if hasattr(base, "mutex") and base.mutex:
                        mutex = True
                        mutex_class = base
                if mutex and mutex_class not in mutex_classes_checked:
                    mutex_types = set()
                    for variable in self.values():
                        if mutex_class in variable.__class__.__bases__:
                            mutex_types.add(variable)
                    self.__mutex_types.add(frozenset(mutex_types))
                    mutex_classes_checked.add(mutex_class)

    def update_adjacenttypes(self):
        if len(self.values()) > 1:
            self.__adjacent_types = dict()
            for variable in self.values():
                if hasattr(variable, "adjacency_set"):
                    for adjacent_class in variable.adjacency_set:
                        for variable_candidate in self.values():
                            if variable_candidate.__class__.__name__ == adjacent_class:
                                if variable in self.__adjacent_types:
                                    self.__adjacent_types[variable].add(variable_candidate)
                                else:
                                    self.__adjacent_types[variable] = {variable_candidate}

    def __setitem__(self, name, elem):
        self.add_elements({elem})

    @property
    def super_types(self) -> Dict[AllTypes, Set[AllTypes]]:
        return self.__super_types

    @property
    def mutex_types(self) -> Set[Set[AllTypes]]:
        return self.__mutex_types

    @property
    def adjacent_types(self) -> Dict[AllTypes, Set[AllTypes]]:
        return self.__adjacent_types
