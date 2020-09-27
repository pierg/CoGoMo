import itertools
from typing import Union, Dict, List, Tuple
from goal import Goal
from typescogomo.formula() import LTL, InconsistentException


def create_contextual_clusters(goals: List[Goal],
                               aggregation_type: str) -> Dict[LTL, List[Goal]]:
    """Returns clusters in the form: Context -> List of goals"""

    if aggregation_type == "MINIMAL":
        """LTL Creation"""
        "Among a pair of context combinations (two rows), save only the smaller context"
        KEEP_SMALLER_COMBINATION: bool = True
        """Goal Mapping"""
        """When mapping a goal context to a combination of context C, map if the goal context is satisfiable with C"""
        GOAL_CTX_SAT: bool = False
        """When mapping a goal context to a combination of context C, map if the goal context is smaller than C"""
        GOAL_CTX_SMALLER: bool = False
        """When more context points to the same set of goal take the smaller context"""
        SAVE_SMALLER_CONTEXT: bool = False

    elif aggregation_type == "MUTEX":
        """LTL Creation"""
        """Among a pair of context combinations (two rows), save only the smaller context"""
        KEEP_SMALLER_COMBINATION = False
        """Goal Mapping"""
        """When mapping a goal context to a combination of context C, map if the goal context is satisfiable with C"""
        GOAL_CTX_SAT: bool = False
        """When mapping a goal context to a combination of context C, map if the goal context is smaller than C"""
        GOAL_CTX_SMALLER: bool = False
        """When more context points to the same set of goal take the smaller context"""
        SAVE_SMALLER_CONTEXT: bool = False
    else:
        raise Exception("The type is not supported, either MINIMAL or MUTEX")

    goals_flat = []
    """Extract goals that are already conjoined by the designer"""
    for goal in goals:
        if goal.children is not None and all(link == "CONJUNCTION" for link in goal.children.values()):
            goals_flat.extend(goal.children.keys())
        else:
            goals_flat.append(goal)

    goals = goals_flat

    """Extract all unique contexts"""
    contexts: List[LTL] = extract_unique_contexts_from_goals(goals)

    if len(contexts) == 0:
        return {LTL(): goals}

    print("\n\n\n\n" + str(len(goals)) + " GOALS\nCONTEXTS:" + str([str(c) for c in contexts]))

    print("\n\n")

    """Extract the combinations of all contextes and the combination with the negations of all the other contexts"""
    combs_all_contexts, combs_all_contexts_neg = extract_all_combinations_and_negations_from_contexts(contexts)

    context_goals = {}

    if aggregation_type == "MINIMAL":
        context_goals = context_based_specification_clustering(combs_all_contexts, goals,
                                                               KEEP_SMALLER_COMBINATION,
                                                               GOAL_CTX_SAT,
                                                               GOAL_CTX_SMALLER,
                                                               SAVE_SMALLER_CONTEXT)

    if aggregation_type == "MUTEX":
        context_goals = context_based_specification_clustering(combs_all_contexts_neg, goals,
                                                               KEEP_SMALLER_COMBINATION,
                                                               GOAL_CTX_SAT,
                                                               GOAL_CTX_SMALLER,
                                                               SAVE_SMALLER_CONTEXT)

    return context_goals


def context_based_specification_clustering(combinations: List[List[LTL]],
                                           goals,
                                           KEEP_SMALLER_COMBINATION,
                                           GOAL_CTX_SAT,
                                           GOAL_CTX_SMALLER,
                                           SAVE_SMALLER_CONTEXT):
    # """Add constaints to the context combinations"""
    # if rules is not None:
    #     add_constraints_to_all_contexts(combinations, rules, add_to_all=False)

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


def find_goal_with_name(name: str, goals: Union[Dict[Goal, List[Goal]], List[Goal]]):
    """Search for an existing goal"""
    if isinstance(goals, dict):
        for goal_1, goal_2 in goals.items():
            if goal_1.name == name:
                return goal_1
            for g in goal_2:
                if g.name == name:
                    return g

    elif isinstance(goals, list):
        for goal in goals:
            if goal.name == name:
                return goal


