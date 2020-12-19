from contract import Contract
from tests.testtypes import *


c1 = Contract(assumptions=a, guarantees=b)
print(c1)

c2 = Contract(assumptions=c, guarantees=d)
print(c2)


c12 = Contract.composition({c1, c2})
print(c12)


c1 = Contract(assumptions=a, guarantees=b)
print(c1)

c2 = Contract(assumptions=c, guarantees=d)
print(c2)


c12 = Contract.composition({c1, c2})
print(c12)

c3 = Contract(assumptions=e, guarantees=f)
print(c2)


c123 = Contract.conjunction({c12, c3})
print(c123)






