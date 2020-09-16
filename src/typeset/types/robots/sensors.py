from typeset.types.basic import BoundedInteger, Boolean


class HumanDetection(Boolean):

    def __init__(self, name: str):
        super().__init__(name)


class LiftingPower(BoundedInteger):

    def __init__(self, name: str):
        super().__init__(name, min_value=0, max_value=50)
        self.kind = "characteristics"


class BatteryIndicator(BoundedInteger):

    def __init__(self, name: str):
        super().__init__(name, min_value=0, max_value=100)
        self.kind = "sensor"


class ReachLocation(Boolean):

    def __init__(self, name: str):
        super().__init__(name)
        self.kind = "location"


class ObjectRecognitionSensor(Boolean):

    def __init__(self, name: str):
        super().__init__(name)
        self.kind = "sensor"

class Greeting(Boolean):

    def __init__(self, name: str):
        super().__init__(name)
        self.kind = "action"


class Pickup(Boolean):

    def __init__(self, name: str):
        super().__init__(name)
        self.kind = "action"


class Charge(Boolean):

    def __init__(self, name: str):
        super().__init__(name)
        self.kind = "action"
