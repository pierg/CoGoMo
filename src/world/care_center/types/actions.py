from typeset.types.basic import MutexType
from typeset.types.subtypes.actions import BooleanAction


class MutexActions(MutexType):
    pass


class Greeting(BooleanAction, MutexActions):

    def __init__(self, name: str = "do_greeting"):
        super().__init__(name)


class Pickup(BooleanAction, MutexActions):

    def __init__(self, name: str = "do_pickup"):
        super().__init__(name)


class Charge(BooleanAction, MutexActions):

    def __init__(self, name: str = "do_charge"):
        super().__init__(name)
