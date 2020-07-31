from typing import Set
from helper.tools import extract_terms


class Type(object):
    """Base Type Class, a Type is a variable with a name, basic_type for nuxmv (e.g. boolean),
    and variable_type: used for example when a component requires multiple variables of the same type
    but having different names. If the port_type is not specified then it's the same as the name of the variable"""

    def __init__(self, name: str, basic_type: str, controllable=False, port_type: str = None):
        """Name of the variable"""
        self.name = name

        """Controllable, for the synthesis"""
        self.__controllable: bool = controllable

        """Basic type, for nuxmv """
        self.basic_type = basic_type

        """Type of the variable, if it is not specified then it's the same as the name"""
        self.port_type = port_type if port_type is not None else name

    def __str__(self):
        return self.name

    @property
    def controllable(self) -> 'bool':
        return self.__controllable

    @controllable.setter
    def controllable(self, value: bool):
        self.__controllable = value


    def nuxmv_variable(self):
        return self.name + ": " + self.basic_type + ";\n"

    def __eq__(self, other):
        return self.name == other.name and self.basic_type == other.basic_type and self.port_type == other.port_type

    def __hash__(self):
        return hash(self.name + self.basic_type)


class Boolean(Type):

    def __init__(self, name: str, port_type: str = None):
        super().__init__(name, "boolean", port_type=port_type)


class Integer(Type):

    def __init__(self, name: str, min: int, max: int, port_type: str = None):
        super().__init__(name, str(min) + ".." + str(max), port_type=port_type)


class BoundedInt(Integer):

    def __init__(self, name: str, port_type: str = None):
        super().__init__(name, min=-100, max=100, port_type=port_type)


class BoundedNat(Integer):

    def __init__(self, name: str, port_type: str = None):
        super().__init__(name, min=0, max=100, port_type=port_type)


class Variables(set):
    """Redefining Variables as a set of Types"""

    def add(self, other):
        if not isinstance(other, Type):
            raise AttributeError
        else:
            super().add(other)

    def __or__(self, other):
        return Variables(super().__or__(other))

    def get_nusmv_names(self):
        """Get List[str] for nuxmv"""
        tuple_vars = []
        for v in self:
            tuple_vars.append(v.name + ": " + v.basic_type)
        return tuple_vars

    def get_nusmv_types(self):
        """Get List[str] for nuxmv"""
        tuple_vars = []
        for v in self:
            tuple_vars.append(v.port_type + ": " + v.basic_type)
        return tuple_vars


def extract_variable(formula: str) -> 'Variables':
    if formula == "TRUE" or formula == "FALSE":
        return Variables()

    var_names = extract_terms(formula)

    vars: Set[Type] = set()

    try:
        int(var_names[1])
        vars.add(BoundedNat(var_names[0]))
    except:
        for var_name in var_names:
            vars.add(Boolean(var_name))

    return Variables(vars)
