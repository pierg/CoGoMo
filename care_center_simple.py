from formula.patterns.robotic_patterns import *
from goal import Goal
from typeset.types.context import ContextTime
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
    GoE()
}

t = Typeset(variables)

print(t)

# rules = {
#     "refinement": [
#         Patrolling([t["go_corridor"]]) << Patrolling([t["go_b"], t["go_c"], t["go_d"], t["go_e"]])
#     ]
# }

goals = [
    Goal(
        name="patrol",
        context=(t["time"] > 17) | (t["time"] < 9),
        specification=PromptReaction(
            trigger=t["see_package"],
            reaction=t["pick_package"])
    ),
    Goal(
        name="pick_up_package",
        context=~((t["time"] > 17) | (t["time"] < 9)),
        specification=Patrolling([t["go_corridor"]])
    )
]





library = [
    Goal(
        name="patrol_b",
        specification=Patrolling([t["go_b"]])
    ),
    Goal(
        name="patrol_b_c_d_e",
        specification=Patrolling([t["go_b"], t["go_c"], t["go_d"], t["go_e"]])
    ),
]

print(Patrolling([t["go_corridor"]]) << Patrolling([t["go_b"], t["go_c"], t["go_d"], t["go_e"]]))

print("\n")
for goal in goals:
    print(goal)
