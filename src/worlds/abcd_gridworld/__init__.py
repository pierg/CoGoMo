
from typeset import Typeset
from worlds import World
from worlds.abcd_gridworld.types.locations import *
from worlds.abcd_gridworld.types.sensors import *


class ABCDGridworld(World):

    def __init__(self):
        self.__typset = Typeset()

        """Sensors"""
        self.__typset |= SeA()
        self.__typset |= SeB()
        self.__typset |= SeC()
        self.__typset |= SeD()

        """Locations"""
        self.__typset |= GoA()
        self.__typset |= GoB()
        self.__typset |= GoC()
        self.__typset |= GoD()

    @property
    def typeset(self) -> Typeset:
        return self.__typset
