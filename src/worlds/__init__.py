from abc import ABC

from typeset import Typeset


class World(ABC):

    @property
    def typeset(self) -> (str, Typeset):
        pass
