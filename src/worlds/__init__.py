from typing import Set

from type import Types
from typeset import Typeset


class World:

    def __init__(self, types: Set[Types]):
        self.__typeset = Typeset(types)

    @property
    def typeset(self) -> Typeset:
        return self.__typeset

