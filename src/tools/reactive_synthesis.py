from copy import deepcopy
from typing import Dict, List

from tools.logic import Not, And, Or
from typescogomo.formula import LTL
from old_src.typescogomo.variables import Variables


def process_ap(ap_dict: Dict) -> Dict:
    """Process a dictionary of strings and returns a dictionary of LTL ap"""
    new_ap_dict = {}

    for t, aps in ap_dict.items():
        for v in aps:
            ap_ltl = LTL(formula=v, kind=t, ap=True)
            new_ap_dict[v] = ap_ltl

    return new_ap_dict


def general_str_to_LTL(formula: str, variables_str: List[str], ap: Dict) -> LTL:
    variables = Variables()

    for var_str in variables_str:
        variables |= ap[var_str].variables

    return LTL(
        formula=formula,
        variables=variables,
        skip_checks=True
    )


def adjacencies_str_to_LTL(map_dict: Dict, ap: Dict) -> List[LTL]:
    list_LTL = []

    for elem_str, adjacents_str in map_dict.items():
        elem = ap[elem_str]

        adjacent = []
        for adjacent_str in adjacents_str:
            adjacent.append(ap[adjacent_str])

        ltl = "G("
        ltl += elem.formula + " -> X ("
        ltl += " | ".join([a.formula for a in adjacent])
        ltl += "))"
        variables = Variables()
        variables |= elem.variables
        for a in adjacent:
            variables |= a.variables
        list_LTL.append(LTL(formula=ltl, variables=variables, kind="adjacencies"))

    return list_LTL


def infinetely_often_str_to_LTL(ap_list: List[str], ap: Dict) -> List[LTL]:
    list_LTL = []

    for elem_str in ap_list:

        elem = ap[elem_str]
        ltl = "G( F("
        ltl += elem.formula + "))"
        variables = Variables()
        variables |= elem.variables
        list_LTL.append(LTL(formula=ltl, variables=variables, kind="infinetely_often"))

    return list_LTL


def mutex_str_to_LTL(mutex_list: List[str], ap: Dict) -> List[LTL]:
    list_LTL = []

    mtx_elements = []

    for mtx_element_strings in mutex_list:
        mtx_elements.append(ap[mtx_element_strings])

    if len(mtx_elements) > 0:
        variables: Variables = Variables()
        ltl = "G("
        for vs in mtx_elements:
            variables |= vs.variables
        clauses = []
        for vs_a in mutex_list:
            clause = [deepcopy(vs_a)]
            for vs_b in mutex_list:
                if vs_a is not vs_b:
                    clause.append(Not(deepcopy(vs_b)))
            clauses.append(And(clause, brackets=True))
        ltl += Or(clauses)
        ltl += ")"
        list_LTL.append(
            LTL(formula=ltl, variables=variables, kind="constraints", skip_checks=False))

    return list_LTL
