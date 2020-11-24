from __future__ import annotations

from typing import Union, Tuple

from specification import Specification, FormulaType
from specification.formula import LTL
from tools.nuxmv import Nuxmv
from tools.strings.logic import Logic
from typeset import Typeset


class Atom(Specification):

    def __init__(self,
                 formula: Union[str, Tuple[str, Typeset]] = None):
        """Atomic Specification (can be an AP, but also an LTL formula that cannot be broken down, e.g. a Pattern)"""

        if formula is None:
            raise AttributeError
        if isinstance(formula, str):
            if formula == "TRUE":
                self.__base_formula: Tuple[str, Typeset] = "TRUE", Typeset()
        else:
            self.__base_formula: Tuple[str, Typeset] = formula

    def formula(self, formulatype: FormulaType = None) -> (str, Typeset):
        return self.__base_formula

    def __str__(self):
        return self.formula()

    def __hash__(self):
        return hash(self.__base_formula[0])

    def __and__(self, other: Union[Atom, LTL]) -> LTL:
        """self & other
        Returns a new Specification with the conjunction with other"""
        if not (isinstance(other, Atom) or isinstance(other, LTL)):
            raise AttributeError

        if isinstance(other, Atom):
            other = LTL(atom=other)

        return LTL(atom=self) & other

    def __or__(self, other: Union[Atom, LTL]) -> LTL:
        """self | other
        Returns a new Specification with the disjunction with other"""
        if not (isinstance(other, Atom) or isinstance(other, LTL)):
            raise AttributeError

        if isinstance(other, Atom):
            other = LTL(atom=other)

        return LTL(atom=self) | other

    def __invert__(self) -> LTL:
        """Returns a new Specification with the negation of self"""

        return ~ LTL(atom=self)

    def __rshift__(self, other: Union[Atom, LTL]) -> LTL:
        """>>
        Returns a new Specification that is the result of self -> other (implies)"""
        if not (isinstance(other, Atom) or isinstance(other, LTL)):
            raise AttributeError

        if isinstance(other, Atom):
            other = LTL(atom=other)

        return LTL(atom=self) >> other

    def __lshift__(self, other: Union[Atom, LTL]) -> LTL:
        """<<
        Returns a new Specification that is the result of other -> self (implies)"""
        if not (isinstance(other, Atom) or isinstance(other, LTL)):
            raise AttributeError

        if isinstance(other, Atom):
            other = LTL(atom=other)

        return LTL(atom=self) << other

    def __iand__(self, other: Union[Atom, LTL]) -> LTL:
        """self &= other
        Modifies self with the conjunction with other"""

        return self & other

    def __ior__(self, other: Union[Atom, LTL]) -> LTL:
        """self |= other
        Modifies self with the disjunction with other"""

        return self | other
