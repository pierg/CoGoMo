from itertools import combinations, permutations

from formula.patterns.basic import G
from formula.patterns.robotic_patterns import *
from typeset.types.robots.sensors import *
from world import World

"""List of types"""
# t = {
#     "lifting_power": LiftingPower("lifting_power"),
#     "battery_level": BatteryIndicator("battery_level"),
#     "a": ReachLocation("a"),
#     "b": ReachLocation("b"),
#     "c": ReachLocation("c"),
#     "d": ReachLocation("d"),
#     "e": ReachLocation("e"),
#     "f": ReachLocation("f"),
#     "corridor": ReachLocation("corridor"),
#     "charging_room": ReachLocation("charging_room"),
#     "entrance": ReachLocation("entrance"),
#     "care_center": ReachLocation("care_center"),
#     "welcome_patient": Greeting("welcome"),
#     "package_pickup": Pickup("package"),
#     "charge_battery": Charge("charge_battery"),
# }

tset = {
    ReachLocation("a"),
    ReachLocation("b"),
    ReachLocation("c"),
    ReachLocation("d"),
    ReachLocation("corridor"),
}

t = Typeset(tset)

print(t["a"])
print(t["b"])


rules = {
    "refinement": [
        Patrolling([t["corridor"]]) << Patrolling([t["a"], t["b"], t["c"], t["d"]])
    ]
}

comparisons = permutations(rules["refinement"], 2)

relationships = []

for p1, p2 in comparisons:

    if p1 <= p2:
        if p1 == p2:
            relationships.append(type(p1).__name__ + " = " + type(p2).__name__)
        else:
            relationships.append(type(p1).__name__ + " < " + type(p2).__name__)

print(*relationships, sep='\n')
