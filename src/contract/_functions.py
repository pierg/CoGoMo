from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract import Contract


def propagate_assumptions_from(self: Contract, other: Contract):
    self.assumptions &= other.assumptions