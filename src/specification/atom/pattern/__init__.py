from specification.atom import Atom
from typeset import Typeset


class Pattern(Atom):
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
