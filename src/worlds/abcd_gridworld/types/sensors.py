from type.subtypes.sensors import *


class SeA(BooleanSensor):

    def __init__(self, name: str = "se_a"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "sensor_locations"


class SeB(BooleanSensor):

    def __init__(self, name: str = "se_b"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "sensor_locations"


class SeC(BooleanSensor):

    def __init__(self, name: str = "se_c"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "sensor_locations"


class SeD(BooleanSensor):

    def __init__(self, name: str = "se_d"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "sensor_locations"
