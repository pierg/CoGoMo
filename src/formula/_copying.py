from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from formula import LTL

from copy import deepcopy, copy


def __deepcopy__(self: LTL, memo):
    cls = self.__class__
    result = cls.__new__(cls)
    memo[id(self)] = result
    for k, v in self.__dict__.items():
        if k == "_LTL__cnf":
            if len(v) == 1 and self == next(iter(v)):
                setattr(result, k, {result})
            else:
                setattr(result, k, deepcopy(v))
        elif k == "_LTL__variables":
            """Shallow copy of variables"""
            setattr(result, k, copy(v))
        else:
            setattr(result, k, deepcopy(v))
    return result
