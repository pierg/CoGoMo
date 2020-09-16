import itertools
import re
from copy import deepcopy
from typing import Union, Dict, List, Tuple
from tools.logic import Not, Or, And, Implies
from controller.parser import parse_controller
from controller.synthesis import create_controller_if_exists
from tools.strings_manipulation import save_to_file
from typescogomo.formula import LTL, InconsistentException
from old_src.typescogomo.variables import Variables
from old_src.goals.cgtgoal import Goal


def context_based_specification_clustering(combinations: List[List[LTL]],
                                           rules: List[LTL],
                                           goals,
                                           KEEP_SMALLER_COMBINATION,
                                           GOAL_CTX_SAT,
                                           GOAL_CTX_SMALLER,
                                           SAVE_SMALLER_CONTEXT):
    """Add constaints to the context combinations"""
    if rules is not None:
        add_constraints_to_all_contexts(combinations, rules, add_to_all=False)

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


def extract_rules(rules: Dict) -> Dict:
    """Translates the rules in LTL formulae and returnes a dictionary of 5 cathegories"""

    """Dictionary to return"""
    rules_ltl = {}

    if "gridworld" in rules:
        rules_ltl["gridworld"] = []
        for elem, adjacent in rules["gridworld"].items():
            ltl = "G("
            ltl += elem.formula + " -> X ("
            ltl += " | ".join([a.formula for a in adjacent])
            ltl += "))"
            variables = Variables()
            variables |= elem.variables
            for a in adjacent:
                variables |= a.variables
            rules_ltl["gridworld"].append(LTL(formula=ltl, variables=variables, kind="gridworld"))

    if "context" in rules:
        rules_ltl["context"] = []
        if "mutex" in rules["context"]:
            for mtx_elements in rules["context"]["mutex"]:
                if len(mtx_elements) > 0:
                    variables: Variables = Variables()
                    ltl = "G("
                    for vs in mtx_elements:
                        variables |= vs.variables
                    mtx_elements_str = [n.formula for n in mtx_elements]
                    clauses = []
                    for vs_a in mtx_elements_str:
                        clause = [deepcopy(vs_a)]
                        for vs_b in mtx_elements_str:
                            if vs_a is not vs_b:
                                clause.append(Not(deepcopy(vs_b)))
                        clauses.append(And(clause))
                    ltl += Or(clauses)
                    ltl += ")"
                    rules_ltl["context"].append(LTL(formula=ltl, variables=variables, kind="context"))

        if "inclusion" in rules["context"]:
            for pre, post in rules["context"]["inclusion"].items():
                variables = Variables()
                variables |= pre.variables | post.variables
                ltl = "G((" + pre.formula + ") -> (" + post.formula + "))"
                rules_ltl["context"].append(LTL(formula=ltl, variables=variables, kind="context"))

    if "context_gridworld" in rules:
        rules_ltl["context_gridworld"] = []
        for pre, post in rules["context_gridworld"].items():
            variables = Variables()
            variables |= pre.variables | post.variables
            ltl = "G((" + pre.formula + ") -> (" + post.formula + "))"
            rules_ltl["context_gridworld"].append(LTL(formula=ltl, variables=variables, kind="context_gridworld"))

    if "constraints" in rules:
        rules_ltl["constraints"] = []
        if "mutex" in rules["constraints"]:
            for mtx_elements in rules["constraints"]["mutex"]:
                if len(mtx_elements) > 0:
                    variables: Variables = Variables()
                    ltl = "G("
                    for vs in mtx_elements:
                        variables |= vs.variables
                    mtx_elements_str = [n.formula for n in mtx_elements]
                    clauses = []
                    for vs_a in mtx_elements_str:
                        clause = [deepcopy(vs_a)]
                        for vs_b in mtx_elements_str:
                            if vs_a is not vs_b:
                                clause.append(Not(deepcopy(vs_b)))
                        clauses.append(And(clause))
                    ltl += Or(clauses)
                    ltl += ")"
                    rules_ltl["constraints"].append(
                        LTL(formula=ltl, variables=variables, kind="constraints"))

        if "inclusion" in rules["constraints"]:
            for pre, post in rules["constraints"]["inclusion"].items():
                variables = Variables()
                variables |= pre.variables | post.variables
                ltl = "G((" + pre.formula + ") -> (" + post.formula + "))"
                rules_ltl["constraints"].append(
                    LTL(formula=ltl, variables=variables, kind="constraints"))

    return rules_ltl


