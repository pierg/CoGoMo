from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from specification.contract import Contract


def __str__(self: Contract):
    """Override the print behavior"""
    ret = "\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    ret += '\n  assumptions:\t' + str(self.assumptions) + "\n"
    ret += '  guarantees:\t' + str(self.guarantees) + "\n"
    ret += "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"

    return ret