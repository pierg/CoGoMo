from typing import Union
from contract import Contract
from formula import LTL
from typing import TypeVar

LTL_types = TypeVar('LTL_types', bound=LTL)


class Specification(Contract):

    def __init__(self,
                 specification: Union[Contract, LTL_types]):

        if isinstance(specification, Contract):
            super().__init__(assumptions=specification.assumptions,
                             guarantees=specification.guarantees)
        elif isinstance(specification, LTL):
            super().__init__(guarantees=specification)


