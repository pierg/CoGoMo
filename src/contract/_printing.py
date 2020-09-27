from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract import Contract


def __str__(self: Contract):
    """Override the print behavior"""
    # a = str(self.variables)
    # b = re.sub('\n', '\n\t\t\t', a)
    # print(b)
    ret = '  types:\t' + re.sub('\n', '\n\t\t\t', str(self.variables))
    ret += '\n  assumptions:\t' + str(self.assumptions) + "\n"
    ret += '  guarantees:\t' + str(self.guarantees) + "\n"

    return ret

    #
    # for var in self.variables:
    #     astr += str(var) + ', '
    # astr = astr[:-2] + ' ]\n  assumptions   :\t[ '
    # for assumption in self.assumptions.cnf:
    #     astr += assumption.formula() + ', '
    # astr = astr[:-2] + ' ]\n  guarantees    :\t[ '
    # for guarantee in self.guarantees.cnf:
    #     astr += guarantee.formula() + ', '