from __future__ import annotations

from copy import deepcopy
from typing import Union, Tuple
from specification import Specification
from specification.enums import *
from specification.exceptions import NotSatisfiableException, AtomNotSatisfiableException
from specification.formula import Formula
from tools.logic import Logic, LogicTuple
from typeset import Typeset


class Atom(Specification):

    def __init__(self,
                 formula: Union[str, Tuple[str, Typeset]] = None,
                 kind: AtomKind = None,
                 check: bool = True):
        """Atomic Specification (can be an AP, but also an LTL formula that cannot be broken down, e.g. a Pattern)"""

        if kind is None:
            self.__kind = AtomKind.UNDEFINED
        self.__kind = kind

        if self.__kind == AtomKind.REFINEMENT_RULE or \
                self.__kind == AtomKind.ADJACENCY_RULE or \
                self.__kind == AtomKind.MUTEX_RULE:
            self.__spec_kind = SpecKind.RULE
        else:
            self.__spec_kind = SpecKind.UNDEFINED

        """Indicates if the formula is negated"""
        self.__negation: bool = False

        """Used for linking guarantees to assumptions"""
        self.__saturation = None

        if formula is None:
            raise AttributeError
        if isinstance(formula, str):
            if formula == "TRUE":
                self.__base_formula: Tuple[str, Typeset] = "TRUE", Typeset()
            elif formula == "FALSE":
                self.__base_formula: Tuple[str, Typeset] = "FALSE", Typeset()
        else:
            self.__base_formula: Tuple[str, Typeset] = formula

            if check:
                if not self.is_satisfiable():
                    raise AtomNotSatisfiableException(formula=self.__base_formula)

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

    def contains_rule(self, rule: AtomKind = None):
        if rule is None:
            return (
                    self.kind == AtomKind.MUTEX_RULE or self.kind == AtomKind.REFINEMENT_RULE or self.kind == AtomKind.ADJACENCY_RULE)
        else:
            return self.kind == rule

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
    def spec_kind(self) -> SpecKind:
        return self.__spec_kind

    @spec_kind.setter
    def spec_kind(self, value: SpecKind):
        self.__spec_kind = value

    @property
    def saturation(self):
        return self.__saturation

    def saturate(self, value: Specification):
        self.__saturation = value

    @property
    def negated(self) -> bool:
        return self.__negation

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
        new_formula = deepcopy(self)
        new_formula.__negation = not new_formula.__negation
        return new_formula

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