def extract_ltl_rules(context_rules: Dict) -> List[LTL]:
    """Dict:  ltl_formula -> list_of_variables_involved"""

    ltl_list: List[LTL] = []

    if "mutex" in context_rules:
        for cvars in context_rules["mutex"]:
            if len(cvars) > 0:
                variables: Variables = Variables()
                ltl = "G("
                for vs in cvars:
                    variables |= vs.variables
                cvars_str = [n.formula for n in cvars]
                clauses = []
                for vs_a in cvars_str:
                    clause = [deepcopy(vs_a)]
                    for vs_b in cvars_str:
                        if vs_a is not vs_b:
                            clause.append(Not(deepcopy(vs_b)))
                    clauses.append(And(clause))

                ltl += Or(clauses)
                ltl += ")"
                ltl_list.append(LTL(formula=ltl, variables=variables))

    if "inclusion" in context_rules:
        for cvars in context_rules["inclusion"]:
            if len(cvars) > 0:
                variables: Variables = Variables()
                ltl = "G("
                for i, vs in enumerate(cvars):
                    variables |= vs.variables
                    ltl += str(vs)
                    if i < (len(cvars) - 1):
                        ltl += " -> "
                ltl += ")"

                ltl_list.append(LTL(formula=ltl, variables=variables))

    if "liveness" in context_rules:
        for cvars in context_rules["liveness"]:
            variables: Variables = Variables()
            ltl = "G( F("
            variables |= cvars.variables
            ltl += str(cvars)
            ltl += "))"
            ltl_list.append(LTL(formula=ltl, variables=variables))

    return ltl_list


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
                if ctx.formula not in [n.formula for n in comb_contexts_neg]:
                    ctx_copy = deepcopy(ctx)
                    ctx_copy.negate()
                    comb_contexts_neg.append(ctx_copy)

            combs_all_contexts.append(comb_contexts)
            combs_all_contexts_neg.append(comb_contexts_neg)

    return combs_all_contexts, combs_all_contexts_neg


def add_constraints_to_all_contexts(comb_contexts: List[List[LTL]], rules: List[LTL], add_to_all=False):
    if add_to_all:
        """Add all rules to all the combinations"""
        for comb in comb_contexts:
            for rule in rules:
                comb.append(rule)
    else:
        """Add rules only to the combinations that predicate on the rule"""
        for comb in comb_contexts:
            comb_variables = Variables()
            for c in comb:
                comb_variables |= c.variables
            for rule in rules:
                if len(comb_variables & rule.variables) > 0:
                    comb.append(rule)


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
            if ctxa.formula in ctx_removed:
                continue
            if ctxb.formula in ctx_removed:
                continue
            if ctxa is not ctxb:
                if set(goalsa) == set(goalsb):
                    if ctxa <= ctxb:
                        print(str(ctxa) + "\nINCLUDED IN\n" + str(ctxb))
                        if SAVE_SMALLER_CONTEXT:
                            del context_goals[ctxb]
                            ctx_removed.append(ctxb.formula)
                            print(str(ctxb) + "\nREMOVED")
                        else:
                            del context_goals[ctxa]
                            ctx_removed.append(ctxa.formula)
                            print(str(ctxa) + "\nREMOVED")

    """Check the all the goals have been mapped"""
    if len(goals_non_mapped) > 0:
        print("+++++CAREFUL+++++++")
        for g in goals_non_mapped:
            print(g.name + ": " + str(g.context) + " not mapped to any goal")
        raise Exception("Some goals have not been mapped to the context!")

    print("*** ALL GOAL HAVE BEEN MAPPED TO A CONTEXT ***")

    return context_goals


