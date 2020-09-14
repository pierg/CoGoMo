from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract import Contract


def __str__(self: Contract):
    """Override the print behavior"""
    astr = '  variables:\t[ '
    for var in self.variables:
        astr += str(var) + ', '
    astr = astr[:-2] + ' ]\n  assumptions      :\t[ '
    for assumption in self.assumptions.cnf:
        astr += assumption.formula + ', '
    astr = astr[:-2] + ' ]\n  guarantees       :\t[ '
    for guarantee in self.guarantees.cnf:
        astr += guarantee.formula + ', '
    return astr[:-2] + ' ]\n'
