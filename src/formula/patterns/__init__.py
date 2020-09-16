from formula import LTL
from typeset import Typeset


class Pattern(LTL):
    """
    General LTL Pattern
    """

    def __init__(self, formula: str, variables: Typeset, kind=None):
        if kind is None:
            kind = "pattern"

        super().__init__(
            formula=formula,
            variables=variables,
            kind=kind)
