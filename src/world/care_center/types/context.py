from typeset.types.basic import MutexType
from typeset.types.subtypes.context import *


class Time(ContextTime):

    def __init__(self, name: str = "time"):
        super().__init__(name)


class MutexSeverity(MutexType):
    pass


class Mild(ContextIdentity, MutexSeverity):

    def __init__(self, name: str = "mild_symptoms"):
        super().__init__(name)


class Severe(ContextIdentity, MutexSeverity):

    def __init__(self, name: str = "severe_symptoms"):
        super().__init__(name)


class MutexCovid(MutexType):
    pass


class Positive(ContextIdentity, MutexCovid):

    def __init__(self, name: str = "insured"):
        super().__init__(name)


class Negative(ContextIdentity, MutexCovid):

    def __init__(self, name: str = "negative"):
        super().__init__(name)


class MutexContextLocation(MutexType):
    pass


class Pharmacy(ContextLocation, MutexContextLocation):

    def __init__(self, name: str = "pharmacy"):
        super().__init__(name)

class Entrance(ContextLocation, MutexContextLocation):

    def __init__(self, name: str = "entrance"):
        super().__init__(name)


class Corridoor(ContextLocation, MutexContextLocation):

    def __init__(self, name: str = "corridor"):
        super().__init__(name)
