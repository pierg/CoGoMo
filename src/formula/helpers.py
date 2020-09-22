from __future__ import annotations

from typing import Set
from typeset import Typeset

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from formula import LTL


def extract_refinement_rules(variables: Typeset) -> Set[LTL]:
    rules: Set[LTL] = set()

    for variable in variables.values():
        for supertype in variable.supertypes:
            formula = "G(" + variable.name + " -> " + supertype.name + ")"
            rule = LTL(formula=formula, variables=variable | supertype)
            rules.add(rule)

    return rules
