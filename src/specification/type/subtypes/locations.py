from __future__ import annotations
from typing import Set

from specification.typeset import Boolean


class ReachLocation(Boolean):

    def __init__(self, name: str, adjacent_to: Set[str] = None):
        super().__init__(name)
        self.kind: str = "location"

        if adjacent_to is not None:
            self.__adjacency_set: Set[str] = adjacent_to

    @property
    def adjacency_set(self) -> Set[str]:
        return self.__adjacency_set
