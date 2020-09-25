from __future__ import annotations
from copy import deepcopy
from typing import Set, Union, List

from formula.exceptions import InconsistentException, DifferentContextException
from formula.helpers import extract_refinement_rules
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

        self.__saturation = LTL("TRUE")

        if kind is not None:
            self.__kind: str = kind
        else:
            self.__kind: str = ""

        self.__refinement_rules: Set[LTL] = set()
        self.__mutex_rules: Set[LTL] = set()

        if context is None:
            self.__context = LTL("TRUE")

        if formula is not None:
            if formula == "TRUE" or formula == "true":
                self.__base_formula: str = "TRUE"
                self.__cnf: Set[LTL] = {self}
                self.__dnf: Set[LTL] = {self}
                self.__variables: Typeset = Typeset()

            elif formula == "FALSE" or formula == "false":
                self.__base_formula: str = "FALSE"
                self.__cnf: Set[LTL] = {self}
                self.__dnf: Set[LTL] = {self}
                self.__variables: Typeset = Typeset()

            else:

                """String representing the LTL"""
                self.__base_formula: str = formula

                """Typeset present in the formula"""
                self.__variables: Typeset = variables

                """Set of LTL that conjoined result in the formula"""
                self.__cnf: Set[LTL] = {self}

        elif cnf is not None:

            cnf_str = [x.formula for x in cnf]

            self.__base_formula: str = And(cnf_str, brackets=True)
            self.__variables: Typeset = Typeset()
            self.__cnf: Set[LTL] = cnf
            for x in cnf:
                self.__variables |= x.variables


        elif dnf is not None:

            dnf_str = [x.formula for x in cnf]

            self.__base_formula: str = Or(dnf_str)
            self.__dnf: Set[LTL] = dnf
            self.__variables: Typeset = Typeset()
            for x in dnf:
                self.__variables |= x.variables


        else:
            raise Exception("Wrong parameters LTL construction")

        """Rules derived from typeset and refinement/mutex relations"""
        if self.__kind != "refinement_rule":
            self.__refinement_rules: Set[LTL] = self.extract_refinement_rules()
        if self.__kind != "mutex_rule":
            self.__mutex_rules: Set[LTL] = self.extract_mutex_rules()

        """Check satisfiability"""
        if not skip_checks:
            if not self.is_satisfiable():
                raise InconsistentException(self, self)

    from ._copying import __deepcopy__, __hash__
    from ._operators import __eq__, __le__, __ge__, __gt__, __lt__, __ne__

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

        formula = Not(self.formula)

        return LTL(formula=formula, variables=self.variables)

    def __rshift__(self, other: Union[LTL, Boolean]) -> LTL:
        """>>
        Returns a new LTL that is the result of self -> other (implies)"""
        if isinstance(other, Boolean):
            other = other.assign_true()
        return LTL(
            formula=Implies(self.formula, other.formula),
            variables=self.variables | other.variables
        )

    def __lshift__(self, other: Union[LTL, Boolean]) -> LTL:
        """<<
        Returns a new LTL that is the result of other -> self (implies)"""
        if isinstance(other, Boolean):
            other = other.assign_true()
        return LTL(
            formula=Implies(other.formula, self.formula),
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
        self.__base_formula = And([self.formula, other.formula])
        self.__variables |= other.variables

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
        self.__base_formula = Or([self.formula, other.formula])
        self.__variables |= other.variables

        if not self.is_satisfiable():
            raise InconsistentException(self, other)
        return self

    @property
    def formula(self) -> str:
        formula = self.__base_formula

        """We add the rules r for both a and g, since the overall contract is the same: 
                (a & r) -> (G(c -> (a->g))) === (r -> a) -> (r -> G(c -> (a->g)))"""

        """Adding saturation"""
        if not self.__saturation.is_true():
            formula = "((" + self.__saturation.formula + ") -> (" + self.__base_formula + "))"

        """Adding context"""
        if not self.__context.is_true():
            formula = "G((" + self.__context.formula + ") -> (" + formula + "))"

        rules = []

        """Adding refinement rules"""
        if len(self.__refinement_rules) > 0:
            for rule in self.__refinement_rules:
                rules.append(rule.formula)

        """Adding mutex rules"""
        if len(self.__mutex_rules) > 0:
            for rule in self.__mutex_rules:
                rules.append(rule.formula)

        if len(rules) > 0:
            rules = And(rules, brackets=True)
            formula = rules + " & " + formula

        return formula

    @property
    def unsaturated(self) -> str:
        formula = self.__base_formula

        """Adding context"""
        if not self.__context.is_true():
            formula = "G((" + self.__context.formula + ") -> (" + self.__base_formula + "))"

        """Adding refinement rules"""
        if len(self.__refinement_rules) > 0:
            rules = []
            for rule in self.__refinement_rules:
                rules.append(rule.formula)
            rules = And(rules, brackets=True)
            formula = rules + " -> " + formula

        """Adding mutex rules"""
        if len(self.__mutex_rules) > 0:
            rules = []
            for rule in self.__mutex_rules:
                rules.append(rule.formula)
            rules = And(rules, brackets=True)
            formula = rules + " -> " + formula

        return formula

    @property
    def variables(self) -> Typeset:
        return self.__variables | self.__context.variables | self.__saturation.variables

    @property
    def objective_variables(self) -> Typeset:
        return self.__variables

    @property
    def cnf(self) -> Set[LTL]:
        return self.__cnf

    @property
    def dnf(self) -> Set[LTL]:
        return self.__dnf

    @property
    def kind(self) -> str:
        return self.__kind

    @property
    def base_formula(self) -> str:
        return self.__base_formula

    @property
    def context(self) -> LTL:
        return self.__context

    @context.setter
    def context(self, value: LTL):
        self.__context = value
        self.__variables |= value.variables

    @property
    def saturation(self) -> LTL:
        return self.__saturation

    @saturation.setter
    def saturation(self, value: LTL):
        self.__saturation = value
        self.__variables |= value.variables

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

    def extract_refinement_rules(self) -> Set[LTL]:
        rules: Set[LTL] = set()

        for variable, supertypes in self.variables.supertypes.items():
            for supertype in supertypes:
                formula = "G(" + variable.name + " -> " + supertype.name + ")"
                rule = LTL(formula=formula, variables=Typeset({variable, supertype}), kind="refinement_rule")
                rules.add(rule)
                self.__variables |= supertype

        return rules

    def extract_mutex_rules(self) -> Set[LTL]:
        rules: Set[LTL] = set()

        for mutextypes in self.variables.mutextypes:
            if len(mutextypes) > 1:
                variables: Typeset = Typeset()
                ltl = "G("
                for vs in mutextypes:
                    variables |= vs
                mutextypes_str = [n.name for n in mutextypes]
                clauses = []
                for vs_a in mutextypes_str:
                    clause = [deepcopy(vs_a)]
                    for vs_b in mutextypes_str:
                        if vs_a is not vs_b:
                            clause.append(Not(deepcopy(vs_b)))
                    clauses.append(And(clause))
                ltl += Or(clauses)
                ltl += ")"
                rules.add(LTL(formula=ltl, variables=variables, kind="mutex_rule"))
        return rules

    def copy(self):
        """Return a new LTL which is a copy of self"""
        return self & self

    def negate(self):
        """Modifies the LTL formula with its negation"""
        self.__base_formula = Not(self.formula)

    def remove(self, element):
        self.cnf.remove(element)

        if len(self.cnf) == 0:
            self.__base_formula: str = "TRUE"
            self.__cnf: Set[LTL] = {self}
            self.__variables: Typeset = Typeset()
            return

        cnf_str = [x.formula for x in self.cnf]

        self.__base_formula: str = And(cnf_str)
        self.__variables: Typeset = Typeset()

        variables = set()
        for x in self.cnf:
            variables.add(x.variables)
        self.__variables &= variables

    def is_true(self):
        return self.formula == "TRUE"

    def is_false(self):
        return self.formula == "FALSE"

    def is_satisfiable(self):
        if self.formula == "TRUE":
            return True
        if self.formula == "FALSE":
            return False
        return check_satisfiability(self.variables.get_nusmv_names(), self.formula)

    def is_satisfiable_with(self, other):
        if self.formula == "TRUE":
            return True
        try:
            self & other
        except InconsistentException:
            return False
        return True

    def can_provide_for(self, other):
        """Check if the set of behaviours is smaller or equal in the other set of behaviours but on the types"""
        variables = self.variables | other.variables
        proposition = Implies(self.formula, other.formula)
        for v in variables:
            proposition = proposition.replace(v.name, v.port_type)
        return check_validity(variables.get_nusmv_types(), proposition)

    def __str__(self):
        return self.formula

    def are_satisfiable_with(self, assumptions):
        pass
