from specification.typeset import BoundedInteger, Boolean


class ContextTime(BoundedInteger):

    def __init__(self, name: str = "time"):
        super().__init__(name, min_value=0, max_value=24)
        self.kind = "time"


class ContextBooleanTime(Boolean):

    def __init__(self, name: str = "time"):
        super().__init__(name)
        self.kind = "time"


class ContextLocation(Boolean):

    def __init__(self, name: str = "location"):
        super().__init__(name)
        self.kind = "location"


class ContextIdentity(Boolean):

    def __init__(self, name: str = "identity"):
        super().__init__(name)
        self.kind = "identity"
