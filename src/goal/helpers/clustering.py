import itertools
from typing import Dict, List, Tuple, Set

from formula import LTL, InconsistentException
from goal import Goal
from goal.helpers.goals import flat_goals


def create_contextual_clusters(goals: Set[Goal],
                               aggregation_type: str) -> Dict[LTL, Set[Goal]]:
    """Returns clusters in the form: Context -> List of goals"""

    """REFINEMENT SETTINGS"""
    """When mapping a goal context to a combination of context C, map if the goal context is satisfiable with C"""
    GOAL_CTX_SAT: bool = False
    """When mapping a goal context to a combination of context C, map if the goal context is smaller than C"""
    GOAL_CTX_SMALLER: bool = False
    """When more context points to the same set of goal take the smaller context"""
    SAVE_SMALLER_CONTEXT: bool = False

    goals = flat_goals(goals)

    """Extract all unique contexts"""
    contexts: Set[LTL] = extract_unique_contexts_from_goals(goals)

    if len(contexts) == 0:
        return {LTL(): goals}

    print("\n\n\n\n" + str(len(goals)) + " GOALS\nCONTEXTS:" + str([str(c) for c in contexts]))

    print("\n\n")

    """Extract the combinations of all contextes and the combination with the negations of all the other contexts"""
    combs_all_contexts, combs_all_contexts_neg = extract_all_combinations_and_negations_from_contexts(contexts)

    combinations = combs_all_contexts_neg if aggregation_type == "MUTEX" else combs_all_contexts

    print("\n\n__ALL_COMBINATIONS_(" + str(
        len(combinations)) + ")___________________________________________________________")
    for c_list in combinations:
        print(*c_list, sep='\t\t\t')

    """Filter from combinations the comb that are satisfiable and if they are then merge them"""
    merged = merge_contexes(combinations)

    print("\n\n__MERGED_____________________________________________________________________")
    print(*merged, sep='\n')

    contexts_list = merged

    context_goals = map_goals_to_contexts(contexts_list, goals, GOAL_CTX_SAT, GOAL_CTX_SMALLER, SAVE_SMALLER_CONTEXT)

    return context_goals


def extract_unique_contexts_from_goals(goals: Set[Goal]) -> Set[LTL]:
    contexts: Set[LTL] = set()
    for goal in goals:
        if not goal.context.is_true():
            contexts.add(goal.context)
    return contexts


def extract_all_combinations_and_negations_from_contexts(contexts: Set[LTL]) \
        -> Tuple[List[List[LTL]], List[List[LTL]]]:
    """Extract the combinations of all contexts"""
    combs_all_contexts: List[List[LTL]] = []

    """Extract the combinations of all contexts with negations"""
    combs_all_contexts_neg: List[List[LTL]] = []

    for i in range(0, len(contexts)):
        combs = itertools.combinations(contexts, i + 1)

        for comb in combs:

            comb_contexts = list(comb)
            comb_contexts_neg = list(comb)

            for ctx in contexts:
                if ctx.formula() not in [n.formula() for n in comb_contexts_neg]:
                    ctx_copy = LTL(formula=ctx.formula(), variables=ctx.variables)
                    ctx_copy.negate()
                    comb_contexts_neg.append(ctx_copy)

            combs_all_contexts.append(comb_contexts)
            combs_all_contexts_neg.append(comb_contexts_neg)

    return combs_all_contexts, combs_all_contexts_neg


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


def map_goals_to_contexts(contexts: Set[LTL], goals: Set[Goal],
                          GOAL_CTX_SAT,
                          GOAL_CTX_SMALLER,
                          SAVE_SMALLER_CONTEXT) -> Dict[LTL, Set[Goal]]:
    """Map each goal to each context """

    goals_non_mapped = set(goals)
    print("\n\nMAPPING " + str(len(goals)) + " GOALS TO " + str(len(contexts)) + " CONTEXTS")
    context_goals: Dict[LTL, Set[Goal]] = {}
    for ctx in contexts:
        """Initializing the set"""
        context_goals[ctx] = set()
        for goal in goals:
            print(ctx)
            print(goal.context)
            if ctx <= goal.context:
                print("Ctx: " + str(ctx) + " \t-->\t Goal_ctx: " + str(goal.context))
                """Add goal to the context"""
                context_goals[ctx].add(goal)
                if goal in goals_non_mapped:
                    goals_non_mapped.remove(goal)
            # """If the goal has no context"""
            # if goal.context is None:
            #     """Add goal to the context"""
            #     context_goals[ctx].add(goal)
            #     if goal in goals_non_mapped:
            #         goals_non_mapped.remove(goal)
            # else:
            #     if GOAL_CTX_SAT:
            #         """Verify that the goal-context is satisfiable with the context"""
            #         if goal.context.is_satisfiable_with(ctx):
            #             print("Goal_ctx (" + goal.name + "): " + str(goal.context) + " \t-->\t Ctx: " + str(ctx))
            #             """Add goal to the context"""
            #             context_goals[ctx].add(goal)
            #             if goal in goals_non_mapped:
            #                 goals_non_mapped.remove(goal)
            #     else:
            #         if GOAL_CTX_SMALLER:
            #             """Verify that the goal is included the context"""
            #             if goal.context <= ctx:
            #                 print("Goal_ctx: " + str(goal.context) + " \t-->\t Ctx: " + str(ctx))
            #                 """Add goal to the context"""
            #                 context_goals[ctx].add(goal)
            #                 if goal in goals_non_mapped:
            #                     goals_non_mapped.remove(goal)
            #         else:
            #             """Verify that the context is included in goal context"""
            #             if ctx <= goal.context:
            #                 print("Ctx: " + str(ctx) + " \t-->\t Goal_ctx: " + str(goal.context))
            #                 """Add goal to the context"""
            #                 context_goals[ctx].add(goal)
            #                 if goal in goals_non_mapped:
            #                     goals_non_mapped.remove(goal)

    """Check all the contexts that point to the same set of goals and take the most abstract one"""
    ctx_removed = []
    context_goals_copy = dict(context_goals)
    for ctxa, goalsa in context_goals_copy.items():

        for ctxb, goalsb in context_goals_copy.items():
            if ctxa.formula() in ctx_removed:
                continue
            if ctxb.formula() in ctx_removed:
                continue
            if ctxa is not ctxb:
                if set(goalsa) == set(goalsb):
                    if ctxa <= ctxb:
                        print(str(ctxa) + "\nINCLUDED IN\n" + str(ctxb))
                        if SAVE_SMALLER_CONTEXT:
                            del context_goals[ctxb]
                            ctx_removed.append(ctxb.formula())
                            print(str(ctxb) + "\nREMOVED")
                        else:
                            del context_goals[ctxa]
                            ctx_removed.append(ctxa.formula())
                            print(str(ctxa) + "\nREMOVED")

    """Check the all the goals have been mapped"""
    if len(goals_non_mapped) > 0:
        print("+++++CAREFUL+++++++")
        for g in goals_non_mapped:
            print(g.name + ": " + str(g.context) + " not mapped to any goal")
        raise Exception("Some goals have not been mapped to the context!")

    print("*** ALL GOAL HAVE BEEN MAPPED TO A CONTEXT ***")

    return context_goals
