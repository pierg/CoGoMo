from __future__ import annotations

from copy import deepcopy
from typing import Set

from tools.logic import Not, And, Or
from typeset import Typeset

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from formula import LTL




def extract_refinement_rules(variables: Typeset) -> Set[LTL]:
    rules: Set[LTL] = set()

    for variable, supertypes in variables.supertypes.items():
        for supertype in supertypes:
            formula = "G(" + variable.name + " -> " + supertype.name + ")"
            rule = LTL(formula=formula, variables=Typeset({variable, supertype}), kind="refinement_rule")
            rules.add(rule)

    return rules

def extract_mutex_rules(variables: Typeset) -> Set[LTL]:
    rules: Set[LTL] = set()

    for mutextypes in variables.mutextypes:
        if len(mutextypes) > 1:
            variables: Typeset = Typeset()
            ltl = "G("
            for vs in mutextypes:
                variables |= vs
            mutextypes_str = [n.name for n in mutextypes]
            clauses = []
            for vs_a in mutextypes_str:
                clause = [deepcopy(vs_a)]
                for vs_b in mutextypes_str:
                    if vs_a is not vs_b:
                        clause.append(Not(deepcopy(vs_b)))
                clauses.append(And(clause))
            ltl += Or(clauses)
            ltl += ")"
            rules.add(LTL(formula=ltl, variables=variables, kind="mutex_rule", skip_checks=True))
    return rules