from type.subtypes.locations import *

""""
    A1      A2   
        Z
    B1      B2
"""


class A1(ReachLocation):

    def __init__(self, name: str = "a1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"A2", "Z"}


class A2(ReachLocation):

    def __init__(self, name: str = "a2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"A1", "A"}


class B1(ReachLocation):

    def __init__(self, name: str = "b1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"B2", "Z"}


class B2(ReachLocation):

    def __init__(self, name: str = "b2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"B1", "Z"}


class Z(ReachLocation):

    def __init__(self, name: str = "z"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"A1", "A2", "B1", "B2"}
