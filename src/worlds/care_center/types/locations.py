from type import MutexType
from type.subtypes.locations import *


class MutexLocationsA(MutexType):
    pass


class GoCareCenter(ReachLocation):

    def __init__(self, name: str = "go_care_center"):
        super().__init__(name)


class GoCorridor(GoCareCenter, MutexLocationsA):

    def __init__(self, name: str = "go_corridor"):
        super().__init__(name)


class GoPharmacy(GoCareCenter, MutexLocationsA):

    def __init__(self, name: str = "go_pharmacy"):
        super().__init__(name)


class GoEntrance(GoCareCenter, MutexLocationsA):

    def __init__(self, name: str = "go_entrance"):
        super().__init__(name)


class GoMedicalRoom(GoCareCenter, MutexLocationsA):

    def __init__(self, name: str = "go_medical_room"):
        super().__init__(name)


class GoWaitingRoom(GoCareCenter, MutexLocationsA):

    def __init__(self, name: str = "go_waiting_room"):
        super().__init__(name)


class MutexLocationsB(MutexType):
    pass


class GoB(GoCorridor, MutexLocationsB):

    def __init__(self, name: str = "go_b"):
        super().__init__(name)


class GoC(GoCorridor, MutexLocationsB):

    def __init__(self, name: str = "go_c"):
        super().__init__(name)


class GoE(GoCorridor, MutexLocationsB):

    def __init__(self, name: str = "go_e"):
        super().__init__(name)


class GoF(GoCorridor, MutexLocationsB):

    def __init__(self, name: str = "go_f"):
        super().__init__(name)


class GoCommon(GoWaitingRoom, MutexLocationsB):

    def __init__(self, name: str = "go_common"):
        super().__init__(name)


class GoIsolation(GoWaitingRoom, MutexLocationsB):

    def __init__(self, name: str = "go_isolation"):
        super().__init__(name)


class GoA(GoEntrance, MutexLocationsB):

    def __init__(self, name: str = "go_a"):
        super().__init__(name)


class GoD(GoPharmacy, MutexLocationsB):

    def __init__(self, name: str = "go_d"):
        super().__init__(name)


class GoG(GoMedicalRoom, MutexLocationsB):

    def __init__(self, name: str = "go_g"):
        super().__init__(name)


class GoCharging(ReachLocation, MutexLocationsB):

    def __init__(self, name: str = "go_charging"):
        super().__init__(name)
