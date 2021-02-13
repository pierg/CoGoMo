from typing import List, Union, Tuple
from specification.atom import Atom
from specification.atom.pattern.robotics import RoboticPattern
from type import Boolean
from typeset import Typeset


class Trigger(RoboticPattern):

    def __init__(self, formula: Tuple[str, Typeset] = None):
        super().__init__(formula=formula)

    @staticmethod
    def process_input(pre: Union[Atom, Boolean], post: Union[Atom, Boolean]) -> Tuple[Typeset, str, str]:

        new_typeset = Typeset()

        if isinstance(pre, Boolean):
            new_typeset |= pre
            pre = pre.name
        elif isinstance(pre, Atom):
            new_typeset |= pre.typeset
            pre = pre.string
        else:
            raise AttributeError

        if isinstance(post, Boolean):
            new_typeset |= post
            post = post.name
        elif isinstance(post, Atom):
            new_typeset |= post.typeset
            post = post.string
        else:
            raise AttributeError

        return new_typeset, pre, post
