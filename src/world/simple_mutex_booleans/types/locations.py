from typeset.types.basic import MutexType
from typeset.types.subtypes.locations import ReachLocation


class MutexLocations(MutexType):
    pass


class L1(ReachLocation, MutexLocations):

    def __init__(self, name: str = "l1"):
        super().__init__(name)


class L2(ReachLocation, MutexLocations):

    def __init__(self, name: str = "l2"):
        super().__init__(name)


class L3(ReachLocation, MutexLocations):

    def __init__(self, name: str = "l3"):
        super().__init__(name)

