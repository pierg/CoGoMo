from __future__ import annotations

from typing import Dict, List

from tools.strings_generation import get_name_and_id
from goal import Goal


class Library(set):
    """Library is a set of Goal elements"""

    def __init__(self,
                 name: str = None,
                 description: str = None,
                 environment_rules: Dict = None,
                 system_rules: Dict = None,
                 goals: List[Goal] = None):
        super().__init__()

        self.name = name
        self.description = description
        self.environment_rules = environment_rules
        self.system_rules = system_rules
        for goal in goals:
            self.add(goal)

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

    @property
    def environment_rules(self) -> Dict:
        return self.__environment_rules

    @environment_rules.setter
    def environment_rules(self, value: Dict):
        self.__environment_rules: Dict = value

    @property
    def system_rules(self) -> Dict:
        return self.__system_rules

    @system_rules.setter
    def system_rules(self, value: Dict):
        self.__system_rules: Dict = value

    def add(self, other: Goal):
        if not isinstance(other, Goal):
            raise AttributeError
        else:
            super().add(other)

