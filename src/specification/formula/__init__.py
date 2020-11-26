from __future__ import annotations

import itertools
from copy import deepcopy
from enum import Enum, auto
from typing import Set, Tuple, TYPE_CHECKING, List

from specification import Specification
from specification.exceptions import NotSatisfiableException
from tools.strings.logic import LogicTuple
from typeset import Typeset

if TYPE_CHECKING:
    from specification.atom import Atom


class FormulaOutput(Enum):
    CNF = auto()
    DNF = auto()


class FormulaKind(Enum):
    OBJECTIVE = auto()
    MUTEXRULE = auto()
    REFINEMENTRULE = auto()
    ADJACENCYRULE = auto()
    UNDEFINED = auto()


class Formula(Specification):
    def __init__(self, atom: Atom = None, kind: FormulaKind = None):

        if kind is None:
            self.__kind = FormulaKind.UNDEFINED

        self.__refinement_rules = None
        self.__mutex_rules = None
        self.__adjacency_rules = None

        self.__saturation = None

        if atom is None:
            self.cnf: List[Set[Atom]] = [{Atom("TRUE")}]
            self.dnf: List[Set[Atom]] = [{Atom("TRUE")}]

        elif atom is not None:
            self.cnf: List[Set[Atom]] = [{atom}]
            self.dnf: List[Set[Atom]] = [{atom}]

        else:
            raise Exception("Wrong parameters LTL construction")

    @property
    def kind(self) -> FormulaKind:
        return self.__kind

    @kind.setter
    def kind(self, value: FormulaKind):
        self.__kind = value

    @property
    def cnf(self) -> List[Set[Atom]]:
        return self.__cnf

    @cnf.setter
    def cnf(self, value: List[Set[Atom]]):
        self.__cnf = value

    @property
    def dnf(self) -> List[Set[Atom]]:
        return self.__dnf

    @dnf.setter
    def dnf(self, value: List[Set[Atom]]):
        self.__dnf = value

    def __str__(self):
        return self.formula()[0]

    def formula(self, formulatype: FormulaOutput = FormulaOutput.CNF) -> Tuple[str, Typeset]:
        """Generate the formula"""

        if formulatype == FormulaOutput.CNF:
            return LogicTuple.and_(
                [LogicTuple.or_([a.formula() for a in atoms], brakets=True) for atoms in self.cnf],
                brackets=False)

        if formulatype == FormulaOutput.DNF:
            return LogicTuple.or_(
                [LogicTuple.and_([a.formula() for a in atoms], brackets=True) for atoms in self.dnf],
                brakets=False)

    def __and__(self, other: Formula) -> Formula:
        """self & other
        Returns a new Specification with the conjunction with other"""
        if not isinstance(other, Formula):
            raise AttributeError

        new_ltl = deepcopy(self)

        """Cartesian product between the two dnf"""
        new_ltl.dnf = [a | b for a, b in itertools.product(new_ltl.dnf, other.dnf)]

        """Append to list if not already there"""
        for other_elem in other.cnf:
            if other_elem not in new_ltl.cnf:
                new_ltl.cnf.append(other_elem)

        if not new_ltl.is_satisfiable():
            raise NotSatisfiableException(self, other)

        return new_ltl

    def __or__(self, other: Formula) -> Formula:
        """self | other
        Returns a new Specification with the disjunction with other"""
        if not isinstance(other, Formula):
            raise AttributeError

        new_ltl = deepcopy(self)

        """Cartesian product between the two dnf"""
        new_ltl.cnf = [a | b for a, b in itertools.product(new_ltl.cnf, other.cnf)]

        """Append to list if not already there"""
        for other_elem in other.dnf:
            if other_elem not in new_ltl.dnf:
                new_ltl.dnf.append(other_elem)

        # if not new_ltl.is_satisfiable():
        #     raise NotSatisfiableException(self, other)

        return new_ltl

    def __invert__(self) -> Formula:
        """Returns a new Specification with the negation of self"""

        new_ltl = deepcopy(self)

        for atoms in new_ltl.cnf:
            for atom in atoms:
                atom.negate()

        """Swap CNF with DNF"""
        new_ltl.cnf, new_ltl.dnf = new_ltl.dnf, new_ltl.cnf

        return new_ltl

    def __rshift__(self, other: Formula) -> Formula:
        """>>
        Returns a new Specification that is the result of self -> other (implies)
        NOT self OR other"""
        if not isinstance(other, Formula):
            raise AttributeError

        new_ltl = ~ self

        return new_ltl | other

    def __lshift__(self, other: Formula) -> Formula:
        """<<
        Returns a new Specification that is the result of other -> self (implies)
        NOT other OR self"""
        if not isinstance(other, Formula):
            raise AttributeError

        new_ltl = ~ other

        return new_ltl | self

    def __iand__(self, other: Formula) -> Formula:
        """self &= other
        Modifies self with the conjunction with other"""
        if not isinstance(other, Formula):
            raise AttributeError

        """Cartesian product between the two dnf"""
        self.dnf = [a | b for a, b in itertools.product(self.dnf, other.dnf)]

        """Append to list if not already there"""
        for other_elem in other.cnf:
            if other_elem not in self.cnf:
                self.cnf.append(other_elem)

        if not self.is_satisfiable():
            raise NotSatisfiableException(self, other)

        return self

    def __ior__(self, other: Formula) -> Formula:
        """self |= other
        Modifies self with the disjunction with other"""
        if not isinstance(other, Formula):
            raise AttributeError

        """Cartesian product between the two dnf"""
        self.cnf = [a | b for a, b in itertools.product(self.cnf, other.cnf)]

        """Append to list if not already there"""
        for other_elem in other.dnf:
            if other_elem not in self.dnf:
                self.dnf.append(other_elem)

        if not self.is_satisfiable():
            raise NotSatisfiableException(self, other)

        return self
