from copy import deepcopy

from world.simple_mutex_booleans.types.sensors import *
from world.simple_mutex_booleans.types.actions import *
from world.simple_mutex_booleans.types.locations import *
from world.simple_mutex_booleans.types.context import *

"""A = actions, C = context, L = location, S = sensors"""
variables = {
    A1("g1"), A2("g2"), A3("g3"),
    X1("x1"), X2("x2"), C3("c3"),
    L1(), L2(), L3(),
    S1("a1"), S2("a2"), S3("a3")
}

t = Typeset(variables)

"""Assumptions"""
a1 = t["a1"].assign_true()
a2 = t["a2"].assign_true()
a3 = t["a3"].assign_true()

"""Contexts"""
x1 = t["x1"].assign_true()
x2 = t["x2"].assign_true()
c3 = t["c3"].assign_true()

"""Guarantees"""
g1 = t["g1"].assign_true()
g2 = t["g2"].assign_true()
g3 = t["g3"].assign_true()

phi_1 = a1 >> g1
print(phi_1)
phi_2 = a2 >> g2
print(phi_2)
phi_3 = a3 >> g3
print(phi_3)

psi_1 = phi_1 & phi_2
print(psi_1)

psi_1_b = deepcopy(psi_1)
psi_1_b &= phi_3
psi_5 = psi_1 & phi_3
print(psi_1_b)
print(psi_5)
