import os

from components.components import ComponentsLibrary, SimpleComponent, Component
from contracts.contract import PContract
from src.goals.cgtgoal import *
from typescogomo.subtypes.patterns import *
from typescogomo.subtypes.scopes import *


def get_inputs():
    """The designer specifies a mission using the predefined catalogue of patterns
       In addition to the patterns to use the designer specifies also in which context each goal can be active"""

    print("CUSTOM SPEC 5 complete")
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
            "severe": LTL("severe"),
            "mild": LTL("mild")
        },
        "s": {
            "temperature_checked": LTL("temperature_checked"),
            "low_battery": LTL("low_battery"),
            "doctor_arrived": LTL("doctor_arrived"),
            "patient_is_following": LTL("patient_is_following"),
            "full_battery": LTL("full_battery"),
            "get_med": LTL("get_med"),
            "look_up_meds": LTL("look_up_meds"),
            "label_correct": LTL("label_correct"),
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
            "g": LTL("g"),
            "waiting": LTL("waiting"),
            "isolation": LTL("isolation"),
            "charging": LTL("charging")
        },
        "a": {
            "measure_temperature": LTL("measure_temperature"),
            "stay_with_patient": LTL("stay_with_patient"),
            "contact_station": LTL("contact_station"),
            "welcome_patient": LTL("welcome_patient"),
            "search_shelf": LTL("search_shelf"),
            "check_label": LTL("check_label"),
            "pick_up_medicine": LTL("pick_up_medicine"),
            "give_med": LTL("give_med"),
            "identify_customer": LTL("identify_customer"),
            "deliver_medicine": LTL("deliver_medicine")
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
                [ap["cl"]["entrance"], ap["cl"]["pharmacy"], ap["cl"]["corridor"]],
            ],
            "inclusion": {
                ap["l"]["a"]: ap["cl"]["entrance"],
                ap["l"]["d"]: ap["cl"]["pharmacy"],
                SequencedPatrolling([ap["l"]["b"], ap["l"]["c"], ap["l"]["e"], ap["l"]["f"]]):
                    SequencedPatrolling([ap["cl"]["corridor"]]),

            }
        },
        "gridworld": {
            ap["l"]["a"]: [ap["l"]["a"], ap["l"]["b"], ap["l"]["d"]],
            ap["l"]["b"]: [ap["l"]["b"], ap["l"]["a"], ap["l"]["c"], ap["l"]["waiting"]],
            ap["l"]["c"]: [ap["l"]["c"], ap["l"]["b"], ap["l"]["d"], ap["l"]["e"], ap["l"]["isolation"]],
            ap["l"]["d"]: [ap["l"]["d"], ap["l"]["a"], ap["l"]["c"]],
            ap["l"]["e"]: [ap["l"]["e"], ap["l"]["c"], ap["l"]["f"]],
            ap["l"]["f"]: [ap["l"]["f"], ap["l"]["e"], ap["l"]["g"], ap["l"]["charging"]],
        },
        "constraints": {
            "mutex": [[
                ap["l"]["a"],
                ap["l"]["b"],
                ap["l"]["c"],
                ap["l"]["d"],
                ap["l"]["e"],
                ap["l"]["f"],
            ]],
            "inclusion": {
            }
        }
    }

    """List of specifications / goals"""
    list_of_goals = [
        CGTGoal(
            name="patrolling",
            description="patrol the care-center",
            contracts=[PContract([
                SequencedPatrolling([ap["cl"]["entrance"], ap["cl"]["pharmacy"], ap["cl"]["corridor"]])
            ])]
        )
    ]

    """Instantiating a Library of Goals"""
    component_library = GoalsLibrary(name="hospital")

    component_library.add_goals(
        [
            CGTGoal(
                name="seq-patrol-b-c-e-f",
                description="patrol areas b, c, e and f",
                contracts=[PContract([
                    SequencedPatrolling(
                        [ap["l"]["a"], ap["l"]["d"], ap["l"]["b"], ap["l"]["c"], ap["l"]["e"], ap["l"]["f"]])
                ])]
            )
        ]
    )

    for c in component_library.goals:
        print(c.contracts[0].guarantees.formula)

    return ap, rules, list_of_goals, component_library
