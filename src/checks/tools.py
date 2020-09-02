import re
from typing import List

OPERATORS = r'\+|-|\*|==|<=|>=|<|>|!|\||->|&'
TEMPORALOPS = r'^F|^G|^X|^U'

operators = re.compile(OPERATORS)
temporaloperators = re.compile(TEMPORALOPS)


def And(propositions: List[str], brackets: bool = False) -> str:
    """Returns an str formula representing the logical AND of list_propoositions"""
    if len(propositions) > 1:

        if "FALSE" in propositions:
            return "FALSE"

        """Remove all TRUE elements"""
        propositions = list(filter("TRUE".__ne__, propositions))
        if len(propositions) == 0:
            return "TRUE"

        conj = ' & '.join(propositions)
        if brackets:
            return "(" + conj + ")"
        else:
            return conj

    elif len(propositions) == 1:
        return propositions[0]
    else:
        raise Exception("List of propositions is empty")


def Implies(prop_1: str, prop_2: str) -> str:
    """Returns an str formula representing the logical IMPLIES of prop_1 and prop_2"""
    return '((' + prop_1 + ') -> (' + prop_2 + '))'


def Not(prop: str) -> str:
    """Returns an str formula representing the logical NOT of prop"""
    match_operators = bool(re.search(operators, prop))
    match_temporal = bool(re.search(temporaloperators, prop))
    if match_operators or match_temporal:
        return "!(" + prop + ")"
    return "!" + prop


def Or(propositions: List[str]) -> str:
    """Returns an LTL formula representing the logical OR of list_propoositions"""
    if len(propositions) > 1:
        if "TRUE" in propositions:
            return "TRUE"
        """Remove all FALSE elements"""
        propositions = list(filter("FALSE".__ne__, propositions))

        res = " | ".join(propositions)
        return "(" + res + ")"
    elif len(propositions) == 1:
        return propositions[0]
    else:
        raise Exception("List of propositions is empty")
