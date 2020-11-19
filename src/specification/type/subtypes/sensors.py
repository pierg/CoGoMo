from specification.typeset import BoundedInteger, Boolean


class IntegerSensor(BoundedInteger):

    def __init__(self, name: str, min_value=0, max_value=50):
        super().__init__(name, min_value=min_value, max_value=max_value)
        self.kind = "sensor"


class MutexIntegerSensor(BoundedInteger):

    def __init__(self, name: str, min_value=0, max_value=50):
        super().__init__(name, min_value=min_value, max_value=max_value)
        self.kind = "sensor"


class BooleanSensor(Boolean):

    def __init__(self, name: str):
        super().__init__(name)
        self.kind = "sensor"


class MutexBooleanSensor(Boolean):

    def __init__(self, name: str):
        super().__init__(name)
        self.kind = "sensor"
