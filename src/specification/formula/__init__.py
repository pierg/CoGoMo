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


class LTL(Specification):
    def __init__(self,
                 atom: Atom = None,
                 kind: FormulaKind = None):

        self._negation = False

        if kind is None:
            self.__kind = FormulaKind.UNDEFINED

        self.__refinement_rules = None
        self.__mutex_rules = None
        self.__adjacency_rules = None

        self.__base_formula = None, None
        self.__saturation = None

        """Base Case"""
        if atom is None:
            if formula is None or formula[0] == "TRUE":
                self.__base_formula: Tuple[str, Typeset] = ("TRUE", Typeset())
            elif formula[0] == "FALSE":
                self.__base_formula: Tuple[str, Typeset] = ("FALSE", Typeset())
            else:
                self.__base_formula: Tuple[str, Typeset] = formula

            self.__cnf: Set[Union[Atom, LTL]] = {self}
            self.__dnf: Set[Union[Atom, LTL]] = {self}

        elif atom is not None:

            self.__base_formula: Tuple[str, Typeset] = atom.formula

            self.__cnf: Set[Union[Atom, LTL]] = {atom}
            self.__dnf: Set[Union[Atom, LTL]] = {atom}

        else:
            raise Exception("Wrong parameters LTL construction")

    @property
    def cnf(self) -> Set[Union[Atom, LTL]]:
        return self.__cnf

    @cnf.setter
    def cnf(self, value: Set[Union[Atom, LTL]]):
        self.cnf = value

    @property
    def dnf(self) -> Set[Union[Atom, LTL]]:
        return self.__dnf

    @dnf.setter
    def dnf(self, value: Set[Union[Atom, LTL]]):
        self.dnf = value

    def formula(self, formulatype: FormulaType = None) -> Tuple[str, Typeset]:
        """Generate the formula"""
        if formulatype is None:
            formulatype = FormulaType.COMPLETE

        if len(self.cnf) == 1 and formulatype == FormulaType.EXPRESSION:
            return self.__base_formula

        expression_l = [e.formula(FormulaType.EXPRESSION)[0] for e in self.cnf]
        variables_l = [e.formula(FormulaType.EXPRESSION)[1] for e in self.cnf]

        expression = Logic.and_(expression_l, brackets=True)
        variables = Typeset()
        for v in variables_l:
            variables |= v

        return expression, variables



    def __and__(self, other: LTL) -> LTL:
        """self & other
        Returns a new Specification with the conjunction with other"""
        if not isinstance(other, LTL):
            raise AttributeError

        if not self.is_satisfiable():
            return deepcopy(self)

        if not other.is_satisfiable():
            return deepcopy(other)

        new_ltl = deepcopy(self)

        new_ltl.cnf |= other

        for e in new_ltl.dnf:
            e &= other

        return new_ltl

    def __or__(self, other: LTL) -> LTL:
        """self | other
        Returns a new Specification with the disjunction with other"""
        if not isinstance(other, LTL):
            raise AttributeError

        if not self.is_satisfiable():
            return deepcopy(self)

        if not other.is_satisfiable():
            return deepcopy(other)

        new_ltl = deepcopy(self)

        new_ltl.dnf |= other

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

        if not self.is_satisfiable():
            return deepcopy(self)

        if not other.is_satisfiable():
            return deepcopy(other)

        self.cnf |= other

        for e in self.dnf:
            e &= other

        return self

    def __ior__(self, other: LTL) -> LTL:
        """self |= other
        Modifies self with the disjunction with other"""
        if not isinstance(other, LTL):
            raise AttributeError

        if not self.is_satisfiable():
            return deepcopy(self)

        if not other.is_satisfiable():
            return deepcopy(other)

        self.dnf |= other

        for e in self.cnf:
            e |= other

        return self
