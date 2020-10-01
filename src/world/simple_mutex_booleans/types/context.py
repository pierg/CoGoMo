from typeset.types.basic import MutexType
from typeset.types.subtypes.context import *


class MutexContext(MutexType):
    pass


class X1(ContextIdentity, MutexContext):

    def __init__(self, name: str = "x1"):
        super().__init__(name)


class X2(ContextIdentity, MutexContext):

    def __init__(self, name: str = "x2"):
        super().__init__(name)


class C3(ContextIdentity):

    def __init__(self, name: str = "c3"):
        super().__init__(name)
