from type import MutexType
from type.subtypes.locations import *


class MutexLocation(MutexType):
    pass


class GoA(ReachLocation, MutexLocation):

    def __init__(self, name: str = "go_a"):
        super().__init__(name, adjacent_to={"GoX", "GoB"})


class GoB(ReachLocation, MutexLocation):

    def __init__(self, name: str = "go_b"):
        super().__init__(name, adjacent_to={"GoX", "GoA"})


class GoC(ReachLocation, MutexLocation):

    def __init__(self, name: str = "go_c"):
        super().__init__(name, adjacent_to={"GoX", "GoD"})


class GoD(ReachLocation, MutexLocation):

    def __init__(self, name: str = "go_d"):
        super().__init__(name, adjacent_to={"GoX", "GoC"})


class GoX(ReachLocation, MutexLocation):

    def __init__(self, name: str = "go_x"):
        super().__init__(name, adjacent_to={"GoA", "GoB", "GoC", "GoD"})
