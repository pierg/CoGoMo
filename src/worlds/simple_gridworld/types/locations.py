from type.subtypes.locations import *



class GoA(ReachLocation):

    def __init__(self, name: str = "a"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoX", "GoB"}

    @property
    def mutex_group(self) -> str:
        return "locations"


class GoB(ReachLocation):

    def __init__(self, name: str = "b"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoX", "GoA"}

    @property
    def mutex_group(self) -> str:
        return "locations"


class GoC(ReachLocation):

    def __init__(self, name: str = "c"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoX", "GoD"}

    @property
    def mutex_group(self) -> str:
        return "locations"


class GoD(ReachLocation):

    def __init__(self, name: str = "d"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoX", "GoC"}

    @property
    def mutex_group(self) -> str:
        return "locations"


class GoX(ReachLocation):

    def __init__(self, name: str = "x"):
        super().__init__(name)

    @property
    def adjacency_set(self) -> Set[str]:
        return {"GoA", "GoB", "GoC", "GoD"}

    @property
    def mutex_group(self) -> str:
        return "locations"

