from typeset.types.subtypes.locations import MutexReachLocation


class GoCorridor(MutexReachLocation):

    def __init__(self, name: str = "go_corridor"):
        super().__init__(name)


class GoB(GoCorridor):

    def __init__(self, name: str = "go_b"):
        super().__init__(name)


class GoC(GoCorridor):

    def __init__(self, name: str = "go_c"):
        super().__init__(name)


class GoD(GoCorridor):

    def __init__(self, name: str = "go_d"):
        super().__init__(name)


class GoE(GoCorridor):

    def __init__(self, name: str = "go_e"):
        super().__init__(name)



class GoPharmacy(MutexReachLocation):

    def __init__(self, name: str = "go_corridor"):
        super().__init__(name)


class GoF(ReachLocation):

    def __init__(self, name: str = "go_f"):
        super().__init__(name)
