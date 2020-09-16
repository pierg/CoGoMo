from typing import Dict

from tools.dict_manipulation import flat_dict
from typeset import Typeset


class World(object):
    """World models containing environment and system rules"""

    def __init__(self,
                 types: Typeset,
                 rules: Dict):
        self.types = types
        self.rules = rules

    @property
    def types(self) -> Dict:
        return self.__types

    @types.setter
    def types(self, value: Dict):
        self.__types = value

    @property
    def environment_rules(self) -> Dict:
        return self.__environment_rules

    @environment_rules.setter
    def environment_rules(self, value: Dict):
        self.__environment_rules = flat_dict(value)

    @property
    def system_rules(self) -> Dict:
        return self.__system_rules

    @system_rules.setter
    def system_rules(self, value: Dict):
        self.__system_rules = flat_dict(value)
