



class Type:

    def __init__(self, name: str):
        """Name of the variable"""
        self.__name: str = name

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