import os

from components.components import ComponentsLibrary, SimpleComponent, Component
from contracts.contract import PContract
from src.goals.cgtgoal import *
from typescogomo.subtypes.assumption import Assumption
from typescogomo.subtypes.patterns import *
from typescogomo.subtypes.scopes import *


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
            "day_time": LTL("day_time"),
            "night_time": LTL("night_time")
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

    rules = {
        "gridworld_map": {
            ap["l"]["a"]: [ap["l"]["a"], ap["l"]["b"], ap["l"]["d"]],
            ap["l"]["b"]: [ap["l"]["b"], ap["l"]["a"], ap["l"]["c"]],
            ap["l"]["c"]: [ap["l"]["c"], ap["l"]["b"], ap["l"]["d"], ap["l"]["e"]],
            ap["l"]["d"]: [ap["l"]["d"], ap["l"]["a"], ap["l"]["c"]],
            ap["l"]["e"]: [ap["l"]["e"], ap["l"]["c"], ap["l"]["f"]],
            ap["l"]["f"]: [ap["l"]["f"], ap["l"]["e"], ap["l"]["g"]]
        },
        "context": {
            "mutex": [
                [ap["cl"]["entrance"], ap["cl"]["pharmacy"], ap["cl"]["corridor"], ap["cl"]["medical_room"]],
                [ap["ct"]["day_time"], ap["ct"]["night_time"]],
                [ap["ci"]["premium"], ap["ci"]["normal"]]
            ],
            "inclusion": [
                [ap["cl"]["entrance"], ap["cl"]["care_center"]],
                [ap["cl"]["pharmacy"], ap["cl"]["care_center"]],
                [ap["cl"]["medical_room"], ap["cl"]["care_center"]],
                [ap["cl"]["corridor"], ap["cl"]["care_center"]]
            ]
        },
        "context_locations_map": {
            ap["l"]["a"]: [ap["cl"]["entrance"]],
            ap["l"]["d"]: [ap["cl"]["pharmacy"]],
            ap["l"]["b"] | ap["l"]["c"] | ap["l"]["e"] | ap["l"]["f"]: [ap["cl"]["corridor"]],
            ap["l"]["g"]: [ap["cl"]["medical_room"]],
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
            "inclusion": [
            ]
        }
    }

    """List of specifications / goals"""
    list_of_goals = [
        CGTGoal(
            name="night-time-patroling",
            description="patrol the care-center during the night",
            context=ap["ct"]["night_time"],
            contracts=[PContract([
                Patroling([ap["cl"]["care_center"]])
            ])]
        ),
        CGTGoal(
            name="day-time-patroling",
            description="patrol the care-center during the day",
            context=ap["ct"]["night_time"],
            contracts=[PContract([
                Patroling([ap["cl"]["care_center"]])
            ])]
        )
    ]

    """Instantiating a Library of Goals"""
    component_library = ComponentsLibrary(name="hospital")

    component_library.add_components(
        [
            Component(
                component_id="day-patrol-entrance-pharmacy",
                context=ap["ct"]["day_time"],
                guarantees=Guarantee(cnf={Patroling([ap["cl"]["entrance"], ap["cl"]["pharmacy"]])}),
            ),
            Component(
                component_id="night-patrol-corridor",
                context=ap["ct"]["night_time"],
                guarantees=Guarantee(cnf={Patroling([ap["cl"]["corridor"]])}),
            ),
            Component(
                component_id="patrol-b-c-e-f",
                guarantees=Guarantee(cnf={Patroling([ap["l"]["b"], ap["l"]["c"], ap["l"]["e"], ap["l"]["f"]])}),
            ),
            Component(
                component_id="patrol-a-d",
                guarantees=Guarantee(cnf={Patroling([ap["l"]["a"], ap["l"]["d"]])}),
            )
        ]
    )

    return ap, rules, list_of_goals
