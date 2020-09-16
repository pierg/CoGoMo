import re
from typing import Dict, List, Tuple
from goal import Goal
from tools.logic import Implies
from controller.parser import parse_controller
from controller.synthesis import create_controller_if_exists
from tools.strings_manipulation import save_to_file
from typescogomo.formula import LTL
from old_src.typescogomo.variables import Variables



def generate_general_controller_inputs_from_goal(ap: dict,
                                                 rules: dict,
                                                 goal: Goal,
                                                 complete=True) -> Tuple[
    List[str], List[str], List[str], List[str]]:
    variables = Variables()
    assumptions = []
    guarantees = []

    """Adding A/G from the goal"""
    a = goal.get_ltl_assumptions().formula
    if a != "TRUE":
        assumptions.append(a)
    g = goal.get_ltl_guarantees().formula
    if g != "TRUE":
        guarantees.append(g)
    variables |= goal.get_variables()

    """Adding liveness rules of the environemnt as assumptions"""
    liveness_rules = extract_ltl_rules(rules["environment"])
    for r in liveness_rules:
        variables |= r.variables
        assumptions.append(r.formula)

    """Adding domain rules of the robot as guarantees"""
    domain_rules = extract_ltl_rules(rules["domain"])
    for r in domain_rules:
        variables |= r.variables
        guarantees.append(r.formula)

    """Adding context rules as assumptions if not already included (cgt includes them)"""
    if complete:
        context_rules = extract_ltl_rules(rules["context"])
        for r in context_rules:
            variables |= r.variables
            assumptions.append(r.formula)

    uncontrollable = []
    controllable = []

    """Splitting the variables between uncontrollable and controllable"""
    for v in variables:
        if v.name in ap["s"]:
            uncontrollable.append(v.name)
        else:
            controllable.append(v.name)

    return assumptions, guarantees, uncontrollable, controllable


def syntax_fix(text: str):
    try:
        res = re.sub(r'(!)', '! ', text)
    except Exception as e:
        raise e
    return res


def realize_specification(environment_rules: Dict, system_rules: Dict, system_goals: List[LTL], ap: Dict,
                          folder_path: str):
    assumptions, guarantees, uncontrollable, controllable = generate_controller_specs(environment_rules, system_rules,
                                                                                      system_goals, ap)

    save_to_file(generate_controller_input_text(assumptions, guarantees, uncontrollable, controllable),
                 folder_path + "specification.txt")

    a, g, i, o = parse_controller(folder_path + "specification.txt")

    assumptions = a.replace("TRUE", "true")
    guarantees = g.replace("TRUE", "true")
    params = ' -k --dot -f "' + Implies(assumptions, guarantees) + '" --ins="' + i + '" --outs="' + o + '"'

    save_to_file(params, folder_path + "specification_params.txt")
    return create_controller_if_exists(folder_path + "specification.txt")


def generate_controller_specs(environment_rules: Dict, system_rules: Dict, system_goals: List[LTL], ap: Dict):
    assumptions = []
    for type, formulas in environment_rules.items():
        for formula in formulas:
            assumptions.append(formula.formula)

    guarantees = []
    for type, formulas in system_rules.items():
        for formula in formulas:
            guarantees.append(formula.formula)

    for formula in system_goals:
        guarantees.append(formula.formula)

    uncontrollable = []
    controllable = []

    for elem in ap.values():
        variable = list(elem.variables)[0]
        if variable.controllable():
            controllable.append(variable.name)
        else:
            uncontrollable.append(variable.name)

    return assumptions, guarantees, uncontrollable, controllable


def generate_controller_input_text(assum: List[str], guaran: List[str], ins: List[str], outs: List[str]):
    ret = "ASSUMPTIONS\n\n"
    for p in assum:
        ret += "\t" + syntax_fix(p) + "\n"

    ret += "\n\nGUARANTEES\n\n"
    for p in guaran:
        ret += "\t" + syntax_fix(p) + "\n"

    ret += "\n\nINPUTS\n\n"
    ret += "\t" + ", ".join(ins)

    ret += "\n\nOUTPUTS\n\n"
    ret += "\t" + ", ".join(outs)

    ret += "\n\nEND\n\n"

    return ret
