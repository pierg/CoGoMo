import os

from components.components import ComponentsLibrary, SimpleComponent, Component
from contracts.contract import PContract
from helper.reactive_synthesis import *
from src.goals.cgtgoal import *
from typescogomo.subtypes.patterns import *
from typescogomo.subtypes.scopes import *


def get_inputs():
    """The designer specifies a mission using the predefined catalogue of patterns
       In addition to the patterns to use the designer specifies also in which context each goal can be active"""

    print("CUSTOM SPEC - PATROLLING")
    print(os.path.dirname(os.path.abspath(__file__)))

    """ Atomic propositions divided in
            sensor  - sensor propositions (uncontrollable) - binary sensor variables
            location  - location propositions (controllable e.g. goto) - are true if the robot is located in the location
            action  - action propositions (controllable) - set of actions that are active (true)"""
    ap = {
        "sensor": ["nemo"],
        "location": ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12"],
        "action": ["camera_on"]
    }

    ap = process_ap(ap)

    environment_rules = {
        "initial": [
            ~ap["nemo"]
        ],
        "transitions": [
            general_LTL(
                formula="G((!r1 & !r3 & !r5 & !r8) -> ((X nemo) <-> nemo))",
                variables_str=["r1", "r3", "r5", "r8", "nemo"],
                ap=ap)
        ]
    }

    system_rules = {
        "initial": [
            ap["r1"] & ~ap["camera_on"],
            ap["r2"] & ~ap["camera_on"],
            ap["r3"] & ~ap["camera_on"],
        ],
        "transitions":
            adjacencies_LTL(
                map_dict={
                    "r1": ["r1", "r9"],
                    "r2": ["r2", "r12"],
                    "r3": ["r3", "r11"],
                    "r4": ["r4", "r11"],
                    "r5": ["r5", "r10"],
                    "r6": ["r6", "r10"],
                    "r7": ["r7", "r10"],
                    "r8": ["r8", "r9"],
                    "r9": ["r9", "r1", "r8", "r10"],
                    "r10": ["r10", "r9", "r7", "r6", "r5", "r11"],
                    "r11": ["r11", "r10", "r4", "r3", "r12"],
                    "r12": ["r12", "r11", "r2", "r9"],
                },
                ap=ap),
        "constraints":
            mutex_LTL(
                mutex_list=["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12"],
                ap=ap)
    }

    print("CIAO")

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
        ),
        CGTGoal(
            name="low-battery",
            description="always go the charging point when the battery is low",
            contracts=[PContract([
                FP_between_Q_and_R(
                    q=ap["s"]["low_battery"],
                    p=ap["l"]["charging"],
                    r=ap["s"]["full_battery"]
                )
            ])]
        )
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
