from tools.reactive_synthesis import *


def get_world_model():
    """The designer specifies a mission using the predefined catalogue of dywer
       In addition to the dywer to use the designer specifies also in which context each goal can be active"""

    """ Atomic propositions divided in
            sensor  - sensor propositions (uncontrollable) - binary sensor variables
            location  - location propositions (controllable e.g. goto) - are true if the robot is located in the location
            action  - action propositions (controllable) - set of actions that are active (true)"""
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
            general_str_to_LTL(
                formula="G((!r1 & !r3 & !r5 & !r8) -> ((X nemo) <-> nemo))",
                variables_str=["r1", "r3", "r5", "r8", "nemo"],
                ap=ap)
        ]
    }

    system_rules = {
        "initial": [
            (ap["r1"] & ~ap["r2"] & ~ap["r3"] & ~ap["r4"] & ~ap["r5"] & ~ap["r6"] & ~ap["r7"] &
             ~ap["r8"] & ~ap["r9"] & ~ap["r10"] & ~ap["r11"] & ~ap["r12"] & ~ap["camera_on"])

            | (~ap["r1"] & ap["r2"] & ~ap["r3"] & ~ap["r4"] & ~ap["r5"] & ~ap["r6"] & ~ap["r7"] &
               ~ap["r8"] & ~ap["r9"] & ~ap["r10"] & ~ap["r11"] & ~ap["r12"] & ~ap["camera_on"])

            | (~ap["r1"] & ~ap["r2"] & ap["r3"] & ~ap["r4"] & ~ap["r5"] & ~ap["r6"] & ~ap["r7"] &
               ~ap["r8"] & ~ap["r9"] & ~ap["r10"] & ~ap["r11"] & ~ap["r12"] & ~ap["camera_on"])
        ],
        "transitions":[
            adjacencies_str_to_LTL(
                map_dict={
                    "r1": ["r1", "r9"],
                    "r2": ["r2", "r12"],
                    "r3": ["r3", "r11"],
                    "r4": ["r4", "r11"],
                    "r5": ["r5", "r10"],
                    "r6": ["r6", "r10"],
                    "r7": ["r7", "r10"],
                    "r8": ["r8", "r9"],
                    "r9": ["r9", "r1", "r8", "r10", "r12"],
                    "r10": ["r10", "r9", "r7", "r6", "r5", "r11"],
                    "r11": ["r11", "r10", "r4", "r3", "r12"],
                    "r12": ["r12", "r11", "r2", "r9"],
                },
                ap=ap),
            general_str_to_LTL(
                formula="G(X nemo -> ((X r1 <-> r1) & (X r2 <-> r2) & (X r3 <-> r3) & (X r4 <-> r4) & (X r5 <-> r5) & "
                        "(X r6 <-> r6) & (X r7 <-> r7) & (X r8 <-> r8) & (X r9 <-> r9) & (X r10 <-> r10) & "
                        "(X r11 <-> r11) & (X r12 <-> r12)) & X camera_on)",
                variables_str=["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12", "camera_on",
                               "nemo"],
                ap=ap
            )
        ],
        "constraints":
            mutex_str_to_LTL(
                mutex_list=["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12"],
                ap=ap)
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
