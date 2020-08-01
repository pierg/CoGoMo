import os

from components.components import ComponentsLibrary, SimpleComponent, Component
from contracts.contract import PContract
from src.goals.cgtgoal import *
from typescogomo.subtypes.patterns import *
from typescogomo.subtypes.scopes import *

print("CUSTOM SPEC v2")


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
            "g": LTL("g")
        },
        "a": {
            "contact_station": LTL("contact_station"),
            "welcome_client": LTL("welcome_client"),
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
                [ap["ci"]["premium"], ap["ci"]["normal"]]
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
                ap["s"]["get_med"]: ap["s"]["look_up_meds"]
            }
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
            ], [
                ap["a"]["search_shelf"],
                ap["a"]["check_label"],
                ap["a"]["deliver_medicine"]

            ]],
            "inclusion": {
                # ap["a"]["search_shelf"] & ap["a"]["check_label"] & ap["a"]["pick_up_medicine"]: ap["a"]["give_med"]
            }
        }
    }

    """List of specifications / goals"""
    list_of_goals = [
        CGTGoal(
            name="serve-pharmacy",
            description="patrol the care-center during the night",
            context=ap["ct"]["day"] & ap["cl"]["pharmacy"],
            contracts=[PContract([
                DelayedReaction(
                    trigger=ap["s"]["get_med"],
                    reaction=ap["a"]["give_med"])
            ])]
        )
    ]

    """Instantiating a Library of Goals"""
    component_library = GoalsLibrary(name="hospital")

    component_library.add_goals(
        [
            # CGTGoal(
            #     name="search-check-pickup",
            #     description="go to d and take medicines",
            #     context=ap["ct"]["day"],
            #     contracts=[PContract([
            #         DelayedReaction(
            #             trigger=ap["s"]["get_med"],
            #             reaction=ap["a"]["search_shelf"] & ap["a"]["check_label"] & ap["a"]["pick_up_medicine"])
            #     ])],
            # ),
            CGTGoal(
                name="search-check-pickup_2",
                description="go to d and take medicines",
                # context=ap["ct"]["day"],
                contracts=[PContract([
                    DelayedReaction(
                        trigger=ap["s"]["look_up_meds"],
                        reaction=ap["a"]["search_shelf"] & ap["a"]["check_label"]),
                    DelayedReaction(
                        trigger=ap["a"]["check_label"] & ap["a"]["search_shelf"],
                        reaction=ap["a"]["pick_up_medicine"]),
                    DelayedReaction(
                        trigger=ap["a"]["pick_up_medicine"],
                        reaction=ap["a"]["deliver_medicine"])
                ])],
            )
            # CGTGoal(
            #     name="go-to-d-and-serve_2",
            #     description="go to d and take medicines",
            #     context=ap["ct"]["day"],
            #     contracts=[PContract([
            #             ap["a"]["search_shelf"] & ap["a"]["check_label"] & ap["a"]["pick_up_medicine"]
            #     ])]
            # )
        ]
    )

    for c in component_library.goals:
        print(c.contracts[0].guarantees.formula)

    return ap, rules, list_of_goals, component_library
