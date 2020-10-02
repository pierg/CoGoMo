import itertools
from copy import deepcopy
from typing import List, Tuple, Set
from contract import Contract
from .exceptions import InconsistentContracts, IncompatibleContracts, UnfeasibleContracts


def compose_contracts(contracts: Set[Contract], refined=False) -> Contract:
    """Composition operation among list of contract.
        It returns two contracts: one is the composition (having guarantees G1),
        the other one is the composition + refinement (having guarantees G2) where:
        s1 = (a1 -> g1), s2 = (a2 -> g2)
        G1 = G(c1 -> (a1 -> g1)) & G(c2 -> (a2 -> g2)) which accepts  (!c1 & !c2) | (!c1 & s2) | (!c2 & s1) | (s1 & s2)
        G2 = G((c1 | c2) -> ((a1 -> g1) & (a2 -> g2))) which accepts  (s1 & s2) | (!c1 & !c2)
        """

    if len(contracts) == 1:
        return next(iter(contracts))
    if len(contracts) == 0:
        raise Exception("No contract specified in the composition")

    contracts_list = list(contracts)

    new_contract: Contract = contracts_list[0]

    """Populate the data structure while checking for compatibility and consistency"""
    for contract in contracts_list[1:]:
        try:
            new_contract &= contract
            print(new_contract)
        except InconsistentContracts as e:
            print("Contracts inconsistent")
            print(e.guarantee_1)
            print("unsatisfiable with")
            print(e.guarantee_2)
            raise e
        except IncompatibleContracts as e:
            print("Contracts incompatible")
            print(e.assumptions_1)
            print("unsatisfiable with")
            print(e.assumptions_2)
            raise e
        except UnfeasibleContracts as e:
            print("Contracts unfeasible")
            print(e.assumptions)
            print("unsatisfiable with")
            print(e.guarantees)
            raise e

    print("The composition is compatible, consistent and feasible")

    """For each combination of assumption/guarantees verify if some g_i -> a_i and simplify a_i"""
    a_removed = []
    g_used = []
    # print(new_contract)
    # print("assumptions:")
    # for a in new_contract.assumptions.cnf:
    #     print(a)
    # print("guarantees:")
    # for g in new_contract.guarantees.cnf:
    #     print(g)
    # print("\n\n")
    for (g, a) in list(itertools.product(new_contract.guarantees.cnf, new_contract.assumptions.cnf)):
        if g not in g_used and a not in a_removed:
            print(str(a) + " -> " + str(g))
            if a <= g:
                print("Simplifying assumption " + str(a))
                new_contract.assumptions.remove(a)
                g_used.append(g)
                a_removed.append(a)
    # for a_elem in list(new_contract.assumptions.cnf):
    #     for g_elem in list(new_contract.guarantees.cnf):
    #         if g_elem not in g_used and a_elem not in a_removed:
    #             print(str(g_elem) + " -> " + str(a_elem))
    #             if g_elem <= a_elem:
    #                 print("Simplifying assumption " + str(a_elem))
    #                 new_contract.assumptions.remove(a_elem)
    #                 g_used.append(g_elem)
    #                 a_removed.append(a_elem)

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
