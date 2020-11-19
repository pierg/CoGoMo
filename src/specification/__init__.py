from __future__ import annotations
from abc import ABC

from specification.atom import Atom


class Specification(Atom):

    def is_satisfiable(self) -> bool: pass

    def is_valid(self) -> bool: pass

    def __lt__(self, other: LTL): pass

    def __le__(self: LTL, other: LTL): pass

    def __eq__(self, other: LTL): pass

    def __ne__(self, other: LTL): pass

    def __gt__(self, other: LTL): pass

    def __ge__(self, other: LTL): pass

