from typing import Union
from specification.atom import Specification
from specification.atom.pattern import Pattern
from type import Boolean


class Init(Pattern):
    """Initial Position"""

    def __init__(self, element: Union[Specification, Boolean]):
        if isinstance(element, Boolean):
            element = element.to_atom()

        formula_str = f"{element.formula()[0]}"

        super().__init__(
            formula=(formula_str, element.formula()[1]))


class G(Pattern):
    """Globally"""

    def __init__(self, element: Union[Specification, Boolean]):
        if isinstance(element, Boolean):
            element = element.to_atom()

        formula_str = f"G {element.formula()[0]}"

        super().__init__(
            formula=(formula_str, element.formula()[1]))


class F(Pattern):
    """Eventually"""

    def __init__(self, element: Union[Specification, Boolean]):
        if isinstance(element, Boolean):
            element = element.to_atom()

        formula_str = f"F {element.formula()[0]}"

        super().__init__(
            formula=(formula_str, element.formula()[1]))


class X(Pattern):
    """Next"""

    def __init__(self, element: Union[Specification, Boolean]):
        if isinstance(element, Boolean):
            element = element.to_atom()

        formula_str = f"X {element.formula()[0]}"

        super().__init__(
            formula=(formula_str, element.formula()[1]))


class GF(Pattern):
    """Globally Eventually"""

    def __init__(self, element: Union[Specification, Boolean]):
        if isinstance(element, Boolean):
            element = element.to_atom()

        formula_str = f"GF {element.formula()[0]}"

        super().__init__(
            formula=(formula_str, element.formula()[1]))


class U(Pattern):
    """Until Pattern"""

    def __init__(self, pre: Union[Specification, Boolean], post: Union[Specification, Boolean]):
        if isinstance(pre, Boolean):
            pre = pre.to_atom()
        if isinstance(post, Boolean):
            post = post.to_atom()

        formula_str = f"({pre.formula()[0]} U {post.formula()[0]})"

        super().__init__(
            formula=(formula_str, pre.formula()[1] | post.formula()[1]))


class W(Pattern):
    """Weak Until Pattern"""

    def __init__(self, pre: Union[Specification, Boolean], post: Union[Specification, Boolean]):
        if isinstance(pre, Boolean):
            pre = pre.to_atom()
        if isinstance(post, Boolean):
            post = post.to_atom()

        formula_str = f"(({pre.formula()[0]} U {post.formula()[0]}) | G{pre.formula()[0]})"

        super().__init__(
            formula=(formula_str, pre.formula()[1] | post.formula()[1]))
