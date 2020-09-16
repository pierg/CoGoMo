from typing import Tuple

from tools.reactive_synthesis import *


def get_world_model() -> Tuple[Dict, Dict, Dict]:
    """The designer specifies a mission using the predefined catalogue of dywer
       In addition to the dywer to use the designer specifies also in which context each goal can be active"""

    """ Atomic propositions divided in
            sensor  - sensor propositions (uncontrollable) - binary sensor variables
            location  - location propositions (controllable e.g. goto) - are true if the robot is located in the location
            action  - action propositions (controllable) - set of actions that are active (true)"""
    ap = {
        "sensor": ["temperature_checked",
                   "low_battery",
                   "doctor_arrived",
                   "patient_is_following",
                   "full_battery",
                   "get_med",
                   "look_up_meds",
                   "label_correct",
                   "human_entered",
                   "guard_entered",
                   "door_alarm",
                   "fire_alarm",
                   "day",
                   "night",
                   "severe",
                   "mild",
                   "package_arrived"],

        "location": ["a",
                     "b",
                     "c",
                     "d",
                     "e",
                     "f",
                     "g",
                     "waiting",
                     "isolation",
                     "charging",
                     "entrance",
                     "pharmacy",
                     "medical_room",
                     "corridor",
                     "care_center"],

        "action": ["measure_temperature",
                   "stay_with_patient",
                   "contact_station",
                   "welcome_patient",
                   "search_shelf",
                   "check_label",
                   "pick_up_medicine",
                   "give_med",
                   "identify_customer",
                   "deliver_medicine",
                   "package_pickup"]
    }

    ap = process_ap(ap)

    environment_rules = {
        "initial": [
        ],
        "transitions": [
        ],
        "constraints": [
        ],
        "refinement": [
        ]
    }

    system_rules = {
        "initial": [
        ],
        "transitions": [
        ],
        "constraints": [
        ],
        "refinement": [
        ]
    }

    # Flattening of dictionaries of rules so that there is only one list for each key
    for key, values in environment_rules.items():
        flat_list = []
        for value in values:
            if isinstance(value, list):
                flat_list.extend(value)
            else:
                flat_list.append(value)
        environment_rules[key] = flat_list

    for key, values in system_rules.items():
        flat_list = []
        for value in values:
            if isinstance(value, list):
                flat_list.extend(value)
            else:
                flat_list.append(value)
        system_rules[key] = flat_list

    return environment_rules, system_rules, ap
