from typeset.types.subtypes.actions import BooleanAction


class Greeting(BooleanAction):

    def __init__(self, name: str = "do_greeting"):
        super().__init__(name)


class Pickup(BooleanAction):

    def __init__(self, name: str = "do_pickup"):
        super().__init__(name)


class Charge(BooleanAction):

    def __init__(self, name: str = "do_charge"):
        super().__init__(name)
