from typeset.types.basic import BoundedInteger, Boolean


class ContextTime(BoundedInteger):

    def __init__(self, name: str):
        super().__init__(name, min_value=0, max_value=24)
        self.kind = "time"


class ContextLocation(Boolean):

    def __init__(self, name: str):
        super().__init__(name)
