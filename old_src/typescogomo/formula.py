from copy import deepcopy
from typing import Set, Union, List
from tools.nusmv import check_satisfiability, check_validity
from tools.logic import And, Implies, Not, Or
from old_src.typescogomo.variables import Variables, extract_variable, Boolean


class LTL:

    def __init__(self,
                 formula: str = None,
                 variables: Variables = None,
                 cnf: Set['LTL'] = None,
                 kind: str = None,
                 context: 'LTL' = None,
                 skip_checks: bool = False,
                 ap: bool = False):
        """Basic LTL formula.
        It can be build by a single formula (str) or by a conjunction of other LTL formulae (CNF form)"""

        self.__saturation = None

        if formula is not None and variables is None and cnf is None and ap is True:
            """Atomic Proposition of type 'kind'"""

            self.__formula: str = formula

            variable = Boolean(formula)

            """Setting up the kind of AP typeset"""
            variable.kind = kind

            """Variables present in the formula"""
            self.__variables: Variables = Variables({variable})

            self.__cnf: Set['LTL'] = {self}

            """Adding context"""
            self.__context = None

        elif formula is not None and cnf is None and variables is not None:

            if variables is None:
                variables = extract_variable(str(formula))

            """String representing the LTL"""
            self.__formula: str = formula

            """Variables present in the formula"""
            self.__variables: Variables = variables

            """Set of LTL that conjoined result in the formula"""
            self.__cnf: Set['LTL'] = {self}

            """Adding context"""
            self.__context = context

            if not skip_checks:
                if not self.is_satisfiable():
                    raise InconsistentException(self, self)

        elif cnf is not None and formula is None:

            cnf_str = [x.formula for x in cnf]

            self.__formula: str = And(cnf_str)

            self.__variables: Variables = Variables()

            for x in cnf:
                self.__variables |= x.variables

            self.__cnf: Set[Union['LTL']] = cnf

            """Adding context"""
            self.__context = context

            if not skip_checks and len(cnf) > 1:
                if not self.is_satisfiable():
                    raise InconsistentException(self, self)

        elif cnf is None and formula is None:
            self.__formula: str = "TRUE"
            self.__cnf: Set['LTL'] = {self}
            self.__variables: Variables = Variables()
            self.__context = None

        else:
            raise Exception("Wrong parameters LTL construction")

        if kind is not None:
            self.__kind: str = kind
        else:
            self.__kind: str = ""

    @property
    def formula(self) -> str:
        formula = self.__formula

        """Adding context"""
        if self.__context is not None:
            formula = "G((" + self.__context.formula + ") -> (" + self.__formula + "))"

        """Adding saturation"""
        if self.__saturation is not None and self.__saturation.formula != "TRUE":
            formula = "((" + self.__saturation.formula + ") -> (" + formula + "))"

        return formula

    @property
    def unsaturated(self) -> str:
        formula = self.__formula

        """Adding context"""
        if self.__context is not None:
            formula = "G((" + self.__context.formula + ") -> (" + self.__formula + "))"

        return formula

    @property
    def variables(self) -> Variables:
        if self.__saturation is not None:
            if self.__context is not None:
                return self.__variables | self.__context.variables | self.__saturation.variables
            else:
                return self.__variables | self.__saturation.variables
        else:
            if self.__context is not None:
                return self.__variables | self.__context.variables
            else:
                return self.__variables

    @property
    def objective_variables(self) -> Variables:
        return self.__variables

    @property
    def cnf(self) -> Set['LTL']:
        return self.__cnf

    @property
    def kind(self) -> str:
        return self.__kind

    @property
    def context(self) -> 'LTL':
        return self.__context

    @context.setter
    def context(self, value: 'LTL'):
        self.__context = value
        self.__variables |= value.variables

    @property
    def saturation(self) -> 'LTL':
        return self.__saturation

    @saturation.setter
    def saturation(self, value: 'LTL'):
        self.__saturation = value
        self.__variables |= value.variables

    def remove_kind(self, kind: str):

        for elem in self.cnf:
            if elem.kind == kind:
                self.cnf.remove(elem)

        super().__init__(cnf=self.cnf, skip_checks=True)

    def get_kind(self, kind: str) -> List['LTL']:
        ret = []
        for elem in self.cnf:
            if elem.kind == kind:
                ret.append(elem)
        return ret

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    """Logic Operators"""

    def __iand__(self, other):
        """self &= other
        Modifies self with the conjunction with other"""
        if not isinstance(other, LTL):
            return AttributeError

        if self.context is not None and other.context is not None:
            if self.context != other.context:
                raise DifferentContextException(self.context, other.context)

        if self.context is None and other.context is not None:
            raise DifferentContextException(self.context, other.context)

        """Contexts must be equal"""

        if self.__formula == "TRUE":
            self.__formula = deepcopy(other.formula)
            self.__variables = deepcopy(other.variables)
            self.__cnf = deepcopy(other.cnf)
            return self

        if other.formula == "TRUE":
            return self
        if other.formula == "FALSE":
            self.__formula = "FALSE"
            self.__cnf |= other.cnf
            return self

        self.__formula = And([self.__formula, other.unsaturated])
        self.__variables |= other.variables
        self.__cnf |= other.cnf

        if not self.is_satisfiable():
            raise InconsistentException(self, other)
        return self

    def __ior__(self, other):
        """self |= other
        Modifies self with the disjunction with other"""
        if not isinstance(other, LTL):
            return AttributeError

        if self.__formula == "TRUE":
            return self

        if other.formula == "FALSE":
            return self
        if other.formula == "TRUE":
            self.__formula = "TRUE"
            self.__cnf |= other.cnf
            return self

        self.__formula = Or([self.formula, other.formula])
        self.__variables = Variables(self.variables | other.variables)

        # """TODO: maybe not needed"""
        # if not self.is_satisfiable():
        #     raise InconsistentException(self, other)

        return self

    def __and__(self, other):
        """self & other
        Returns a new LTL with the conjunction with other"""
        if not isinstance(other, LTL):
            return AttributeError

        return LTL(cnf={self, other})

    def __or__(self, other):
        """self | other
        Returns a new LTL with the disjunction with other"""
        if not isinstance(other, LTL):
            return AttributeError

        formula = Or([self.formula, other.formula])
        variables = Variables(self.variables | other.variables)

        return LTL(formula=formula, variables=variables)

    def __invert__(self):
        """Returns a new LTL with the negation of self"""

        formula = Not(self.formula)

        return LTL(formula=formula, variables=self.variables)

    def __rshift__(self, other: 'LTL') -> 'LTL':
        """>> self
        Returns a new LTL that is the result of self -> other (implies)"""
        return LTL(
            formula=Implies(self.formula, other.formula),
            variables=Variables(self.variables | other.variables)
        )

    """Refinement operators"""

    def __lt__(self, other: 'LTL'):
        """Check if the set of behaviours is smaller in the other set of behaviours"""
        if self.formula == other.formula:
            return False
        lt = self <= other
        neq = self != other
        return lt and neq

    def __le__(self, other: 'LTL'):
        if other.is_true():
            return True
        """Check if the set of behaviours is smaller or equal in the other set of behaviours"""
        variables_a = set(self.variables.get_nusmv_names())
        variables_b = set(other.variables.get_nusmv_names())
        if len(variables_b & variables_a) > 0:
            variables = variables_a | variables_b
            return check_validity(list(variables), "((" + self.formula + ") -> (" + other.formula + "))")
        return False

    def __eq__(self, other: 'LTL'):
        """Check if the set of behaviours is equal to the other set of behaviours"""
        if self.formula == other.formula:
            return True
        implied_a = self >= other
        implied_b = self <= other
        return implied_a and implied_b

    def __ne__(self, other: 'LTL'):
        """Check if the set of behaviours is different from the other set of behaviours"""
        return not (self == other)

    def __gt__(self, other: 'LTL'):
        """Check if the set of behaviours is bigger than the other set of behaviours"""
        gt = self >= other
        neq = self != other
        return gt and neq

    def __ge__(self, other: 'LTL'):
        if self.is_true():
            return True
        """Check if the set of behaviours is bigger of equal than the other set of behaviours"""
        variables_a = set(self.variables.get_nusmv_names())
        variables_b = set(other.variables.get_nusmv_names())
        variables = variables_a | variables_b
        return check_validity(list(variables), "((" + other.formula + ") -> (" + self.formula + "))")

    def __hash__(self):
        try:
            return hash(self.__formula)
        except Exception as e:
            raise e

    def copy(self):
        """Return a new LTL which is a copy of self"""
        return self & self

    def negate(self):
        """Modifies the LTL formula with its negation"""
        self.__formula = Not(self.formula)

    def remove(self, element):
        self.cnf.remove(element)

        if len(self.cnf) == 0:
            self.__formula: str = "TRUE"
            self.__cnf: Set['LTL'] = {self}
            self.__variables: Variables = Variables()
            return

        cnf_str = [x.formula for x in self.cnf]

        self.__formula: str = And(cnf_str)
        self.__variables: Variables = Variables()

        variables = set()
        for x in self.cnf:
            variables.add(x.variables)
        self.__variables &= variables

    def is_true(self):
        return self.formula == "TRUE"

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
            self.__and__(other)
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


class InconsistentException(Exception):

    def __init__(self, conj_a: LTL, conj_b: LTL):
        self.conj_a = conj_a
        self.conj_b = conj_b


class DifferentContextException(Exception):

    def __init__(self, ctx_a: LTL, ctx_b: LTL):
        self.ctx_a = ctx_a
        self.ctx_b = ctx_b
