from type import MutexType
from type.subtypes.sensors import *


class MutexSensor(MutexType):
    pass


class SeA(BooleanSensor, MutexSensor):

    def __init__(self, name: str = "se_a"):
        super().__init__(name)


class SeB(BooleanSensor, MutexSensor):

    def __init__(self, name: str = "se_b"):
        super().__init__(name)


class SeC(BooleanSensor, MutexSensor):

    def __init__(self, name: str = "se_c"):
        super().__init__(name)


class SeD(BooleanSensor, MutexSensor):

    def __init__(self, name: str = "se_d"):
        super().__init__(name)


class SeX(BooleanSensor, MutexSensor):

    def __init__(self, name: str = "se_x"):
        super().__init__(name)
