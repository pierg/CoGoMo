from __future__ import annotations
from copy import deepcopy
from typing import Set, Union, List

from formula.exceptions import InconsistentException, DifferentContextException
from formula.helpers import extract_refinement_rules, extract_mutex_rules
from tools.nusmv import check_satisfiability, check_validity
from typeset import Typeset

from tools.logic import And, Implies, Not, Or
from typeset.types.basic import Boolean


class LTL:

    def __init__(self,
                 formula: str = None,
                 variables: Typeset = None,
                 cnf: Set[LTL] = None,
                 dnf: Set[LTL] = None,
                 kind: str = None,
                 context: LTL = None,
                 skip_checks: bool = False):
        """Basic LTL formula.
        It can be build by a single formula (str) or by a conjunction of other LTL formulae (CNF form)"""

        self.__negation = False
        self.__kind = kind
        self.__refinement_rules = None
        self.__mutex_rules = None
        self.__base_variables: Typeset = Typeset()

        """Base Case"""
        if formula is not None and (formula == "TRUE" or formula == "true"):
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
            if self.kind != "refinement_rule":
                self.__refinement_rules: Set[LTL] = extract_refinement_rules(self.variables)
            if self.kind != "mutex_rule":
                self.__mutex_rules: Set[LTL] = extract_mutex_rules(self.variables)

            """Check satisfiability"""
            if not skip_checks:
                if not self.is_satisfiable():
                    raise InconsistentException(self, self)

    from ._operators import __eq__, __le__, __ge__, __gt__, __lt__, __ne__
    from ._copying import __deepcopy__, __hash__

    def __and__(self, other: Union[LTL, Boolean]) -> LTL:
        """self & other
        Returns a new LTL with the conjunction with other"""
        if isinstance(other, Boolean):
            other = other.assign_true()

        return LTL(cnf={self, other})

    def __or__(self, other: Union[LTL, Boolean]) -> LTL:
        """self | other
        Returns a new LTL with the disjunction with other"""
        if isinstance(other, Boolean):
            other = other.assign_true()

        return LTL(dnf={self, other})

    def __invert__(self: LTL) -> LTL:
        """Returns a new LTL with the negation of self"""

        new_LTL = deepcopy(self)
        new_LTL.negate()
        return new_LTL

    def __rshift__(self, other: Union[LTL, Boolean]) -> LTL:
        """>>
        Returns a new LTL that is the result of self -> other (implies)"""
        if isinstance(other, Boolean):
            other = other.assign_true()
        common_refinement_rules = extract_refinement_rules(self.variables | other.variables)
        individual_rules = self.refinement_rules | other.refinement_rules
        common_refinement_rules = common_refinement_rules - individual_rules
        common_rules_str = []
        for rule in common_refinement_rules:
            common_rules_str.append(rule.formula())
        if len(common_rules_str) > 0:
            formula = Implies(And(common_rules_str),
                              Implies(self.formula(include_rules=True), other.formula(include_rules=True)))
        else:
            formula = Implies(self.formula(include_rules=True), other.formula(include_rules=True))
        return LTL(
            formula=formula,
            variables=self.variables | other.variables
        )

    def __lshift__(self, other: Union[LTL, Boolean]) -> LTL:
        """<<
        Returns a new LTL that is the result of other -> self (implies)"""
        if isinstance(other, Boolean):
            other = other.assign_true()
        return LTL(
            formula=Implies(self.formula(include_rules=False), other.formula(include_rules=False)),
            variables=self.variables | other.variables
        )

    def __iand__(self, other: Union[LTL, Boolean]) -> LTL:
        """self &= other
        Modifies self with the conjunction with other"""
        if isinstance(other, Boolean):
            other = other.assign_true()

        if self.is_true() or other.is_false():
            self.__base_formula = deepcopy(other.base_formula)
            self.__context = deepcopy(other.context)
            self.__saturation = deepcopy(other.saturation)
            self.__cnf = deepcopy(other.cnf)
            return self

        if other.is_true() or self.is_false():
            return self

        old_self = deepcopy(self)
        self.__cnf = {old_self, other}
        self.__base_variables = self.variables
        self.__base_formula = And([old_self.formula(include_rules=False), other.formula(include_rules=False)])
        self.__saturation = LTL("true")
        self.__base_variables |= other.variables

        """Rules derived from typeset and refinement/mutex relations"""
        if self.kind != "refinement_rule":
            self.__refinement_rules: Set[LTL] = extract_refinement_rules(self.variables)
        if self.kind != "mutex_rule":
            self.__mutex_rules: Set[LTL] = extract_mutex_rules(self.variables)

        if not self.is_satisfiable():
            raise InconsistentException(self, other)
        return self

    def __ior__(self, other: Union[LTL, Boolean]) -> LTL:
        """self |= other
        Modifies self with the disjunction with other"""
        if isinstance(other, Boolean):
            other = other.assign_true()

        if self.is_false() or other.is_true():
            self.__base_formula = deepcopy(other.base_formula)
            self.__context = deepcopy(other.context)
            self.__saturation = deepcopy(other.saturation)
            self.__cnf = deepcopy(other.cnf)
            return self

        if other.is_false() or self.is_true():
            return self

        old_self = deepcopy(self)
        self.__dnf = {old_self, other}
        self.__base_formula = Or([self.formula(), other.formula()])
        self.__base_variables |= other.variables

        if not self.is_satisfiable():
            raise InconsistentException(self, other)
        return self

    @property
    def kind(self) -> str:
        return self.__kind

    @property
    def saturation(self) -> LTL:
        return self.__saturation

    @property
    def context(self) -> LTL:
        return self.__context

    @property
    def base_formula(self) -> str:
        return self.__base_formula

    @property
    def refinement_rules(self) -> Set[LTL]:
        if self.__refinement_rules is None:
            return set()
        return self.__refinement_rules

    @property
    def mutex_rules(self) -> Set[LTL]:
        if self.__mutex_rules is None:
            return set()
        return self.__mutex_rules

    @property
    def cnf(self) -> Set[LTL]:
        return self.__cnf

    @property
    def dnf(self) -> Set[LTL]:
        return self.__dnf

    @property
    def variables(self) -> Typeset:
        variables = Typeset()
        variables |= self.__base_variables
        if self.__saturation is not None:
            variables |= self.__saturation.variables
        if self.__context is not None:
            variables |= self.__context.variables
        return variables

    @property
    def base_variables(self) -> Typeset:
        return self.__base_variables

    @property
    def unsaturated(self) -> LTL:
        formula = self.__base_formula
        """Adding context"""
        if self.__context is not None and not self.context.is_true():
            formula = "G((" + self.context.formula() + ") -> (" + formula + "))"

        return formula

    def formula(self, include_rules=True) -> str:

        formula = self.__base_formula

        """Adding saturation"""
        if self.__saturation is not None and not self.saturation.is_true():
            formula = "((" + self.saturation.formula() + ") -> (" + self.__base_formula + "))"

        """Adding context"""
        if self.__context is not None and not self.context.is_true():
            formula = "G((" + self.context.formula() + ") -> (" + formula + "))"

        """Adding negation if necessary"""
        if self.__negation:
            formula = Not(formula)

        if include_rules:

            rules = []

            """Adding refinement rules"""
            for rule in self.refinement_rules:
                rules.append(rule.formula())

            """Adding mutex rules"""
            for rule in self.mutex_rules:
                rules.append(rule.formula())

            if len(rules) > 0:
                rules = And(rules, brackets=True)
                formula = rules + " & " + formula

        return formula

    @context.setter
    def context(self, value: LTL):
        self.__context = value

    @saturation.setter
    def saturation(self, value: LTL):
        self.__saturation = value

    @base_formula.setter
    def base_formula(self, value: str):
        self.__base_formula = value

    def update_from_cnf(self):
        """G = (a1 & a2) -> ((a1 -> g1) & (a2 -> g2)) = (a1 & a2 ) -> (g1 & g2)"""
        alt_self_1 = deepcopy(self)
        alt_self_2 = deepcopy(self)
        cnf_str_base = []
        cnf_str_saturated = []
        cnf_variables = Typeset()
        for elem in self.cnf:
            cnf_str_base.append(elem.base_formula)
            cnf_str_saturated.append(elem.formula())
            cnf_variables |= elem.variables
        alt_self_1.base_formula = And(cnf_str_base)
        alt_self_2.base_formula = And(cnf_str_saturated)

        self.__base_variables = cnf_variables

        if alt_self_1 == alt_self_2:
            self.base_formula = alt_self_1.base_formula
        else:
            self.base_formula = alt_self_2.base_formula

    def remove(self, element):
        self.cnf.remove(element)

        if len(self.cnf) == 0:
            self.__base_formula: str = "TRUE"
            self.__cnf: Set[LTL] = {self}
            self.__base_variables: Typeset = Typeset()
            return

        self.update_from_cnf()

    def is_true(self):
        """G(ctx -> sat -> true) == true"""
        return self.__base_formula == "TRUE"

    def is_false(self):
        return self.formula() == "FALSE"

    def is_satisfiable(self):
        if self.formula() == "TRUE":
            return True
        if self.formula() == "FALSE":
            return False
        return check_satisfiability(self.variables.get_nusmv_names(), self.formula())

    def remove_kind(self, kind: str):

        for elem in self.cnf:
            if elem.kind == kind:
                self.cnf.remove(elem)
        super().__init__(cnf=self.cnf, skip_checks=True)

    def get_kind(self, kind: str) -> List[LTL]:
        ret = []
        for elem in self.cnf:
            if elem.kind == kind:
                ret.append(elem)
        return ret

    def is_satisfiable_with(self, other):
        if self.formula() == "TRUE":
            return True
        try:
            self & other
        except InconsistentException:
            return False
        return True

    def can_provide_for(self, other):
        """Check if the set of behaviours is smaller or equal in the other set of behaviours but on the types"""
        variables = self.variables | other.variables
        proposition = Implies(self.formula(), other.formula())
        for v in variables:
            proposition = proposition.replace(v.name, v.port_type)
        return check_validity(variables.get_nusmv_types(), proposition)

    def __str__(self):
        return self.formula()

    def negate(self):
        self.__negation = not self.__negation

    def are_satisfiable_with(self, assumptions):
        pass
