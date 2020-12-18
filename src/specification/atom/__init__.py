from __future__ import annotations

from typing import Union, Tuple
from enum import Enum, auto
from specification import Specification
from specification.exceptions import NotSatisfiableException
from specification.formula import Formula
from tools.logic import Logic, LogicTuple
from typeset import Typeset


class AtomKind(Enum):
    SENSOR = auto()
    LOCATION = auto()
    ACTION = auto()
    TIME = auto()
    IDENTITY = auto()
    UNDEFINED = auto()


class FormulaType(Enum):
    SATURATED = auto()
    UNSATURATED = auto()

class Atom(Specification):

    def __init__(self,
                 formula: Union[str, Tuple[str, Typeset]] = None,
                 kind: AtomKind = None):
        """Atomic Specification (can be an AP, but also an LTL formula that cannot be broken down, e.g. a Pattern)"""

        if kind is None:
            self.__kind = AtomKind.UNDEFINED

        """Indicates if the formula is negated"""
        self.__negation: bool = False

        """Used for linking guarantees to assumptions"""
        self.__saturation = None

        if formula is None:
            raise AttributeError
        if isinstance(formula, str):
            if formula == "TRUE":
                self.__base_formula: Tuple[str, Typeset] = "TRUE", Typeset()
        else:
            self.__base_formula: Tuple[str, Typeset] = formula

        if not self.is_satisfiable():
            raise NotSatisfiableException

    def formula(self, type: FormulaType = FormulaType.SATURATED) -> (str, Typeset):
        expression, typset = self.__base_formula
        if type == FormulaType.SATURATED:
            if self.__saturation is None:
                expression, typset = self.__base_formula
            else:
                expression, typset = LogicTuple.implies_(self.__saturation.formula(), self.__base_formula)
        if self.negated:
            return Logic.not_(expression), typset
        return expression, typset

    def negate(self):
        self.__negation = not self.negated

    @property
    def unsaturated(self):
        return Atom(self.formula(FormulaType.UNSATURATED), self.kind)

    @property
    def kind(self) -> AtomKind:
        return self.__kind

    @kind.setter
    def kind(self, value: AtomKind):
        self.__kind = value

    @property
    def saturation(self):
        return self.__saturation

    def saturate(self, value: Specification):
        self.__saturation = value

    @property
    def negated(self) -> bool:
        return self.__negation

    def __str__(self):
        return self.formula()[0]

    def __hash__(self):
        return hash(self.__base_formula[0])

    def __and__(self, other: Union[Atom, Formula]) -> Formula:
        """self & other
        Returns a new Specification with the conjunction with other"""
        if not (isinstance(other, Atom) or isinstance(other, Formula)):
            raise AttributeError

        if isinstance(other, Atom):
            other = Formula(atom=other)

        return Formula(atom=self) & other

    def __or__(self, other: Union[Atom, Formula]) -> Formula:
        """self | other
        Returns a new Specification with the disjunction with other"""
        if not (isinstance(other, Atom) or isinstance(other, Formula)):
            raise AttributeError

        if isinstance(other, Atom):
            other = Formula(atom=other)

        return Formula(atom=self) | other

    def __invert__(self) -> Atom:
        """Returns a new Specification with the negation of self"""
        self.__negation = not self.__negation
        return self

    def __rshift__(self, other: Union[Atom, Formula]) -> Formula:
        """>>
        Returns a new Specification that is the result of self -> other (implies)"""
        if not (isinstance(other, Atom) or isinstance(other, Formula)):
            raise AttributeError

        if isinstance(other, Atom):
            other = Formula(atom=other)

        return Formula(atom=self) >> other

    def __lshift__(self, other: Union[Atom, Formula]) -> Formula:
        """<<
        Returns a new Specification that is the result of other -> self (implies)"""
        if not (isinstance(other, Atom) or isinstance(other, Formula)):
            raise AttributeError

        if isinstance(other, Atom):
            other = Formula(atom=other)

        return Formula(atom=self) << other

    def __iand__(self, other: Union[Atom, Formula]) -> Formula:
        """self &= other
        Modifies self with the conjunction with other"""

        return self & other

    def __ior__(self, other: Union[Atom, Formula]) -> Formula:
        """self |= other
        Modifies self with the disjunction with other"""

        return self | other
