from contract import Contract
from formula import LTL
from typing import List, TypeVar

from variable import Variables, Boolean

LTL_types = TypeVar('LTL_types', bound=LTL)


class BooleanContract(Contract):

    def __init__(self,
                 assumptions_str: List[str],
                 guarantees_str: List[str]):

        assumptions = set()
        guarantees = set()

        for a in assumptions_str:
            assumptions.add(LTL(a, Variables({Boolean(a)})))

        for g in guarantees_str:
            guarantees.add(LTL(g, Variables({Boolean(g)})))

        assumptions = LTL(cnf=assumptions)
        guarantees = LTL(cnf=guarantees)

        super().__init__(assumptions=assumptions,
                         guarantees=guarantees)
