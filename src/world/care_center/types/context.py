from typeset.types.subtypes.context import *


class Time(ContextTime):

    def __init__(self, name: str = "time"):
        super().__init__(name)


class Mild(MutexContextIdentity):

    def __init__(self, name: str = "mild_symptoms"):
        super().__init__(name)


class Severe(MutexContextIdentity):

    def __init__(self, name: str = "severe_symptoms"):
        super().__init__(name)


class Insured(MutexContextIdentity):

    def __init__(self, name: str = "insured"):
        super().__init__(name)


class Entrance(MutexContextLocation):

    def __init__(self, name: str = "entrance"):
        super().__init__(name)


class Pharmacy(MutexContextLocation):

    def __init__(self, name: str = "pharmacy"):
        super().__init__(name)


class Corridoor(MutexContextLocation):

    def __init__(self, name: str = "corridor"):
        super().__init__(name)
