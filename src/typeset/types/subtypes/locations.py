from typeset.types.basic import Boolean


class ReachLocation(Boolean):

    def __init__(self, name: str):
        super().__init__(name)
        self.kind = "location"


class MutexReachLocation(Boolean):

    def __init__(self, name: str):
        super().__init__(name)
        self.kind = "location"
