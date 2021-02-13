from worlds import World
from worlds.illustrative_example.types.locations import *
from worlds.illustrative_example.types.sensors import *
from worlds.illustrative_example.types.actions import *
from worlds.illustrative_example.types.context import *


class IllustrativeExample(World):

    def __init__(self):
        super().__init__({
            Person(),
            A1(),
            A2(),
            B1(),
            B2(),
            Z(),
            Day(),
            Night(),
            Greet()
        })
