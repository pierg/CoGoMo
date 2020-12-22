from typing import List, Union, Tuple
from specification import Specification
from specification.atom import Atom
from specification.atom.pattern.basic import F
from specification.atom.pattern.robotics import RoboticPattern
from tools.logic import Logic
from type import Boolean
from typeset import Typeset


class CoreMovement(RoboticPattern):
    """Core Movements
    All the variables are locations where there robot can be at a certain time"""

    def __init__(self, formula: Tuple[str, Typeset] = None):
        super().__init__(formula=formula)

    @staticmethod
    def process_input(ls: Union[Atom, Boolean, List[Atom], List[Boolean]]) -> Tuple[Typeset, List[str]]:
        if not isinstance(ls, list):
            ls = [ls]
        for i, elem in enumerate(ls):
            if isinstance(elem, Boolean):
                ls[i] = elem.to_atom()

        new_typeset = ls[0].typeset
        formulae_str = [ls[0].string]
        for l in ls[1:]:
            new_typeset |= l.typeset
            formulae_str.append(l.string)
        return new_typeset, formulae_str
