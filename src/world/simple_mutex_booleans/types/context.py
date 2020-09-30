from typeset.types.basic import MutexType
from typeset.types.subtypes.context import *


class MutexContext(MutexType):
    pass


class C1(ContextIdentity, MutexContext):

    def __init__(self, name: str = "c1"):
        super().__init__(name)


class C2(ContextIdentity, MutexContext):

    def __init__(self, name: str = "c2"):
        super().__init__(name)


class C3(ContextIdentity, MutexContext):

    def __init__(self, name: str = "c3"):
        super().__init__(name)
