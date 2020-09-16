from world import World

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

care_center = World(atomic_propositions=ap, environment_rules=environment_rules, system_rules=system_rules)