def extract_unique_contexts_from_goals(goals: List[Goal]) -> List[LTL]:
    contexts: List[LTL] = []
    for goal in goals:
        if goal.context is not None:
            already_there = False
            for c in contexts:
                if c == goal.context:
                    already_there = True
            if not already_there:
                contexts.append(goal.context)
    return contexts


def extract_all_combinations_and_negations_from_contexts(contexts: List[LTL]) \
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



# def add_constraints_to_all_contexts(comb_contexts: List[List[LTL]], rules: List[LTL], add_to_all=False):
#     if add_to_all:
#         """Add all rules to all the combinations"""
#         for comb in comb_contexts:
#             for rule in rules:
#                 comb.append(rule)
#     else:
#         """Add rules only to the combinations that predicate on the rule"""
#         for comb in comb_contexts:
#             comb_variables = Tyepset()
#             for c in comb:
#                 comb_variables |= c.variables
#             for rule in rules:
#                 if len(comb_variables & rule.variables) > 0:
#                     comb.append(rule)


def merge_contexes(contexts: List[List[LTL]]) -> List[LTL]:
    """Merge the consistent contexts with conjunction"""
    contexts_merged: List[LTL] = []

    print("\n\nMERGING " + str(len(contexts)) + " CONTEXTS...")

    for group in contexts:
        if len(group) > 0:
            """Extract formulas and check satisfiability, it also filters and simplify each context"""
            try:
                conj = LTL(cnf=set(group))
            except InconsistentException:
                continue

            contexts_merged.append(conj)

    return contexts_merged


def map_goals_to_contexts(contexts: List[LTL], goals: List[Goal],
                          GOAL_CTX_SAT,
                          GOAL_CTX_SMALLER,
                          SAVE_SMALLER_CONTEXT) -> Dict[LTL, List[Goal]]:
    """Map each goal to each context """

    goals_non_mapped = list(goals)
    print("\n\nMAPPING " + str(len(goals)) + " GOALS TO " + str(len(contexts)) + " CONTEXTS")
    context_goals: Dict[LTL, List[Goal]] = {}
    for ctx in contexts:
        for goal in goals:
            """If the goal has no context"""
            if goal.context is None:
                """Add goal to the context"""
                if ctx in context_goals:
                    if goal not in context_goals[ctx]:
                        context_goals[ctx].append(goal)
                else:
                    context_goals[ctx] = [goal]
                if goal in goals_non_mapped:
                    goals_non_mapped.remove(goal)
            else:
                # goal_ctxs = goal.context
                goal_ctx = goal.context
                if GOAL_CTX_SAT:
                    """Verify that the goal-context is satisfiable with the context"""
                    if goal_ctx.is_satisfiable_with(ctx):
                        print("Goal_ctx (" + goal.name + "): " + str(goal_ctx) + " \t-->\t Ctx: " + str(ctx))
                        """Add goal to the context"""
                        if ctx in context_goals:
                            if goal not in context_goals[ctx]:
                                context_goals[ctx].append(goal)
                        else:
                            context_goals[ctx] = [goal]
                        if goal in goals_non_mapped:
                            goals_non_mapped.remove(goal)
                else:
                    if GOAL_CTX_SMALLER:
                        """Verify that the goal is included the context"""
                        if goal_ctx <= ctx:
                            print("Goal_ctx: " + str(goal_ctx) + " \t-->\t Ctx: " + str(ctx))
                            """Add goal to the context"""
                            if ctx in context_goals:
                                if goal not in context_goals[ctx]:
                                    context_goals[ctx].append(goal)
                            else:
                                context_goals[ctx] = [goal]
                            if goal in goals_non_mapped:
                                goals_non_mapped.remove(goal)
                    else:
                        """Verify that the context is included in goal context"""
                        if ctx <= goal_ctx:
                            print("Ctx: " + str(ctx) + " \t-->\t Goal_ctx: " + str(goal_ctx))
                            """Add goal to the context"""
                            if ctx in context_goals:
                                if goal not in context_goals[ctx]:
                                    context_goals[ctx].append(goal)
                            else:
                                context_goals[ctx] = [goal]
                            if goal in goals_non_mapped:
                                goals_non_mapped.remove(goal)

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
