from copy import deepcopy
from typing import List, Tuple
from contract import Contract
from .exceptions import InconsistentContracts, IncompatibleContracts, UnfeasibleContracts


def compose_contracts(contracts: List[Contract]) -> Tuple[Contract, Contract]:
    """Composition operation among list of contract.
        It returns two contracts: one is the composition, the other one is the composition + refinement"""

    if len(contracts) == 1:
        return contracts[0], contracts[0]
    if len(contracts) == 0:
        raise Exception("No contract specified in the composition")

    new_contract = deepcopy(contracts[0])

    """Populate the data structure while checking for compatibility and consistency"""
    for contract in contracts[1:]:
        try:
            new_contract &= contract
            print(new_contract)
        except InconsistentContracts as e:
            print("Contracts inconsistent")
            raise e
        except IncompatibleContracts as e:
            print("Contracts incompatible")
            raise e
        except UnfeasibleContracts as e:
            print("Contracts unfeasible")
            raise e

    print("The composition is compatible, consistent and feasible")

    a_removed = []
    g_used = []

    """For each combination of assumption/guarantees verify if some g_i -> a_i and simplify a_i"""
    for a_elem in list(new_contract.assumptions.cnf):
        for g_elem in list(new_contract.guarantees.cnf):
            if g_elem not in g_used and a_elem not in a_removed:
                if g_elem <= a_elem:
                    print("Simplifying assumption " + str(a_elem))
                    new_contract.assumptions.remove(a_elem)
                    g_used.append(g_elem)
                    a_removed.append(a_elem)

    new_contract.composed_by = contracts

    print("Composed contract:")
    print(new_contract)
    return new_contract


def conjoin_contracts(contracts: List[Contract], check_consistency=True) -> Contract:
    """Conjunction operation among list of contract"""

    if len(contracts) == 1:
        return contracts[0]
    if len(contracts) == 0:
        raise Exception("No contract specified in the composition")

    new_contract = deepcopy(contracts[0])

    if check_consistency:
        for contract in contracts[1:]:
            try:
                new_contract |= contract
            except InconsistentContracts as e:
                print("Contracts inconsistent")
                raise e
            except UnfeasibleContracts as e:
                print("Contracts unfeasible")
                raise e

    new_contract.conjoined_by = contracts

    print("The conjunction is compatible, consistent and feasible")
    print("Conjoined contract:")
    print(new_contract)

    return new_contract
