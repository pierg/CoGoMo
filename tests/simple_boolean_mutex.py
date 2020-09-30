from contract import Contract
from formula.patterns.dywer.scopes import FP_between_Q_and_R
from formula.patterns.robotic_patterns import *
from goal import Goal
from goal.operations import create_cgt
from world.simple_mutex_booleans.types.sensors import *
from world.simple_mutex_booleans.types.actions import *
from world.simple_mutex_booleans.types.locations import *
from world.simple_mutex_booleans.types.context import *

"""A = actions, C = context, L = location, S = sensors"""
variables = {
    A1(), A2(), A3(),
    C1(), C2(), C3(),
    L1(), L2(), L3(),
    S1(), S2(), S3()
}

t = Typeset(variables)

a1 = t["s1"].assign_true()
a2 = t["s2"].assign_true()
c1 = t["c1"].assign_true()
c2 = t["c2"].assign_true()
g1 = t["a1"].assign_true()
g2 = t["a2"].assign_true()

goals_simple = {
    Goal(
        name="G1",
        context=c1,
        specification=Contract(
            assumptions=a1,
            guarantees=g1
        )
    ),
    Goal(
        name="G2",
        context=c2,
        specification=Contract(
            assumptions=a2,
            guarantees=g2
        )
    ),
}

cgt = create_cgt(goals_simple)
