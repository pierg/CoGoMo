from copy import deepcopy
from typing import List
from contracts.contract import Contract
from typescogomo.formula import LTL


class Specification(object):
    def __init__(self,
                 contracts: List[Contract]):

        self.contracts = contracts

    def set_context(self, context):
        for contract in self.contracts:
            contract.set_context(context)

    @property
    def context(self) -> LTL:
        cgt_context = deepcopy(self.contracts[0].context)
        for c in self.contracts[1:]:
            cgt_context |= c.context
        return cgt_context

    @context.setter
    def context(self, value: LTL):
        for contract in self.contracts:
            contract.set_context(value)
