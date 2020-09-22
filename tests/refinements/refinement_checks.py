from formula.patterns.robotic_patterns import *
from typeset.types.subtypes.context import ContextTime
from world.care_center.types.sensors import *
from world.care_center.types.actions import *
from world.care_center.types.locations import *

variables = {
    ContextTime(),
    LiftingPower(),
    ObjectRecognition("see_package"),
    Pickup("pick_package"),
    GoCorridor(),
    GoB(),
    GoC(),
    GoD(),
    GoE(),
    GoF()
}

t = Typeset(variables)

print(t)


a = Patrolling([t["go_b"], t["go_c"], t["go_d"], t["go_e"]]) & Patrolling([t["go_corridor"]])
b = Patrolling([t["go_b"]]) & Patrolling([t["go_corridor"]])
c = Patrolling([t["go_f"]]) & Patrolling([t["go_corridor"]])



print("\n")
for goal in goals:
    print(goal)


cond_b = Patrolling([t["go_b"]]) <= Patrolling([t["go_corridor"]])
cond_d = Patrolling([t["go_b"], t["go_c"], t["go_d"], t["go_e"]]) <= Patrolling([t["go_corridor"]])

cond_bd = cond_b <= cond_d
cond_db = cond_d == cond_b


print(cond_b)
print(cond_d)
print(cond_bd)
print(cond_db)
