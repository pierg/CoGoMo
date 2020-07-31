import os
import shutil
import sys
from copy import deepcopy
from typing import List

from controller.synthesis import create_controller_if_exists, SynthesisException
from goals.cgtgoal import CGTGoal
from goals.helpers import generate_general_controller_inputs_from_goal, generate_controller_input_text, extract_rules
from goals.operations import create_contextual_clusters, create_cgt, CGTFailException, pretty_cgt_exception, \
    extend_cgt
from helper.tools import save_to_file

from crome_specifications import get_inputs

results_path = os.path.dirname(os.path.abspath(__file__)) + "/output/results"
try:
    shutil.rmtree(results_path)
except:
    pass

sys.path.append(os.path.join(os.getcwd(), os.path.pardir))

ap, rules, goals, library = get_inputs()


def pretty_print_goals(ap: dict, rules: dict, goals: List[CGTGoal]) -> str:
    ret = ""
    for g in goals:
        ret += "name:    \t" + g.name + "\n"
        ret += "context: \t" + str(g.context) + "\n"
        ret += "patterns:\t" + str(g.contracts[0].guarantees.formula) + "\n"
        ret += "\n"
    return ret


def generate_controller_from_cgt(cgt: CGTGoal, folder_path, complete):
    assum, guaran, ins, outs = generate_general_controller_inputs_from_goal(ap, rules, cgt, complete)
    save_to_file(generate_controller_input_text(assum, guaran, ins, outs),
                 folder_path + "specification.txt")

    exec_time = 0.0
    realizable = False
    try:
        controller_generated, exec_time = create_controller_if_exists(folder_path + "specification.txt")
        realizable = controller_generated

    except SynthesisException as e:
        if e.os_not_supported:
            print("Os not supported for synthesis. Only linux can run strix")
        elif e.trivial:
            print("The assumptions are not satisfiable. The controller is trivial.")
            raise Exception("Assumptions unsatisfiable in a CGT is impossible.")

    return realizable, exec_time


def generate_controllers_from_cgt_clustered(cgt: CGTGoal, folder_path, complete):
    realizables = []
    exec_times = []
    """Synthetize the controller for the branches of the CGT"""
    print("\n\nSynthetize the controller for the branches of the CGT composing it with the new context")
    for i, goal in enumerate(cgt.refined_by):
        from helper.buchi import generate_buchi
        sub_folder_path = folder_path + "cluster_" + str(i) + "/"
        generate_buchi(goal.context, sub_folder_path + "context")
        realizable, exec_time = generate_controller_from_cgt(goal, sub_folder_path, complete)
        realizables.append(realizable)
        exec_times.append(exec_time)

    return realizables, exec_times


