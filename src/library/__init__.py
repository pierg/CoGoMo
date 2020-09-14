from __future__ import annotations
from tools.strings_generation import get_name_and_id
from goal import Goal
from contract.specification import Specification


class Library(set):
    """Library is a set of Goal elements"""

    def __init__(self,
                 name: str = None,
                 description: str = None):
        super().__init__()

        self.name = name
        self.description = description

    @property
    def id(self):
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name, self.__id = get_name_and_id(value)

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        if value is None:
            self.__description: str = ""
        else:
            self.__description: str = value

    def add(self, other: Goal):
        if not isinstance(other, Goal):
            raise AttributeError
        else:
            super().add(other)


if __name__ == '__main__':
    goal = Goal(
        name="goal_1",
        specification=Specification()
    )
    l1 = Library(name="l1", description="ibrary")


    print(l1)
    print(l1 | l2)

    l3 = Library()
    l3 |= l1
    print(l3)
