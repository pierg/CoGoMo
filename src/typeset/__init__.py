from __future__ import annotations

from copy import deepcopy, copy
from itertools import combinations

from typing import Set, Union, Dict


class Type(object):

    def __init__(self, name: str, kind: str = None):
        """Name of the types"""
        self.__name: str = name

        """Kind of types, needed for the synthesis and to determine if controllable or not"""
        self.__kind: str = kind

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

        """Indicates the supertypes relationships for each type in the typeset"""
        self.__supertypes: Dict[Type, Set[Type]] = {}

        if types is not None:
            self.add_elements(types)
        else:
            super(Typeset, self).__init__()

    def __str__(self):
        ret = ""
        for (key, elem) in self.items():
            ret += key + ":\t" + str(elem)
            if elem in self.supertypes:
                ret += " -> "
                for supertypes in self.supertypes[elem]:
                    ret += supertypes.name
            ret += "\n"
        return ret[:-1]

    def __or__(self, element: Union[Typeset, Type]) -> Typeset:
        """ Returns self |= element """
        if isinstance(element, Type):
            element = Typeset({element})
        """Shallow copy"""
        new_dict = copy(self)
        new_dict |= element
        return new_dict

    def __and__(self, element: Typeset) -> Typeset:
        """ Returns self &= element """
        pass

    def __ior__(self, typeset: Typeset):
        """ Updates self with self |= element """
        for key, value in typeset.items():
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


    def add_elements(self, types: Set[Type]):
        if types is not None:
            for elem in types:
                super(Typeset, self).__setitem__(elem.name, elem)

        self.update_subtypes()

    def update_subtypes(self):
        if len(self.values()) > 1:
            for (a, b) in combinations(self.values(), 2):
                if isinstance(a, type(b)):
                    if a in self.__supertypes:
                        self.__supertypes[a].add(b)
                    else:
                        self.__supertypes[a] = {b}
                if isinstance(b, type(a)):
                    if b in self.__supertypes:
                        self.__supertypes[b].add(a)
                    else:
                        self.__supertypes[b] = {a}

    def __setitem__(self, name, elem):
        self.add_elements({elem})

    @property
    def supertypes(self) -> Dict[Type, Set[Type]]:
        return self.__supertypes

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
