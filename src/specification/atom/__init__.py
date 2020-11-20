from __future__ import annotations
from specification import Specification
from tools.nuxmv import Nuxmv
from typeset import Typeset


class Atom(Specification):

    def __init__(self,
                 formula: str = None,
                 typeset: Typeset = None):
        """Atomic proposition"""

        if formula is None or typeset is None:
            raise AttributeError

        if len(typeset) != 1:
            raise Exception("Atomic propositions only predicate on one type")

        self.__base_formula: str = formula
        self.__typeset: Typeset = typeset

    @property
    def formula(self) -> (str, Typeset):
        return self.__base_formula, self.__typeset

    def is_satisfiable(self) -> bool:
        return Nuxmv.check_satisfiability(self.formula)
