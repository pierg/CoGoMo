from __future__ import annotations

from specification.type import Type


class Atom:

    def __init__(self,
                 atom_type: Type = None,
                 expression: str = None):

        self.type: Type = atom_type
        self.expression = expression

    @property
    def type(self) -> Type:
        return self.__type

    @type.setter
    def type(self, value: Type):
        if isinstance(value, Type):
            self.__type: Type = value
        else:
            raise AttributeError

    @property
    def expression(self) -> str:
        return self.__expression

    @expression.setter
    def expression(self, value: str):
        if isinstance(value, str):
            self.__expression: str = value
        else:
            raise AttributeError
