from specification.atom import Atom
from specification.formula import Formula
from type import MutexType
from type.subtypes.locations import ReachLocation
from typeset import Typeset



"""BASIC CASE: 4 MUTEX PROPOSITIONS"""

class MutexLocation(MutexType):
    pass


class GoA(ReachLocation, MutexLocation):

    def __init__(self, name: str = "a"):
        super().__init__(name, adjacent_to={"GoX", "GoB"})


class GoB(ReachLocation, MutexLocation):

    def __init__(self, name: str = "b"):
        super().__init__(name, adjacent_to={"GoX", "GoA"})


class GoC(ReachLocation, MutexLocation):

    def __init__(self, name: str = "c"):
        super().__init__(name, adjacent_to={"GoX", "GoD"})


class GoD(ReachLocation, MutexLocation):

    def __init__(self, name: str = "d"):
        super().__init__(name, adjacent_to={"GoX", "GoC"})

class GoE(ReachLocation, MutexLocation):

    def __init__(self, name: str = "e"):
        super().__init__(name, adjacent_to={"GoX", "GoD"})


class GoF(ReachLocation, MutexLocation):

    def __init__(self, name: str = "f"):
        super().__init__(name, adjacent_to={"GoX", "GoC"})


a = GoA()
b = GoB()
c = GoC()
d = GoD()
e = GoE()
f = GoF()

a = Formula(Atom((a.name, Typeset({a}))))
b = Formula(Atom((b.name, Typeset({b}))))

c = Formula(Atom((c.name, Typeset({c}))))
d = Formula(Atom((d.name, Typeset({d}))))

e = Formula(Atom((e.name, Typeset({e}))))
f = Formula(Atom((f.name, Typeset({f}))))




