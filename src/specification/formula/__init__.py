from __future__ import annotations

import itertools
from copy import deepcopy
from enum import Enum, auto
from typing import Set, Union, Tuple, TYPE_CHECKING

from specification import Specification, FormulaType
from tools.strings.logic import Logic, LogicTuple
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

        if not self.is_satisfiable():
            raise NotSatisfiableException

    @property
    def cnf(self) -> Set[Union[Atom, LTL]]:
        return self.__cnf

    @cnf.setter
    def cnf(self, value: Set[Union[Atom, LTL]]):
        self.__cnf = value

    @property
    def dnf(self) -> Set[Union[Atom, LTL]]:
        return self.__dnf

    @dnf.setter
    def dnf(self, value: Set[Union[Atom, LTL]]):
        self.__dnf = value

    def __hash__(self):
        return hash(self.formula()[0])

    def __str__(self):
        return self.formula()[0]

    def formula(self, formulatype: FormulaType = FormulaType.CNF) -> Tuple[str, Typeset]:
        """Generate the formula"""

        if formulatype == FormulaType.CNF:
            return LogicTuple.and_([elem.formula() for elem in self.cnf], inner_brackets=True, ext_brackets=False)

        if formulatype == FormulaType.DNF:
            return LogicTuple.or_([elem.formula() for elem in self.dnf], inner_brackets=True, ext_brackets=False)

    def __and__(self, other: LTL) -> LTL:
        """self & other
        Returns a new Specification with the conjunction with other"""
        if not isinstance(other, LTL):
            raise AttributeError

        new_ltl = deepcopy(self)

        """Cartesian product between the two dnf"""
        from specification.atom import Atom
        new_ltl.dnf = {Atom(formula=LogicTuple.and_([a.formula(), b.formula()], ext_brackets=False)) for a, b in
                       itertools.product(new_ltl.dnf, other.dnf)}

        new_ltl.cnf.update(other.cnf)

        if not new_ltl.is_satisfiable():
            raise NotSatisfiableException

        return new_ltl

    def __or__(self, other: LTL) -> LTL:
        """self | other
        Returns a new Specification with the disjunction with other"""
        if not isinstance(other, LTL):
            raise AttributeError

        new_ltl = deepcopy(self)

        """Cartesian product between the two dnf"""
        from specification.atom import Atom
        new_ltl.cnf = {Atom(formula=LogicTuple.or_([a.formula(), b.formula()], ext_brackets=False)) for a, b in
                       itertools.product(new_ltl.cnf, other.cnf)}

        new_ltl.dnf.update(other.dnf)

        if not new_ltl.is_satisfiable():
            raise NotSatisfiableException

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
