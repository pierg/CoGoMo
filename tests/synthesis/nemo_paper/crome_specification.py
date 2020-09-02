import os

from checks.tools import Implies
from controller.parser import parse_controller
from controller.synthesis import create_controller_if_exists, SynthesisException
from goals.helpers import generate_controller_input_text
from helper.reactive_synthesis import *
from helper.tools import save_to_file

folder_path = os.path.dirname(os.path.abspath(__file__)) + "/"


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
            (ap["r1"] & ~ap["r2"] & ~ap["r3"] & ~ap["r4"] & ~ap["r5"] & ~ap["r6"] & ~ap["r7"] &
             ~ap["r8"] & ~ap["r9"] & ~ap["r10"] & ~ap["r11"] & ~ap["r12"] & ~ap["camera_on"])

            | (~ap["r1"] & ap["r2"] & ~ap["r3"] & ~ap["r4"] & ~ap["r5"] & ~ap["r6"] & ~ap["r7"] &
               ~ap["r8"] & ~ap["r9"] & ~ap["r10"] & ~ap["r11"] & ~ap["r12"] & ~ap["camera_on"])

            | (~ap["r1"] & ~ap["r2"] & ap["r3"] & ~ap["r4"] & ~ap["r5"] & ~ap["r6"] & ~ap["r7"] &
               ~ap["r8"] & ~ap["r9"] & ~ap["r10"] & ~ap["r11"] & ~ap["r12"] & ~ap["camera_on"])
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
                    "r9": ["r9", "r1", "r8", "r10", "r12"],
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

    system_specifications = [
        general_LTL(
            formula="G(X nemo -> ((X r1 <-> r1) & (X r2 <-> r2) & (X r3 <-> r3) & (X r4 <-> r4) & (X r5 <-> r5) & "
                    "(X r6 <-> r6) & (X r7 <-> r7) & (X r8 <-> r8) & (X r9 <-> r9) & (X r10 <-> r10) & "
                    "(X r11 <-> r11) & (X r12 <-> r12)) & X camera_on)",
            variables_str=["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12", "camera_on",
                           "nemo"],
            ap=ap
        ),
        general_LTL(
            formula="G (! (X nemo) -> ! (X camera_on) )",
            variables_str=["camera_on", "nemo"],
            ap=ap
        ),
        general_LTL(
            formula="G (F (r1 | nemo)) & G (F (r3 | nemo)) & G (F (r5 | nemo)) & G (F (r8 | nemo))",
            variables_str=["r1", "r3", "r5", "r8", "nemo"],
            ap=ap
        ),
    ]

    return environment_rules, system_rules, system_specifications, ap


environment_rules, system_rules, system_specifications, ap = get_inputs()

assumptions = []
for type, formulas in environment_rules.items():
    for formula in formulas:
        assumptions.append(formula.formula)

guarantees = []
for type, formulas in system_rules.items():
    for formula in formulas:
        guarantees.append(formula.formula)

for formula in system_specifications:
    guarantees.append(formula.formula)

uncontrollable = []
controllable = []
for elem in ap.values():
    variable = list(elem.variables)[0]
    if variable.controllable():
        controllable.append(variable.name)
    else:
        uncontrollable.append(variable.name)

save_to_file(generate_controller_input_text(assumptions, guarantees, uncontrollable, controllable),
             folder_path + "specification.txt")

a, g, i, o = parse_controller(folder_path + "specification.txt")

assumptions = a.replace("TRUE", "true")
guarantees = g.replace("TRUE", "true")
params = 'docker run lazkany/strix -f "' + Implies(assumptions,
                                                   guarantees) + '" --ins="' + i + '" --outs="' + o + '"' + " --k --dot"

save_to_file(params, folder_path + "specification_command.txt")

try:
    realizable, mealy_machine, exec_time = create_controller_if_exists(folder_path + "specification.txt")

    if realizable:
        print("REALIZABLE\t\tYES\t\t" + str(exec_time) + "sec")
    else:
        print("REALIZABLE\t\tNO")


except SynthesisException as e:
    if e.os_not_supported:
        print("Os not supported for synthesis. Only linux can run strix")
    elif e.trivial:
        print("The assumptions are not satisfiable. The controller is trivial.")
        raise Exception("Assumptions unsatisfiable in a CGT is impossible.")
    elif e.out_of_memory:
        print("STRIX went out of memory")
        realizable = False
        controller = None
        time_synthesis = -200
    elif e.timeout:
        print("timeout occurred")
        realizable = False
        controller = None
        time_synthesis = e.timeout_value
