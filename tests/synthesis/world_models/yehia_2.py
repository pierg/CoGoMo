from helper.reactive_synthesis import *


def get_world_model():
    """The designer specifies a mission using the predefined catalogue of patterns
       In addition to the patterns to use the designer specifies also in which context each goal can be active"""

    """ Atomic propositions divided in
            sensor  - sensor propositions (uncontrollable) - binary sensor variables
            location  - location propositions (controllable e.g. goto) - are true if the robot is located in the location
            action  - action propositions (controllable) - set of actions that are active (true)"""
    ap = {
        "sensor": ["s1", "s2", "s3", "s4", "s5"],
        "location": ["r1", "r2", "r3", "r4", "r5"],
        "action": []
    }

    ap = process_ap(ap)

    environment_rules = {
        "initial": [
            ap["s1"]
        ],
        "transitions": [
            adjacencies_str_to_LTL(
                map_dict={
                    "s1": ["s1", "s5"],
                    "s2": ["s2", "s5"],
                    "s3": ["s3", "s5"],
                    "s4": ["s4", "s5"]
                },
                ap=ap),

            infinetely_often_str_to_LTL(["s1", "s2", "s3", "s4", "s5"], ap),
        ],
        "constraints": [
            mutex_str_to_LTL(["s1", "s2", "s3", "s4", "s5"], ap)
        ]
    }

    system_rules = {
        "initial": [
            ap["r1"]
        ],
        "transitions": [
            general_str_to_LTL("G( s1 <-> r1)", variables_str=["s1", "r1"], ap=ap),
            general_str_to_LTL("G( s2 <-> r2)", variables_str=["s2", "r2"], ap=ap),
            general_str_to_LTL("G( s3 <-> r3)", variables_str=["s3", "r3"], ap=ap),
            general_str_to_LTL("G( s4 <-> r4)", variables_str=["s4", "r4"], ap=ap),
            general_str_to_LTL("G( s5 <-> r5)", variables_str=["s5", "r5"], ap=ap),
        ],
        "constraints": [
            mutex_str_to_LTL(["r1", "r2", "r3", "r4", "r5"], ap)
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
