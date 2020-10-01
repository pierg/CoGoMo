import itertools
from typing import Dict, List, Tuple, Set

from formula import LTL, InconsistentException
from goal import Goal
from goal.helpers.goals import flat_goals


def create_contextual_clusters(goals: Set[Goal],
                               aggregation_type: str) -> Dict[LTL, Set[Goal]]:
    """Returns clusters in the form: Context -> List of goals"""

    goals = flat_goals(goals)

    """Extract all unique contexts"""
    contexts: Set[LTL] = extract_unique_contexts_from_goals(goals)

    if len(contexts) == 0:
        return {LTL(): goals}

    print("\n\n\n\n" + str(len(goals)) + " GOALS\nCONTEXTS:" + str([str(c) for c in contexts]))

    print("\n\n")

    """Extract the combinations of all contexts and the combination with the negations of all the other contexts"""
    combs_all_contexts, combs_all_contexts_saturated = extract_all_combinations_and_saturation_from_contexts(contexts)

    combinations = combs_all_contexts_saturated if aggregation_type == "MUTEX" else combs_all_contexts

    print("\n\n__ALL_COMBINATIONS_(" + str(
        len(combinations)) + ")___________________________________________________________")
    for c_list in combinations:
        print(*c_list, sep='\t\t\t')

    """Filter from combinations the comb that are satisfiable and if they are then merge them"""
    merged = merge_contexes(combinations)

    print("\n\n__MERGED_____________________________________________________________________")
    print(*merged, sep='\n')

    contexts_list = merged

    context_goals = map_goals_to_contexts(contexts_list, goals)

    return context_goals


def extract_unique_contexts_from_goals(goals: Set[Goal]) -> Set[LTL]:
    contexts: Set[LTL] = set()
    for goal in goals:
        if not goal.context.is_true():
            contexts.add(goal.context)
    return contexts


def extract_all_combinations_and_saturation_from_contexts(contexts: Set[LTL]) \
        -> Tuple[List[List[LTL]], List[List[LTL]]]:
    """Extract the combinations of all contexts"""
    combs_all_contexts: List[List[LTL]] = []

    """Extract the combinations of all contexts with negations"""
    combs_all_contexts_saturated: List[List[LTL]] = []

    for i in range(0, len(contexts)):
        combs = itertools.combinations(contexts, i + 1)

        for comb in combs:

            comb_contexts = list(comb)
            comb_contexts_saturated = list(comb)

            for ctx in contexts:
                if ctx.formula() not in [n.formula() for n in comb_contexts_saturated]:
                    ctx_copy = LTL(formula=ctx.formula(), variables=ctx.variables)
                    ctx_copy.negate()
                    comb_contexts_saturated.append(ctx_copy)

            combs_all_contexts.append(comb_contexts)
            combs_all_contexts_saturated.append(comb_contexts_saturated)

    return combs_all_contexts, combs_all_contexts_saturated


def merge_contexes(contexts: List[List[LTL]]) -> Set[LTL]:
    """Merge the consistent contexts with conjunction"""
    contexts_merged: Set[LTL] = set()

    print("\n\nMERGING " + str(len(contexts)) + " CONTEXTS...")

    for group in contexts:
        if len(group) > 0:
            """Extract formulas and check satisfiability, it also filters and simplify each context"""
            try:
                conj = LTL(cnf=set(group))
            except InconsistentException:
                continue
            contexts_merged.add(conj)
    return contexts_merged


def map_goals_to_contexts(contexts: Set[LTL], goals: Set[Goal]) -> Dict[LTL, Set[Goal]]:
    """Map each goal to each context """

    goals_non_mapped = set(goals)
    print("\n\nMAPPING " + str(len(goals)) + " GOALS TO " + str(len(contexts)) + " CONTEXTS")
    context_goals: Dict[LTL, Set[Goal]] = {}
    for ctx in contexts:
        """Initializing the set"""
        context_goals[ctx] = set()
        for goal in goals:
            if ctx <= goal.context:
                print("Ctx: " + str(ctx) + " \t-->\t Goal_ctx: " + str(goal.context))
                """Add goal to the context"""
                context_goals[ctx].add(goal)
                if goal in goals_non_mapped:
                    goals_non_mapped.remove(goal)

    """Check all the contexts that point to the same set of goals and take the most abstract one"""
    for ctx_a, ctx_b in itertools.combinations(context_goals.keys(), 2):
        if ctx_a in context_goals and ctx_b in context_goals:
            if context_goals[ctx_a] == context_goals[ctx_b]:
                if ctx_a >= ctx_b:
                    del context_goals[ctx_b]

    """Check the all the goals have been mapped"""
    if len(goals_non_mapped) > 0:
        print("+++++CAREFUL+++++++")
        for g in goals_non_mapped:
            print(g.name + ": " + str(g.context) + " not mapped to any goal")
        raise Exception("Some goals have not been mapped to the context!")

    print("*** ALL GOAL HAVE BEEN MAPPED TO A CONTEXT ***")

    return context_goals
