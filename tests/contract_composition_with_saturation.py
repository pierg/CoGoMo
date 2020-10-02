from contract import Contract
from contract.operations import compose_contracts
from formula.patterns.robotic_patterns import *
from goal import Goal
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

contract_1 = Contract(
    assumptions=a1,
    guarantees=g1)

contract_2 = Contract(
    assumptions=a2,
    guarantees=g2
)

contract_12 = compose_contracts({contract_1, contract_2})

# contract_3 = Contract(
#     assumptions=a3,
#     guarantees=g3
# )
#
# goal_1 = Goal(
#     name="G1",
#     specification=contract_1
# )
#
# goal_2 = Goal(
#     name="G2",
#     specification=contract_2
# )
#
# goal_3 = Goal(
#     name="G3",
#     specification=contract_3
# )
