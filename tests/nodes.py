from goal import Goal
from goal.cgg import Node
from contract import Contract
from tests.testtypes import *

c1 = Contract(assumptions=a, guarantees=b)
c2 = Contract(assumptions=c, guarantees=d)
c3 = Contract(assumptions=e, guarantees=f)
c4 = Contract(assumptions=g, guarantees=e)

g2 = Goal(name="g2",
          description="test_goal 2",
          specification=c2)

n1 = Node(name="g1",
          description="test_goal 1",
          specification=c1)

g3 = Goal(name="g3",
          description="test_goal 1",
          specification=c3)

g4 = Goal(name="g4",
          description="test_goal 2",
          specification=c4)


n2 = Node(goal=g2)
n3 = Node(goal=g3)
n4 = Node(goal=g4)


print(n1)
print(n2)

n12 = Node.composition({n1, n2})

print(n3)


n34 = Node.composition({n3, n4})

print(n34)

n12_34 = Node.conjunction({n12, n34})

print(n12_34)


