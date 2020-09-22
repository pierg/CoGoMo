from formula import LTL
from variable import Variables


class Pattern(LTL):
    """
    General Pattern Class
    """

    def __init__(self, formula: str, variables: Variables):
        super().__init__(formula=formula, variables=variables, kind="general_pattern")
        self.domain_properties = []


class Globally(Pattern):
    """Globally P"""

    def __init__(self, ltl: LTL):
        variables = Variables()
        variables |= ltl.variables

        pattern_formula = "G(" + ltl.formula + ")"

        super().__init__(pattern_formula, variables)


class Eventually(Pattern):
    """Eventually P"""

    def __init__(self, ltl: LTL):
        variables = Variables()
        variables |= ltl.variables

        pattern_formula = "G(" + ltl.formula + ")"

        super().__init__(pattern_formula, variables)


class InfinitelyOften(Pattern):
    """Globally Eventually P"""

    def __init__(self, ltl: LTL):
        variables = Variables()
        variables |= ltl.variables

        pattern_formula = "G( F(" + ltl.formula + "))"

        super().__init__(pattern_formula, variables)
