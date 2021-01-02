from typing import Dict

from specification.atom import Atom
from typeset import Typeset
from worlds import World
from worlds.simple_gridworld.types.locations import *
from worlds.simple_gridworld.types.sensors import *


class SimpleGridWorld(World):

    def __init__(self):
        self.__typset = Typeset()

        """Sensors"""
        self.__typset |= SeA()
        self.__typset |= SeB()
        self.__typset |= SeC()
        self.__typset |= SeD()
        self.__typset |= SeX()

        """Locations"""
        self.__typset |= GoA()
        self.__typset |= GoB()
        self.__typset |= GoC()
        self.__typset |= GoD()
        self.__typset |= GoX()

    @property
    def typeset(self) -> Typeset:
        return self.__typset
