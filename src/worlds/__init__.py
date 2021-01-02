from abc import ABC, abstractmethod

from typeset import Typeset


class World(ABC):

    @property
    @abstractmethod
    def typeset(self) -> Typeset:
        pass
