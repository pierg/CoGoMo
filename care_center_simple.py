from contract import Contract
from formula.patterns.robotic_patterns import *
from goal import Goal
from goal.operations import create_cgt
from world.care_center.types.sensors import *
from world.care_center.types.actions import *
from world.care_center.types.locations import *
from world.care_center.types.context import *


variables = {
    LiftingPower(),
    ObjectRecognition("see_package"),
    Pickup("pick_package"),
    GoCorridor(),
    GoB(),
    GoC(),
    GoD(),
    GoE(),
    GoF(),
    Mild(), Severe(), Time()
}

t = Typeset(variables)

day: LTL = (t["time"] > 17) | (t["time"] < 9)
night: LTL = ~day
mild: LTL = t["mild_symptoms"]
severe: LTL = t["severe_symptoms"]

goals = [
    Goal(
        name="patrol",
        context=day,
        specification=Contract(
            assumptions=LiftingPower() > 25,
            guarantees=PromptReaction(
                trigger=t["see_package"],
                reaction=t["pick_package"])
        )
    ),
    Goal(
        name="pick_up_package",
        context=night,
        specification=Patrolling([t["go_corridor"]])
    ),
    Goal(
        name="pick_up_package",
        context=night,
        specification=Patrolling([t["go_corridor"]])
    )
]

cgt = create_cgt(goals)

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
