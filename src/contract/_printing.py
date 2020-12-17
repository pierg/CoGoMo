from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract import Contract


def __str__(self: Contract):
    """Override the print behavior"""
    ret = "\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    ret += '\n  assumption:\t' + str(self.assumptions) + "\n"
    ret += '  guarantee:\t' + str(self.guarantees) + "\n"
    ret += "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"

    return ret