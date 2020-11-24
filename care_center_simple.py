from specification.atom import Atom
from specification.formula import LTL
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


print(a.name)
print(b.name)
typeset = Typeset({a, b})
print(typeset)

a = Atom((a.name, Typeset({a})))
b = Atom((b.name, Typeset({b})))

c = Atom((c.name, Typeset({c})))
d = Atom((d.name, Typeset({d})))

a_ltl = LTL(atom=a)
b_ltl = LTL(atom=b)

one = a_ltl | b_ltl
print(one)

two = c & d

print(two)

three = one & two

print(three)

