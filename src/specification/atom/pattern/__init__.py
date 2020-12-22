from typing import Union, Tuple

from specification.atom import Atom, AtomKind
from typeset import Typeset


class Pattern(Atom):
    """
    General LTL Pattern
    """

    def __init__(self,
                 formula: Tuple[str, Typeset] = None,
                 kind: AtomKind = None):
        if kind is None:
            kind = AtomKind.PATTERN

        super().__init__(
            formula=formula,
            kind=kind)
