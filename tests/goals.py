from contract import Contract
from goal import Goal
from tests.types import *

c1 = Contract(assumptions=a, guarantees=b)
print(c1)

c2 = Contract(assumptions=c, guarantees=d)
print(c2)

g1 = Goal(name="g1",
          description="test_goal 1",
          specification=c1)

g2 = Goal(name="g2",
          description="test_goal 2",
          specification=c2)

print(g1)
print(g2)

g3 = Goal.composition({g1, g2})

print(g3)
