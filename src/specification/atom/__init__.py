from __future__ import annotations

from specification import Specification
from specification.formula import LTL
from tools.nuxmv import Nuxmv
from tools.strings.logic import Logic
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

    def __gt__(self, other: Atom):
        # TODO
        if not isinstance(other, Atom):
            raise AttributeError

        f1, t1 = self.formula
        f2, t2 = other.formula
        return LTL(
            formula=Logic.implies_(f1, f2),
            typeset=t1 | t2
        )

    def __ge__(self, other: Atom):
        if not isinstance(other, Atom):
            raise AttributeError

        f1, t1 = self.formula
        f2, t2 = other.formula

        return LTL(
            formula=Logic.implies_(f1, f2),
            typeset=t1 | t2
        )