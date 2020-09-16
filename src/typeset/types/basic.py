from __future__ import annotations

from typeset import Type, Typeset
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from formula import LTL


class Boolean(Type):

    def __init__(self, name: str):
        super().__init__(name)

    """Generating Atomic Propositions"""

    def is_true(self):
        from formula import LTL
        return LTL(formula=self.name, variables=Typeset({self}), skip_checks=True)

    def is_false(self):
        from formula import LTL
        return ~ LTL(formula=self.name, variables=Typeset({self}), skip_checks=True)

    def __hash__(self):
        return hash(self.name + self.nusmv_type)

    def __and__(self, other: Union[Boolean, LTL]) -> LTL:
        """self & other
        Returns a new LTL with the conjunction with other"""
        if isinstance(other, Boolean):
            other = other.is_true()

        return self.is_true() & other

    def __or__(self, other: Union[Boolean, LTL]) -> LTL:
        """self | other
        Returns a new LTL with the disjunction with other"""
        if isinstance(other, Boolean):
            other = other.is_true()

        return self.is_true() | other

    def __invert__(self) -> LTL:
        """Returns a new LTL with the negation of self"""

        return ~ self.is_true()

    def __rshift__(self, other: Union[Boolean, LTL]) -> LTL:
        """>>
        Returns a new LTL that is the result of self -> other (implies)"""
        if isinstance(other, Boolean):
            other = other.is_true()

        return self.is_true() >> other

    def __lshift__(self, other: Union[Boolean, LTL]) -> LTL:
        """<<
        Returns a new LTL that is the result of other -> self (implies)"""
        if isinstance(other, Boolean):
            other = other.is_true()

        return other >> self.is_true()


class BoundedInteger(Type):

    def __init__(self, name: str, min_value: int, max_value: int):

        self.min = min_value
        self.max = max_value

        super().__init__(name)

    @property
    def min(self) -> int:
        return self.__min

    @min.setter
    def min(self, value: int):
        self.__min = value

    @property
    def max(self) -> int:
        return self.__max

    @max.setter
    def max(self, value: int):
        self.__max = value

    def __hash__(self):
        return hash(self.name + self.nusmv_type)

    """Generating Atomic Propositions"""

    def __eq__(self, other: Union[int, BoundedInteger]) -> LTL:
        from formula import LTL
        if isinstance(other, int):
            if other > self.max or other < self.min:
                raise AttributeError
            return LTL(formula=self.name + " = " + str(other), variables=Typeset({self}))
        elif isinstance(other, BoundedInteger):
            return LTL(formula=self.name + " = " + other.name, variables=Typeset({self, other}))
        else:
            raise AttributeError

    def __lt__(self, other: Union[int, BoundedInteger]) -> LTL:
        from formula import LTL
        if isinstance(other, int):
            if other > self.max or other < self.min:
                raise AttributeError
            return LTL(formula=self.name + " < " + str(other), variables=Typeset({self}))
        elif isinstance(other, BoundedInteger):
            return LTL(formula=self.name + " < " + other.name, variables=Typeset({self, other}))
        else:
            raise AttributeError

    def __le__(self, other: Union[int, BoundedInteger]) -> LTL:
        from formula import LTL
        if isinstance(other, int):
            if other > self.max or other < self.min:
                raise AttributeError
            return LTL(formula=self.name + " <= " + str(other), variables=Typeset({self}))
        elif isinstance(other, BoundedInteger):
            return LTL(formula=self.name + " <= " + other.name, variables=Typeset({self, other}))
        else:
            raise AttributeError

    def __gt__(self, other: Union[int, BoundedInteger]) -> LTL:
        from formula import LTL
        if isinstance(other, int):
            if other > self.max or other < self.min:
                raise AttributeError
            return LTL(formula=self.name + " > " + str(other), variables=Typeset({self}))
        elif isinstance(other, BoundedInteger):
            return LTL(formula=self.name + " > " + other.name, variables=Typeset({self, other}))
        else:
            raise AttributeError

    def __ge__(self, other: Union[int, BoundedInteger]) -> LTL:
        from formula import LTL
        if isinstance(other, int):
            if other > self.max or other < self.min:
                raise AttributeError
            return LTL(formula=self.name + " >= " + str(other), variables=Typeset({self}))
        elif isinstance(other, BoundedInteger):
            return LTL(formula=self.name + " >= " + other.name, variables=Typeset({self, other}))
        else:
            raise AttributeError