def run(list_of_goals: List[CGTGoal], result_folder: str):
    """Print List of Goals"""
    for g in list_of_goals:
        print(g)

    rules_dict = extract_rules(rules)

    for k, v in rules_dict.items():
        print(k)
        for elem in v:
            print(elem)

    """Create new mutex clusters and assign them to the goals"""
    context_goals = create_contextual_clusters(list_of_goals, "MUTEX", rules_dict["context"])

    """Create the CGT based on the clusters"""
    try:
        cgt_1 = create_cgt(context_goals, rules_dict)
    except CGTFailException as e:
        print(pretty_cgt_exception(e))
        sys.exit()

    save_to_file(str(cgt_1), result_folder + "/cgt_clusters_mutex/CGT.txt")
    save_to_file(str(cgt_1.print_cgt_CROME()), result_folder + "/cgt_clusters_mutex/CGT_CROME.txt")

    """Try to extent every leaf of the CGT by mapping to the library"""
    try:
        extend_cgt(cgt_1, library, rules_dict)
    except CGTFailException as e:
        print(pretty_cgt_exception(e))
        sys.exit()

    """Generate a controller for each branch of the CGT"""
    realizables_clustered, exec_times_clustered = generate_controllers_from_cgt_clustered(cgt_1,
                                                                                          result_folder + "/cgt_clusters_mutex/",
                                                                                          complete)

    ret = "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    ret += "CGT WITH MUTEX CLUSTERS \t  " + str(sum(realizables_clustered)) + "/" + str(
        len(realizables_clustered)) + " REALIZABLE \n"
    cluster_goals = cgt_1.refined_by
    ret += "FEASIBLE CLUSTERS:\t " + str(len(cluster_goals)) + "/" + str(len(context_goals.keys()))
    for i, goal in enumerate(cluster_goals):
        ret += "\nCLUSTER " + str(i) + "\n"
        ret += "SCENARIO:\t" + str(goal.goal_context_to_show.formula) + "\n-->\t" + str(
            len(goal.refined_by)) + " goals: " + str(
            [g.name for g in goal.refined_by]) + "\n"
        if len(realizables_clustered) > 0:
            if realizables_clustered[i]:
                ret += "REALIZABLE\tMUTEX    \tYES\t\t" + format(exec_times_clustered[i], '.3f') + "sec\n"
            else:
                ret += "REALIZABLE\tMUTEX    \tNO\t\t" + format(exec_times_clustered[i], '.3f') + "sec\n"
    ret += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"

    f = open(summary_file_name, "a+")
    f.write(ret)
    f.close()

    if clusters_origianl:
        """Create the CGT composing the goals without the context"""
        try:
            cgt_2 = create_cgt(context_goals, compose_with_context=False)
        except CGTFailException as e:
            print(pretty_cgt_exception(e))
            sys.exit()

        save_to_file(str(cgt_2), result_folder + "/CGT_with_clusters/CGT.txt")
        save_to_file(str(cgt_2.print_cgt_CROME()), result_folder + "/CGT_with_clusters/CGT_CROME.txt")

        realizables_original, exec_times_original = generate_controllers_from_cgt_clustered(cgt_2,
                                                                                            result_folder + "/CGT_with_clusters/",
                                                                                            complete)

        unrealizable_goals = {}

        ret = "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        ret += "CGT WITH CLUSTERS \t" + str(sum(realizables_original)) + "/" + str(
            len(realizables_original)) + " REALIZABLE\n"
        original_goals = cgt_2.refined_by
        ret += "FEASIBLE CLUSTERS:\t " + str(len(original_goals)) + "/" + str(len(context_goals.keys()))
        for i, goal in enumerate(original_goals):
            ret += "\nCLUSTER " + str(i) + "\n"
            ret += "SCENARIO:\t" + str(goal.goal_context_to_show.formula) + "\n-->\t" + str(
                len(goal.refined_by)) + " goals: " + str(
                [g.name for g in goal.refined_by]) + "\n"
            if len(realizables_original) > 0:
                if realizables_original[i]:
                    ret += "REALIZABLE \tYES\t\t" + format(exec_times_original[i], '.3f') + "sec\n"
                else:
                    ret += "REALIZABLE \tNO\t\t" + format(exec_times_original[i], '.3f') + "sec\n"
                    for g_name in [g.name for g in goal.refined_by]:
                        if g_name in unrealizable_goals.keys():
                            unrealizable_goals[g_name] += 1
                        else:
                            unrealizable_goals[g_name] = 1
        ret += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"

        ret += "\n~~~~~~~~~~'UNSAT-CORE' -  UNREALIZABLE GOALS~~~~~~~~~~~~~~~~\n"
        sorted_unrealizable_goals = sorted(unrealizable_goals.items(), key=lambda x: x[1], reverse=True)
        for (g, v) in sorted_unrealizable_goals:
            ret += g + "\t" + str(v) + "\n"
        ret += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
        f = open(summary_file_name, "a+")
        f.write(ret)
        f.close()

    print("\nClustering process finished. Results generated.")

    return realizable_no_clusters, realizables_clustered, realizables_original, no_clusters_exec_time, exec_times_clustered, exec_times_original


if __name__ == "__main__":
    realizable_no_clusters, realizables_clustered, realizables_original, no_clusters_exec_time, exec_times_clustered, exec_times_original = run(
        list_of_goals=goals,
        result_folder=results_path)
