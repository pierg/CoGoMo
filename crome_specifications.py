import os

from components.components import ComponentsLibrary, SimpleComponent, Component
from contracts.contract import PContract
from src.goals.cgtgoal import *
from typescogomo.subtypes.patterns import *
from typescogomo.subtypes.scopes import *


print("CUSTOM SPEC v1")


def get_inputs():
    """The designer specifies a mission using the predefined catalogue of patterns
       In addition to the patterns to use the designer specifies also in which context each goal can be active"""

    print("CUSTOM SPEC c2:")
    print(os.path.dirname(os.path.abspath(__file__)))

    """ Atomic propositions divided in
            cl - context-location propositions
            ct - context-time propositions
            ci - context-identify propositions
            s  - sensor propositions (uncontrollable)
            l  - location propositions (controllable e.g. goto)
            a  - action propositions (controllable)"""
    ap = {
        "cl": {
            "entrance": LTL("entrance"),
            "pharmacy": LTL("pharmacy"),
            "medical_room": LTL("medical_room"),
            "corridor": LTL("corridor"),
            "care_center": LTL("care_center")
        },
        "ct": {
            "day": LTL("day"),
            "night": LTL("night")
        },
        "ci": {
            "premium": LTL("premium"),
            "normal": LTL("normal")
        },
        "s": {
            "low_battery": LTL("low_battery"),
            "full_battery": LTL("full_battery"),
            "get_med": LTL("get_med"),
            "human_entered": LTL("human_entered"),
            "guard_entered": LTL("guard_entered"),
            "door_alarm": LTL("door_alarm"),
            "fire_alarm": LTL("fire_alarm")
        },
        "l": {
            "a": LTL("a"),
            "b": LTL("b"),
            "c": LTL("c"),
            "d": LTL("d"),
            "e": LTL("e"),
            "f": LTL("f"),
            "g": LTL("g")
        },
        "a": {
            "contact_station": LTL("contact_station"),
            "welcome_client": LTL("welcome_client"),
            "take_med": LTL("take_med"),
            "give_med": LTL("give_med")
        }
    }

    """Setting up controllable and uncontrollable"""
    for t, aps in ap.items():
        if t == "cl":
            for elem in aps.values():
                for v in elem.variables:
                    v.controllable = False
        if t == "ct":
            for elem in aps.values():
                for v in elem.variables:
                    v.controllable = False
        if t == "ci":
            for elem in aps.values():
                for v in elem.variables:
                    v.controllable = False
        if t == "s":
            for elem in aps.values():
                for v in elem.variables:
                    v.controllable = False
        if t == "l":
            for elem in aps.values():
                for v in elem.variables:
                    v.controllable = True
        if t == "a":
            for elem in aps.values():
                for v in elem.variables:
                    v.controllable = True

    rules = {
        "context": {
            "mutex": [
                [ap["cl"]["entrance"], ap["cl"]["pharmacy"], ap["cl"]["corridor"], ap["cl"]["medical_room"]],
                [ap["ct"]["day"], ap["ct"]["night"]],
                [ap["ci"]["premium"], ap["ci"]["normal"]]
            ],
            "inclusion": {
                ap["cl"]["entrance"]: ap["cl"]["care_center"],
                ap["cl"]["pharmacy"]: ap["cl"]["care_center"],
                ap["cl"]["medical_room"]: ap["cl"]["care_center"],
                ap["cl"]["corridor"]: ap["cl"]["care_center"]
            }
        },
        "context_gridworld": {
            ap["l"]["a"]: ap["cl"]["entrance"],
            ap["l"]["d"]: ap["cl"]["pharmacy"],
            ap["l"]["b"] | ap["l"]["c"] | ap["l"]["e"] | ap["l"]["f"]: ap["cl"]["corridor"],
            ap["l"]["g"]: ap["cl"]["medical_room"],
        },
        "gridworld": {
            ap["l"]["a"]: [ap["l"]["a"], ap["l"]["b"], ap["l"]["d"]],
            ap["l"]["b"]: [ap["l"]["b"], ap["l"]["a"], ap["l"]["c"]],
            ap["l"]["c"]: [ap["l"]["c"], ap["l"]["b"], ap["l"]["d"], ap["l"]["e"]],
            ap["l"]["d"]: [ap["l"]["d"], ap["l"]["a"], ap["l"]["c"]],
            ap["l"]["e"]: [ap["l"]["e"], ap["l"]["c"], ap["l"]["f"]],
            ap["l"]["f"]: [ap["l"]["f"], ap["l"]["e"], ap["l"]["g"]]
        },
        "system_constraints": {
            "mutex": [[
                ap["l"]["a"],
                ap["l"]["b"],
                ap["l"]["c"],
                ap["l"]["d"],
                ap["l"]["e"],
                ap["l"]["f"],
                ap["l"]["g"]
            ]],
            "inclusion": {}
        }
    }

    """List of specifications / goals"""
    list_of_goals = [
        CGTGoal(
            name="patrolling",
            description="patrol the care-center during the night",
            context=ap["ct"]["night"] | ap["ct"]["day"],
            contracts=[PContract([
                Patrolling([ap["cl"]["care_center"]])
            ])]
        )
    ]

    """Instantiating a Library of Goals"""
    component_library = GoalsLibrary(name="hospital")

    component_library.add_goals(
        [
            CGTGoal(
                name="day-patrol-entrance-pharmacy",
                description="patrol entrance and pharmacy",
                context=ap["ct"]["day"],
                contracts=[PContract([
                    Patrolling([ap["cl"]["entrance"], ap["cl"]["pharmacy"]])
                ])]
            ),
            CGTGoal(
                name="night-patrol-corridor",
                description="patrol corridor during night",
                context=ap["ct"]["night"],
                contracts=[PContract([
                    Patrolling([ap["cl"]["corridor"]])
                ])]
            ),
            CGTGoal(
                name="patrol-b-c-e-f",
                description="patrol areas b, c, e and f",
                contracts=[PContract([
                    Patrolling([ap["l"]["b"], ap["l"]["c"], ap["l"]["e"], ap["l"]["f"]])
                ])]
            ),
            CGTGoal(
                name="patrol-a-d",
                description="patrol areas a and d",
                contracts=[PContract([
                    Patrolling([ap["l"]["a"], ap["l"]["d"]])
                ])]
            )
        ]
    )

    return ap, rules, list_of_goals, component_library
