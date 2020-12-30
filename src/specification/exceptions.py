from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from typeset import Typeset

if TYPE_CHECKING:
    from specification.formula import Formula
    from typing import TypeVar

    Formula_types = TypeVar('Formula_types', bound=Formula)


class NotSatisfiableException(Exception):

    def __init__(self, conj_a: Formula, conj_b: Formula):
        self.conj_a = conj_a
        self.conj_b = conj_b


class AtomNotSatisfiableException(Exception):

    def __init__(self, formula: Tuple[str, Typeset]):
        self.formula = formula
