from __future__ import annotations

from enum import Enum, auto
from typing import Set

from specification import Specification
from typeset import Typeset


class FormulaKinds(Enum):
    SENSOR = auto()
    LOCATION = auto()
    ACTION = auto()
    TIME = auto()
    IDENTITY = auto()


class LTL(Specification):
    def __init__(self,
                 formula: str = None,
                 typeset: Typeset = None,
                 cnf: Set[LTL] = None,
                 dnf: Set[LTL] = None,
                 kind: FormulaKinds = None):

        self.__negation = False
        self.__kind = kind

        self.__refinement_rules = None
        self.__mutex_rules = None
        self.__adjacency_rules = None

        self.__base_variables: Typeset = Typeset()

        """Base Case"""
        if formula is not None and formula == "TRUE":
            self.__base_formula: str = "TRUE"
            self.__saturation = None
            self.__context = None
            self.__cnf: Set[LTL] = {self}
            self.__dnf: Set[LTL] = {self}
        else:
            self.__context = LTL("TRUE") if context is None else context
            self.__saturation = LTL("TRUE")

            if formula is not None:
                if formula == "TRUE" or formula == "true":
                    self.__base_formula: str = "TRUE"

                if formula == "FALSE" or formula == "false":
                    self.__base_formula: str = "FALSE"
                else:
                    self.__base_formula: str = formula
                    self.__base_variables: Typeset = variables
                self.__cnf: Set[LTL] = {self}
                self.__dnf: Set[LTL] = {self}

            elif cnf is not None:

                cnf_str = [x.formula(include_rules=False) for x in cnf]

                self.__base_formula: str = And(cnf_str, brackets=True)
                self.__cnf: Set[LTL] = cnf
                for x in cnf:
                    self.__base_variables |= x.variables

            elif dnf is not None:

                dnf_str = [x.formula(include_rules=False) for x in dnf]

                self.__base_formula: str = Or(dnf_str)
                self.__dnf: Set[LTL] = dnf
                for x in dnf:
                    self.__base_variables |= x.variables

            else:
                raise Exception("Wrong parameters LTL construction")

            """Rules derived from typeset and refinement/mutex relations"""
            if self.kind != "refinement_rule" and self.kind != "mutex_rule" and self.kind != "adjacency_rule":
                self.__refinement_rules: Set[LTL] = extract_refinement_rules(self.variables)
                self.__mutex_rules: Set[LTL] = extract_mutex_rules(self.variables)
                self.__adjacency_rules: Set[LTL] = extract_adjacency_rule(self.variables)

            """Check satisfiability"""
            if not skip_checks:
                if not self.is_satisfiable():
                    raise InconsistentException(self, self)