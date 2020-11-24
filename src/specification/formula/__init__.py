from __future__ import annotations

from copy import deepcopy
from enum import Enum, auto
from typing import Set, Union, Tuple, TYPE_CHECKING

from specification import Specification, FormulaType
from tools.strings.logic import Logic
from typeset import Typeset

if TYPE_CHECKING:
    from specification.atom import Atom


class FormulaKind(Enum):
    SENSOR = auto()
    LOCATION = auto()
    ACTION = auto()
    TIME = auto()
    IDENTITY = auto()
    UNDEFINED = auto()


class NotSatisfiableException(Exception):
    pass


class LTL(Specification):
    def __init__(self, atom: Atom = None, kind: FormulaKind = None):

        self._negation = False

        if kind is None:
            self.__kind = FormulaKind.UNDEFINED

        self.__refinement_rules = None
        self.__mutex_rules = None
        self.__adjacency_rules = None

        self.__saturation = None

        if atom is None:
            self.cnf: Set[Union[Atom, LTL]] = {Atom("TRUE")}
            self.dnf: Set[Union[Atom, LTL]] = {Atom("TRUE")}

        elif atom is not None:
            self.cnf: Set[Union[Atom, LTL]] = {atom}
            self.dnf: Set[Union[Atom, LTL]] = {atom}

        else:
            raise Exception("Wrong parameters LTL construction")

    @property
    def cnf(self) -> Set[Union[Atom, LTL]]:
        return self.__cnf

    @cnf.setter
    def cnf(self, value: Set[Union[Atom, LTL]]):
        self.__cnf = value

        if not self.is_satisfiable():
            raise NotSatisfiableException

    @property
    def dnf(self) -> Set[Union[Atom, LTL]]:
        return self.__dnf

    @dnf.setter
    def dnf(self, value: Set[Union[Atom, LTL]]):
        self.__dnf = value

        if not self.is_satisfiable():
            raise NotSatisfiableException

    def __hash__(self):
        return hash(self.formula()[0])

    def __str__(self):
        return self.formula()[0]

    def formula(self, formulatype: FormulaType = FormulaType.CNF) -> Tuple[str, Typeset]:
        """Generate the formula"""

        if formulatype == FormulaType.CNF:
            if len(self.cnf) == 1:
                element = list(self.cnf)[0]
                if isinstance(element, LTL):
                    return self.formula(formulatype=FormulaType.DNF)
                else:
                    return element.formula()

            formulae = [e.formula() for e in self.cnf]
            expressions = set()
            typeset = Typeset()
            for formula in formulae:
                expressions.add(formula[0])
                typeset |= formula[1]

            return Logic.and_(list(expressions), brackets=True), typeset

        elif formulatype == FormulaType.DNF:
            if len(self.dnf) == 1:
                element = list(self.dnf)[0]
                if isinstance(element, LTL):
                    return self.formula(formulatype=FormulaType.CNF)
                else:
                    return element.formula()

            formulae = [e.formula() for e in self.dnf]
            expressions = set()
            typeset = Typeset()
            for formula in formulae:
                expressions.add(formula[0])
                typeset |= formula[1]

            return Logic.or_(list(expressions)), typeset

    def __and__(self, other: LTL) -> LTL:
        """self & other
        Returns a new Specification with the conjunction with other"""
        if not isinstance(other, LTL):
            raise AttributeError

        new_ltl = deepcopy(self)

        new_ltl.cnf.update(other.cnf)

        if len(new_ltl.dnf) == 1:
            new_ltl.dnf = {new_ltl}
        else:
            for e in new_ltl.dnf:
                e &= other

        return new_ltl

    def __or__(self, other: LTL) -> LTL:
        """self | other
        Returns a new Specification with the disjunction with other"""
        if not isinstance(other, LTL):
            raise AttributeError

        new_ltl = deepcopy(self)

        new_ltl.dnf.update(other.dnf)

        if len(new_ltl.cnf) == 1:
            new_ltl.cnf = {new_ltl}
        else:
            for e in new_ltl.cnf:
                e |= other

        return new_ltl

    def __invert__(self) -> LTL:
        """Returns a new Specification with the negation of self"""

        new_ltl = deepcopy(self)
        new_ltl._negation = not new_ltl._negation

        return new_ltl

    def __rshift__(self, other: LTL) -> LTL:
        """>>
        Returns a new Specification that is the result of self -> other (implies)
        NOT self OR other"""
        if not isinstance(other, LTL):
            raise AttributeError

        new_ltl = ~ self

        return new_ltl | other

    def __lshift__(self, other: LTL) -> LTL:
        """<<
        Returns a new Specification that is the result of other -> self (implies)
        NOT other OR self"""
        if not isinstance(other, LTL):
            raise AttributeError

        new_ltl = ~ other

        return new_ltl | self

    def __iand__(self, other: LTL) -> LTL:
        """self &= other
        Modifies self with the conjunction with other"""
        if not isinstance(other, LTL):
            raise AttributeError

        self.cnf.update(other.cnf)

        if len(self.dnf) == 1:
            self.dnf = {self}
        else:
            for e in self.dnf:
                e &= other

        return self

    def __ior__(self, other: LTL) -> LTL:
        """self |= other
        Modifies self with the disjunction with other"""
        if not isinstance(other, LTL):
            raise AttributeError

        self.dnf.update(other.dnf)

        if len(self.cnf) == 1:
            self.cnf = {self}
        else:
            for e in self.cnf:
                e |= other

        return self
