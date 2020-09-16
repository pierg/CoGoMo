from typing import Union

from formula import LTL
from formula.patterns import Pattern
from typeset.types.basic import Boolean


class G(Pattern):
    """Globally"""

    def __init__(self, element: Union[LTL, Boolean]):
        if isinstance(element, Boolean):
            element = element.is_true()

        pattern_formula = "G(" + element.formula + ")"

        super().__init__(formula=pattern_formula, variables=element.variables)


class F(Pattern):
    """Eventually"""

    def __init__(self, element: Union[LTL, Boolean]):
        if isinstance(element, Boolean):
            element = element.is_true()

        pattern_formula = "F(" + element.formula + ")"

        super().__init__(formula=pattern_formula, variables=element.variables)


class GF(Pattern):
    """Globally Eventually"""

    def __init__(self, element: Union[LTL, Boolean]):
        if isinstance(element, Boolean):
            element = element.is_true()

        pattern_formula = "G(F(" + element.formula + "))"

        super().__init__(formula=pattern_formula, variables=element.variables)
