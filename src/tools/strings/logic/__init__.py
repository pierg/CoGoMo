import re
from typing import List

OPERATORS = r'\+|-|\*|==|<=|>=|<|>|!|\||->|&'
TEMPORAL_OPS = r'^F|^G|^X|^U'

operators = re.compile(OPERATORS)
temporal_ops = re.compile(TEMPORAL_OPS)


class Logic:

    @staticmethod
    def and_(propositions: List[str], brackets: bool = False) -> str:
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
                return f"({conj})"
            else:
                return conj

        elif len(propositions) == 1:
            return propositions[0]
        else:
            raise Exception("List of propositions is empty")

    @staticmethod
    def implies_(prop_1: str, prop_2: str) -> str:
        """Returns an str formula representing the logical IMPLIES of prop_1 and prop_2"""
        return f"(({prop_1}) -> ({prop_2}))"

    @staticmethod
    def not_(prop: str) -> str:
        """Returns an str formula representing the logical NOT of prop"""
        match_operators = bool(re.search(operators, prop))
        match_temporal = bool(re.search(temporal_ops, prop))
        if match_operators or match_temporal:
            return f"!({prop})"
        return "!" + prop

    @staticmethod
    def or_(propositions: List[str]) -> str:
        """Returns an formula formula representing the logical OR of list_propoositions"""
        if len(propositions) > 1:
            if "TRUE" in propositions:
                return "TRUE"
            """Remove all FALSE elements"""
            propositions = list(filter("FALSE".__ne__, propositions))

            res = " | ".join(propositions)
            return f"({res})"
        elif len(propositions) == 1:
            return propositions[0]
        else:
            raise Exception("List of propositions is empty")
