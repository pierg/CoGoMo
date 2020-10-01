from typeset.types.basic import MutexType
from typeset.types.subtypes.sensors import IntegerSensor, BooleanSensor


class MutexSensor(MutexType):
    pass


class S1(BooleanSensor):

    def __init__(self, name: str = "s1"):
        super().__init__(name)


class S2(BooleanSensor):

    def __init__(self, name: str = "s2"):
        super().__init__(name)


class S3(BooleanSensor):

    def __init__(self, name: str = "s3"):
        super().__init__(name)
