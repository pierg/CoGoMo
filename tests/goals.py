from contract import Contract
from goal import Goal
from tests.testtypes import *

c1 = Contract(assumptions=a, guarantees=b)
print(c1)

c2 = Contract(assumptions=c, guarantees=d)
print(c2)

c3 = Contract(assumptions=e, guarantees=f)
print(c2)

c4 = Contract(assumptions=g, guarantees=e)
print(c2)

g1 = Goal(name="g1",
          description="test_goal 1",
          specification=c1)

g2 = Goal(name="g2",
          description="test_goal 2",
          specification=c2)

print(g1)
print(g2)

g12 = Goal.composition({g1, g2})

print(g12)

g3 = Goal(name="g4",
          description="test_goal 1",
          specification=c3)

g4 = Goal(name="g3",
          description="test_goal 2",
          specification=c4)

