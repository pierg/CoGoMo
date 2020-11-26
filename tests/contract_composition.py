from specification.contract import Contract
from specification.formula import FormulaOutput
from specification.atom import Atom
from specification.formula import Formula
from type import MutexType
from type.subtypes.locations import ReachLocation
from typeset import Typeset


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


a = GoA()
b = GoB()
c = GoC()
d = GoD()

a = Formula(Atom((a.name, Typeset({a}))))
b = Formula(Atom((b.name, Typeset({b}))))

c = Formula(Atom((c.name, Typeset({c}))))
d = Formula(Atom((d.name, Typeset({d}))))

c1 = Contract(assumptions=a, guarantees=b)
c2 = Contract(assumptions=c, guarantees=d)

c12 = Contract.composition({c1, c2})

print(str(c12))
