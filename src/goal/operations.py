from contract import Contract
from contract.exceptions import InconsistentContracts, IncompatibleContracts, UnfeasibleContracts
from contract.operations import conjoin_contracts, compose_contracts
from formula import LTL
from . import Goal, Link
from ._copying import deepcopy
from itertools import product, combinations
from typing import List, Dict, Set

from .exceptions import GoalFailException, FailOperations, FailMotivations
from .helpers.clustering import create_contextual_clusters


def conjunction(goals: Set[Goal],
                name: str = None,
                description: str = None,
                check_consistency=True) -> Goal:
    """Conjunction Operations among the goals in 'goals'.
       It returns a new goal"""

    if len(goals) == 1:
        return next(iter(goals))

    # """If any goal is already part of a CGG, then it creates a copy"""
    # for n, goal in enumerate(goals):
    #     if len(goal.parents) > 0:
    #         print(goal.name + " is already part of another CGT. Making a copy of it...")
    #         new_goal = deepcopy(goal)
    #         goals -= goal
    #         goals |= new_goal

    if name is None:
        names = []
        for goal in goals:
            names.append(goal.name)
        names.sort()
        conj_name = ""
        for name in names:
            conj_name += name + "^^"
        name = conj_name[:-2]

    if check_consistency:
        """For each contract pair, checks the consistency of the guarantees
        among the goals that have common assumptions"""
        for pair_of_goals in combinations(goals, r=2):

            for contract_1 in pair_of_goals[0].specification.conjoined_by:

                for contract_2 in pair_of_goals[1].specification.conjoined_by:

                    if contract_1.assumptions.is_satisfiable_with(contract_2.assumptions):

                        if not contract_1.guarantees.is_satisfiable_with(contract_2.guarantees):
                            raise GoalFailException(failed_operation=FailOperations.conjunction,
                                                    faild_motivation=FailMotivations.inconsistent,
                                                    goals_involved_a=[pair_of_goals[0]],
                                                    goals_involved_b=[pair_of_goals[1]])

    print("The conjunction satisfiable.")

    new_contract = conjoin_contracts([goal.specification for goal in goals], check_consistency=False)

    new_goal = Goal(name=name,
                    description=description,
                    specification=new_contract)

    new_goal.add_children(link=Link.CONJUNCTION, goals=goals)

    return new_goal


def composition(goals: Set[Goal],
                name: str = None,
                description: str = None) -> Goal:
    """Returns a new goal that is the result of the composition of 'goals'
    The new goal returned points to a copy of 'goals'"""

    if len(goals) == 1:
        return next(iter(goals))

    contracts: Dict[Goal, List[Contract]] = {}

    if name is None:
        names = []
        for goal in goals:
            names.append(goal.name)
        names.sort()
        comp_name = ""
        for name in names:
            comp_name += name + "||"
        name = comp_name[:-2]

    for goal in goals:
        contracts[goal.name] = goal.specification.conjoined_by

    """Dot products among the contract to perform the compositions of the conjunctions"""
    composition_contracts = (dict(list(zip(contracts, x))) for x in product(*iter(contracts.values())))

    """List of composed contract. Each element of the list is in conjunction"""
    composed_contracts: List[Contract] = []

    for c in composition_contracts:
        contracts: List[Contract] = list(c.values())
        try:
            composed_contract, refined_contract = compose_contracts(contracts)

        except InconsistentContracts as e:
            goals_involved = []
            goals_failed = []
            for goal in goals:
                for contract in goal.specification.conjoined_by:
                    if e.guarantee_1 <= contract.guarantees:
                        goals_involved.append(goal)
                    if e.guarantee_2 >= contract.guarantees:
                        goals_failed.append(goal)
            raise GoalFailException(failed_operation=FailOperations.composition,
                                    faild_motivation=FailMotivations.inconsistent,
                                    goals_involved_a=goals_involved,
                                    goals_involved_b=goals_failed)

        except IncompatibleContracts as e:

            goals_involved = []
            goals_failed = []
            for goal in goals:
                for contract in goal.specification.conjoined_by:
                    if e.assumptions_1 <= contract.assumptions:
                        goals_involved.append(goal)
                    if e.assumptions_2 <= contract.assumptions:
                        goals_failed.append(goal)
            raise GoalFailException(failed_operation=FailOperations.composition,
                                    faild_motivation=FailMotivations.incompatible,
                                    goals_involved_a=goals_involved,
                                    goals_involved_b=goals_failed)

        except UnfeasibleContracts as e:

            goals_involved = []
            goals_failed = []
            for goal in goals:
                for contract in goal.specification.conjoined_by:
                    if e.assumptions <= contract.assumptions:
                        goals_involved.append(goal)
                    if e.guarantees <= contract.assumptions:
                        goals_failed.append(goal)
            raise GoalFailException(failed_operation=FailOperations.composition,
                                    faild_motivation=FailMotivations.unfeasible,
                                    goals_involved_a=goals_involved,
                                    goals_involved_b=goals_failed)

        composed_contracts.append(composed_contract)

    print("The composition is satisfiable.")

    new_contract = conjoin_contracts(composed_contracts, check_consistency=False)

    new_goal = Goal(name=name,
                    description=description,
                    specification=new_contract)

    new_goal.add_children(link=Link.COMPOSITION, goals=set(goals))

    return new_goal


def create_cgt(goals: Set[Goal]) -> Goal:
    """Compose all the set of goals in identified context and conjoin the results"""

    """Dictionary context -> Set[Goal]"""
    context_goals: Dict[LTL, Set[Goal]] = create_contextual_clusters(goals, "MUTEX")

    composed_goals = set()
    for i, (ctx, ctx_goals) in enumerate(context_goals.items()):
        try:
            new_goal = composition(ctx_goals)
            composed_goals.add(new_goal)
            # new_goal.context = ctx
        except GoalFailException as e:
            print("FAILED OPE:\t" + e.failed_operation.name)
            print("FAILED MOT:\t" + e.faild_motivation.name)
            print("GOALS_1:\t" + str([g.name for g in e.goals_involved_a]))
            print("GOALS_2:\t" + str([g.name for g in e.goals_involved_b]))

    """Conjoin the goals across all the mutually exclusive contexts"""
    cgt = conjunction(composed_goals, check_consistency=False)

    return cgt
