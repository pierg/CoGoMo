from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from goal import Goal

from copy import deepcopy


def __copy__(self: Goal):
    cls = self.__class__
    result = cls.__new__(cls)
    result.__dict__.update(self.__dict__)
    return result


def __deepcopy__(self: Goal, memo):
    cls = self.__class__
    result = cls.__new__(cls)
    memo[id(self)] = result
    for k, v in self.__dict__.items():
        setattr(result, k, deepcopy(v))
    return result


def __hash__(self):
    return hash(self.id) + hash(self.specification)
