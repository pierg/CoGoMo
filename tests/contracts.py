from contract import Contract
from specification.atom.pattern.basic import Init
from worlds.simple_gridworld import SimpleGridWorld

sw = SimpleGridWorld()

t = sw.typeset

"""We are using the Init pattern which is basically atom corresponding to the type at time zero, 
    e.g. type: a => atom: a"""

c1 = Contract(assumptions=Init(t["se_a"]), guarantees=Init(t["a"]))
print(c1)


#
# c2 = Contract(assumptions=Init(t["se_b"]), guarantees=Init(t["b"]))
# print(c2)
#
#
# c12 = Contract.composition({c1, c2})
# print(c12)
#
#
# c3 = Contract(assumptions=Init(t["se_c"]), guarantees=Init(t["c"]))
# print(c2)
#
#
# c123 = Contract.conjunction({c12, c3})
# print(c123)
#
#
#



