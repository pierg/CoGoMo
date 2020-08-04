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
                [ap["cl"]["entrance"], ap["cl"]["pharmacy"], ap["cl"]["corridor"], ap["cl"]["medical_room"]],
                [ap["ct"]["day"], ap["ct"]["night"]],
                [ap["ci"]["severe"], ap["ci"]["mild"]]
            ],
            "inclusion": {
                ap["cl"]["entrance"]: ap["cl"]["care_center"],
                ap["cl"]["pharmacy"]: ap["cl"]["care_center"],
                ap["cl"]["medical_room"]: ap["cl"]["care_center"],
                ap["cl"]["corridor"]: ap["cl"]["care_center"],
                ap["l"]["a"]: ap["cl"]["entrance"],
                ap["l"]["d"]: ap["cl"]["pharmacy"],
                ap["l"]["b"] | ap["l"]["c"] | ap["l"]["e"] | ap["l"]["f"]: ap["cl"]["corridor"],
                ap["l"]["g"]: ap["cl"]["medical_room"],
                ap["a"]["deliver_medicine"]: ap["a"]["give_med"],
                ap["s"]["get_med"]: ap["s"]["look_up_meds"] & ap["s"]["label_correct"],
                ap["a"]["measure_temperature"]: ap["s"]["temperature_checked"],
                ap["l"]["waiting"]: ap["cl"]["care_center"],
                ap["l"]["isolation"]: ap["cl"]["care_center"],
                ap["l"]["charging"]: ap["cl"]["care_center"],
            }
        },
        "gridworld": {
            ap["l"]["a"]: [ap["l"]["a"], ap["l"]["b"], ap["l"]["d"]],
            ap["l"]["b"]: [ap["l"]["b"], ap["l"]["a"], ap["l"]["c"], ap["l"]["waiting"]],
            ap["l"]["c"]: [ap["l"]["c"], ap["l"]["b"], ap["l"]["d"], ap["l"]["e"], ap["l"]["waiting"]],
            ap["l"]["d"]: [ap["l"]["d"], ap["l"]["a"], ap["l"]["c"]],
            ap["l"]["e"]: [ap["l"]["e"], ap["l"]["c"], ap["l"]["f"]],
            ap["l"]["f"]: [ap["l"]["f"], ap["l"]["e"], ap["l"]["g"], ap["l"]["charging"]],
            ap["l"]["waiting"]: [ap["l"]["waiting"], ap["l"]["b"], ap["l"]["isolation"]],
            ap["l"]["isolation"]: [ap["l"]["isolation"], ap["l"]["waiting"], ap["l"]["c"]],
            ap["l"]["charging"]: [ap["l"]["charging"], ap["l"]["f"]]
        },
        "system_constraints": {
            "mutex": [[
                ap["l"]["a"],
                ap["l"]["b"],
                ap["l"]["c"],
                ap["l"]["d"],
                ap["l"]["e"],
                ap["l"]["f"],
                ap["l"]["g"],
                ap["l"]["waiting"],
                ap["l"]["isolation"],
                ap["l"]["charging"]
            ], [
                ap["a"]["search_shelf"],
                ap["a"]["check_label"],
                ap["a"]["deliver_medicine"]

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
            context=[ap["ct"]["night"], ap["ct"]["day"]],
            contracts=[PContract([
                Patrolling([ap["cl"]["care_center"]])
            ])]
        ),
        CGTGoal(
            name="serve-pharmacy",
            description="serve pharmacy during the day",
            context=ap["ct"]["day"] & ap["cl"]["pharmacy"],
            contracts=[PContract([
                DelayedReaction(
                    trigger=ap["s"]["get_med"],
                    reaction=ap["a"]["give_med"])
            ])]
        ),
        CGTGoal(
            name="welcome-patients",
            description="welcome patients at their arrival and check their temperature",
            context=[ap["ct"]["day"] & ap["cl"]["entrance"] & ap["ci"]["mild"],
                     ap["ct"]["day"] & ap["cl"]["entrance"] & ap["ci"]["severe"]],
            contracts=[PContract([
                PromptReaction(
                    trigger=ap["s"]["human_entered"],
                    reaction=ap["a"]["welcome_patient"])
            ])]
        )
        # CGTGoal(
        #     name="low-battery",
        #     description="always go the charging point and contact the main station when the battery is low",
        #     contracts=[PContract([
        #         Recurrence_P_between_Q_and_R(
        #             q=ap["s"]["low_battery"],
        #             p=ap["l"]["charging"],
        #             r=ap["s"]["full_battery"]
        #         )
        #     ])]
        # )
    ]

    """Instantiating a Library of Goals"""
    component_library = GoalsLibrary(name="hospital")

    component_library.add_goals(
        [
            CGTGoal(
                name="search-check-pickup",
                description="go to d and take medicines",
                contracts=[PContract([
                    PromptReaction(
                        trigger=ap["s"]["look_up_meds"],
                        reaction=ap["a"]["search_shelf"] & ap["a"]["check_label"]),
                    PromptReaction(
                        trigger=ap["a"]["check_label"] & ap["a"]["search_shelf"],
                        reaction=ap["a"]["pick_up_medicine"]),
                    PromptReaction(
                        trigger=ap["a"]["pick_up_medicine"],
                        reaction=ap["a"]["deliver_medicine"])
                ])],
            ),
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
                name="mild-symptoms-welcome",
                description="welcome patient with mild symptoms",
                context=ap["ci"]["mild"],
                contracts=[PContract([
                    InstantReaction(
                        trigger=ap["s"]["human_entered"],
                        reaction=ap["a"]["welcome_patient"] & ap["a"]["measure_temperature"]),
                    Wait(
                        where=ap["cl"]["entrance"],
                        until=ap["s"]["patient_is_following"]),
                    Visit([ap["l"]["waiting"]])
                ])]
            ),
            CGTGoal(
                name="severe-symptoms-welcome",
                description="welcome patient with severe symptoms",
                context=ap["ci"]["severe"],
                contracts=[PContract([
                    InstantReaction(
                        trigger=ap["s"]["human_entered"],
                        reaction=ap["a"]["welcome_patient"] & ap["a"]["measure_temperature"]),
                    Wait(
                        where=ap["cl"]["entrance"],
                        until=ap["s"]["patient_is_following"]),
                    Visit([ap["l"]["isolation"]])
                ])]
            ),
            CGTGoal(
                name="seq-patrol-b-c-e-f",
                description="patrol areas b, c, e and f",
                contracts=[PContract([
                    SequencedPatrolling([ap["l"]["b"], ap["l"]["c"], ap["l"]["e"], ap["l"]["f"]])
                ])]
            ),
            CGTGoal(
                name="seq-patrol-a-d",
                description="patrol areas a and d",
                contracts=[PContract([
                    SequencedPatrolling([ap["l"]["a"], ap["l"]["d"]])
                ])]
            )
        ]
    )

    for c in component_library.goals:
        print(c.contracts[0].guarantees.formula)

    return ap, rules, list_of_goals, component_library
