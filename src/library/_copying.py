from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Library

from copy import deepcopy


def __copy__(self: Library):
    cls = self.__class__
    result = cls.__new__(cls)
    result.__dict__.update(self.__dict__)
    return result


def __deepcopy__(self, memo):
    cls = self.__class__
    result = cls.__new__(cls)
    memo[id(self)] = result
    for k, v in self.__dict__.items():
        setattr(result, k, deepcopy(v))
    return result
