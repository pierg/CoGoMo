from __future__ import annotations

from copy import deepcopy
from itertools import combinations

from typing import Set


class Type(object):

    def __init__(self, name: str, kind: str = None):
        """Name of the types"""
        self.__name: str = name

        """Kind of types, needed for the synthesis and to determine if controllable or not"""
        self.__kind: str = kind

        """List of types that can be refined by self (filled when type is part of typeset)"""
        self.__is_refinement_of: Set[Type] = set()

    def __str__(self):
        return type(self).__name__ + "(" + self.name + ")"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def kind(self) -> str:
        return self.__kind

    @kind.setter
    def kind(self, value: str):
        self.__kind = value

    @property
    def is_refinement_of(self) -> Set[Type]:
        return self.__is_refinement_of

    def add_supertype(self, value: Type):
        self.__is_refinement_of.add(value)

    @property
    def controllable(self) -> 'bool':
        if self.kind is not None:
            if self.kind == "characteristics" or \
                    self.kind == "sensor":
                """Not controllable"""
                return False
            if self.kind == "location" or self.kind == "action":
                """Controllable"""
                return True
        else:
            raise Exception("Type does not have a kind")

    @property
    def nusmv_type(self) -> str:
        from .types.basic import Boolean
        if isinstance(self, Boolean):
            return "boolean"
        from .types.basic import BoundedInteger
        if isinstance(self, BoundedInteger):
            return str(self.min) + ".." + str(self.max)

    @property
    def nuxmv_variable(self):
        return self.name + ": " + self.nusmv_type + ";\n"

    def __eq__(self, other):
        return self.name == other.name and \
               self.nusmv_type == other.nusmv_type and \
               type(self).__name__ == type(other).__name__

    def __hash__(self):
        return hash(self.name + self.nusmv_type)


class Typeset(dict):
    """Set of identified -> Types"""

    def __init__(self, types: Set[Type] = None):

        if types is not None:
            for elem in types:
                super(Typeset, self).__setitem__(elem.name, elem)

        for (a, b) in combinations(types, 2):
            if isinstance(a, type(b)):
                a.add_supertype(b)
            # if isinstance(b, type(a)):
            #     b.add_supertype(a)

        super(Typeset, self).__init__()

    def __str__(self):
        ret = ""
        for (key, elem) in self.items():
            ret += key + ":\t" + str(elem)
            getset = elem.is_refinement_of()
            if elem.is_refinement_of() != set():
                ret += " -> " + str(*elem.is_refinement_of) + "\n"
        return ret[:-1]

    def __or__(self, element: Typeset) -> Typeset:
        """ Returns self |= element """
        new_dict = deepcopy(self)
        new_dict.update(element)
        return new_dict

    def __and__(self, element: Typeset) -> Typeset:
        """ Returns self &= element """
        pass

    def __ior__(self, element: Typeset):
        """ Updates self with self |= element """
        self.update(element)
        return self

    def __iand__(self, element: Typeset):
        """ Updates self with self &= element """
        pass

    def __isub__(self, element):
        """ Updates self with self -= element """
        pass

    def __setitem__(self, name, elem):
        super().__setitem__(name, elem)

        for (a, b) in combinations(self.values(), 2):
            if issubclass(a, b):
                a.add_supertype(b)
            if issubclass(b, a):
                b.add_supertype(a)

    def get_nusmv_names(self):
        """Get List[str] for nuxmv"""
        tuple_vars = []
        for k, v in self.items():
            tuple_vars.append(v.name + ": " + v.nusmv_type)
        return tuple_vars

    def get_nusmv_types(self):
        """Get List[str] for nuxmv"""
        tuple_vars = []
        for k, v in self.items():
            tuple_vars.append(v.port_type + ": " + v.nusmv_type)
        return tuple_vars