def prioritize_goal(first_priority_goal, second_priority_goal):
    pass
    """
    Makes the assumption of one goal dependent on the satisfiability of the assumptions of the second goal
    """
    variables = []
    stronger_assumptions_list = []

    for contract in first_priority_goal.contracts:
        variables |= contract.variables
        stronger_assumptions_list.append(And(contract.assumptions))

    for contract in second_priority_goal.contracts:
        contract.add_variables(variables)
        contract.add_assumptions(Not(Or(stronger_assumptions_list)))


def generate_general_controller_inputs_from_goal(ap: dict,
                                                 rules: dict,
                                                 goal: Goal,
                                                 complete=True) -> Tuple[
    List[str], List[str], List[str], List[str]]:
    variables = Variables()
    assumptions = []
    guarantees = []

    """Adding A/G from the goal"""
    a = goal.get_ltl_assumptions().formula
    if a != "TRUE":
        assumptions.append(a)
    g = goal.get_ltl_guarantees().formula
    if g != "TRUE":
        guarantees.append(g)
    variables |= goal.get_variables()

    """Adding liveness rules of the environemnt as assumptions"""
    liveness_rules = extract_ltl_rules(rules["environment"])
    for r in liveness_rules:
        variables |= r.variables
        assumptions.append(r.formula)

    """Adding domain rules of the robot as guarantees"""
    domain_rules = extract_ltl_rules(rules["domain"])
    for r in domain_rules:
        variables |= r.variables
        guarantees.append(r.formula)

    """Adding context rules as assumptions if not already included (cgt includes them)"""
    if complete:
        context_rules = extract_ltl_rules(rules["context"])
        for r in context_rules:
            variables |= r.variables
            assumptions.append(r.formula)

    uncontrollable = []
    controllable = []

    """Splitting the variables between uncontrollable and controllable"""
    for v in variables:
        if v.name in ap["s"]:
            uncontrollable.append(v.name)
        else:
            controllable.append(v.name)

    return assumptions, guarantees, uncontrollable, controllable


def syntax_fix(text: str):
    try:
        res = re.sub(r'(!)', '! ', text)
    except Exception as e:
        raise e
    return res


def realize_specification(environment_rules: Dict, system_rules: Dict, system_goals: List[LTL], ap: Dict,
                          folder_path: str):
    assumptions, guarantees, uncontrollable, controllable = generate_controller_specs(environment_rules, system_rules,
                                                                                      system_goals, ap)

    save_to_file(generate_controller_input_text(assumptions, guarantees, uncontrollable, controllable),
                 folder_path + "specification.txt")

    a, g, i, o = parse_controller(folder_path + "specification.txt")

    assumptions = a.replace("TRUE", "true")
    guarantees = g.replace("TRUE", "true")
    params = ' -k --dot -f "' + Implies(assumptions, guarantees) + '" --ins="' + i + '" --outs="' + o + '"'

    save_to_file(params, folder_path + "specification_params.txt")
    return create_controller_if_exists(folder_path + "specification.txt")


def generate_controller_specs(environment_rules: Dict, system_rules: Dict, system_goals: List[LTL], ap: Dict):
    assumptions = []
    for type, formulas in environment_rules.items():
        for formula in formulas:
            assumptions.append(formula.formula)

    guarantees = []
    for type, formulas in system_rules.items():
        for formula in formulas:
            guarantees.append(formula.formula)

    for formula in system_goals:
        guarantees.append(formula.formula)

    uncontrollable = []
    controllable = []

    for elem in ap.values():
        variable = list(elem.variables)[0]
        if variable.controllable():
            controllable.append(variable.name)
        else:
            uncontrollable.append(variable.name)

    return assumptions, guarantees, uncontrollable, controllable


def generate_controller_input_text(assum: List[str], guaran: List[str], ins: List[str], outs: List[str]):
    ret = "ASSUMPTIONS\n\n"
    for p in assum:
        ret += "\t" + syntax_fix(p) + "\n"

    ret += "\n\nGUARANTEES\n\n"
    for p in guaran:
        ret += "\t" + syntax_fix(p) + "\n"

    ret += "\n\nINPUTS\n\n"
    ret += "\t" + ", ".join(ins)

    ret += "\n\nOUTPUTS\n\n"
    ret += "\t" + ", ".join(outs)

    ret += "\n\nEND\n\n"

    return ret
