from typing import Set

from type import Boolean, TypeKinds


class ReachLocation(Boolean):

    def __init__(self, name: str, adjacent_to: Set[str] = None):
        """adjacent_to is a set of strings where each string is the name of the class self is adjacent to"""

        super().__init__(name)
        if adjacent_to is not None:
            self.__adjacency_set: Set[str] = adjacent_to

    @property
    def kind(self):
        return TypeKinds.LOCATION

    @property
    def adjacency_set(self) -> Set[str]:
        return self.__adjacency_set
