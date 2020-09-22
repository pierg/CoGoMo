from typing import Set
from tools.strings_manipulation import extract_terms


class Type(object):
    """Base Type Class, a Type is a types with a name, basic_type for nuxmv (e.g. boolean),
    and variable_type: used for example when a component requires multiple variables of the same type
    but having different names. If the port_type is not specified then it's the same as the name of the types"""

    def __init__(self, name: str, basic_type: str, kind: str = None, port_type: str = None):
        """Name of the types"""
        self.__name: str = name

        """Kind of types, needed for the synthesis and to determine if controllable or not"""
        self.__kind: str = kind

        """Basic type, for nuxmv """
        self.__basic_type: str = basic_type

        """Type of the types, if it is not specified then it's the same as the name"""
        self.__port_type: str = port_type if port_type is not None else name

    def __str__(self):
        return self.name

    @property
    def name(self) -> 'str':
        return self.__name

    @property
    def kind(self) -> 'str':
        return self.__kind

    @kind.setter
    def kind(self, value: str):
        self.__kind = value

    @property
    def basic_type(self) -> 'str':
        return self.__basic_type

    @property
    def port_type(self) -> 'str':
        return self.__port_type

    def controllable(self) -> 'bool':
        if self.kind is not None:

            if self.kind == "ctx_location" or \
                    self.kind == "ctx_time" or \
                    self.kind == "ctx_identity" or \
                    self.kind == "sensor":
                """Not controllable"""
                return False

            if self.kind == "location" or self.kind == "action":
                """Controllable"""
                return True

        else:
            raise Exception("Type does not have a kind")


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

    def __or__(self, other) -> 'Variables':
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
