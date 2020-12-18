from goal.cgg import Node
from contract import Contract
from tests.types import *

c1 = Contract(assumptions=a, guarantees=b)
print(c1)

c2 = Contract(assumptions=c, guarantees=d)
print(c2)

n1 = Node(name="g1",
          description="test_goal 1",
          specification=c1)

n2 = Node(name="g2",
          description="test_goal 2",
          specification=c2)

print(n1)
print(n2)

n3 = Node.composition({n1, n2})

print(n3)
