from itertools import permutations

from formula.patterns.robotic_patterns import *
from goal import Goal
from typeset.types.context import ContextTime
from typeset.types.robots.sensors import *

types = {
    ContextTime("time"),
    LiftingPower("lifting_power"),
    ObjectRecognitionSensor("see_package"),
    Pickup("pick_package"),
    ReachLocation("go_corridor"),
    ReachLocation("go_a"),
    ReachLocation("go_b"),
}

t = Typeset(types)

rules = {
    "refinement": [
        Patrolling([t["go_corridor"]]) << Patrolling([t["go_a"], t["go_b"]])
    ]
}

one = t["time"] > 17
two = t["time"] < 9

c1 = (t["time"] > 17) | (t["time"] < 9)
c2 = ~((t["time"] > 17) | (t["time"] < 9))

print(c1)
print(c2)

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
    ),
]

comparisons = permutations(rules["refinement"], 2)

relationships = []

for p1, p2 in comparisons:

    if p1 <= p2:
        if p1 == p2:
            relationships.tpend(type(p1).__name__ + " = " + type(p2).__name__)
        else:
            relationships.tpend(type(p1).__name__ + " < " + type(p2).__name__)

print(*relationships, sep='\n')
