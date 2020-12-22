from type.subtypes.sensors import *


class HumanDetection(BooleanSensor):

    def __init__(self, name: str = "human_detected"):
        super().__init__(name)


class LiftingPower(IntegerSensor):

    def __init__(self, name: str = "lifting_power"):
        super().__init__(name, min_value=0, max_value=50)


class BatteryIndicator(IntegerSensor):

    def __init__(self, name: str = "battery"):
        super().__init__(name, min_value=0, max_value=100)


class ObjectRecognition(BooleanSensor):

    def __init__(self, name: str = "objected_detected"):
        super().__init__(name)
