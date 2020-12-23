from typing import Set

from specification.atom.pattern.robotics.coremovement.surveillance import OrderedPatrolling
from type import MutexType
from type.subtypes.locations import ReachLocation

"""We define 2 mutex locations: living_room and bedroom adjacent to each other"""


class MutexRegion(MutexType):
    pass


class GoLiving(ReachLocation, MutexRegion):

    def __init__(self, name: str = "living_room"):
        super().__init__(name)


    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoBedroom"}


class GoBedroom(ReachLocation, MutexRegion):

    def __init__(self, name: str = "bedroom"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoLiving"}


"""We define 3 mutex locations: a, b, c, d in a grid as: |a|b|c|d|, and
 where locations a,b -> living_room and b,c -> bedroom"""


class MutexLocation(MutexType):
    pass


class GoA(GoLiving, MutexLocation):

    def __init__(self, name: str = "a"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoB"}


class GoB(GoLiving, MutexLocation):

    def __init__(self, name: str = "b"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoA", "GoC"}


class GoC(GoBedroom, MutexLocation):

    def __init__(self, name: str = "c"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoB", "GoD"}


class GoD(GoBedroom, MutexLocation):

    def __init__(self, name: str = "d"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoC"}


"""Variable instantiation"""
living_room = GoLiving()
bedroom = GoBedroom()
a = GoA()
b = GoB()
c = GoC()
d = GoD()

"""Let us create some specifications"""
patrol_ab = OrderedPatrolling([a, b])
patrol_living_room = OrderedPatrolling([living_room])
print(patrol_ab >= patrol_living_room)
