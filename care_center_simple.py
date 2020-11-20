from specification.atom import Atom
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


a = GoA()
b = GoB()


print(a.name)
print(b.name)
typeset = Typeset({a, b})
print(typeset)

a = Atom(a.name, Typeset({a}))
b = Atom(b.name, Typeset({b}))

print(a.is_satisfiable())
print(b)

