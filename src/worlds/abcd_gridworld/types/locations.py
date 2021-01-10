from type.subtypes.locations import *

""""
    A   B   
    C   D
"""

class GoA(ReachLocation):

    def __init__(self, name: str = "a"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoC", "GoB"}

    @property
    def mutex_group(self) -> str:
        return "locations"


class GoB(ReachLocation):

    def __init__(self, name: str = "b"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoD", "GoA"}

    @property
    def mutex_group(self) -> str:
        return "locations"


class GoC(ReachLocation):

    def __init__(self, name: str = "c"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoA", "GoD"}

    @property
    def mutex_group(self) -> str:
        return "locations"


class GoD(ReachLocation):

    def __init__(self, name: str = "d"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoB", "GoC"}

    @property
    def mutex_group(self) -> str:
        return "locations"

