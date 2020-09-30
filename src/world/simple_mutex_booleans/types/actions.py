from typeset.types.basic import MutexType
from typeset.types.subtypes.actions import BooleanAction


class MutexActions(MutexType):
    pass


class A1(BooleanAction, MutexActions):

    def __init__(self, name: str = "a1"):
        super().__init__(name)


class A2(BooleanAction, MutexActions):

    def __init__(self, name: str = "a2"):
        super().__init__(name)


class A3(BooleanAction, MutexActions):

    def __init__(self, name: str = "a3"):
        super().__init__(name)
