import os
import shutil
import sys
from typing import List

from controller.synthesis import create_controller_if_exists, SynthesisException
from old_src.goals.cgtgoal import CGTGoal
from old_src.goals import generate_controller_input_text, extract_rules
from old_src.goals import create_contextual_clusters, create_cgt, CGTFailException, pretty_cgt_exception, \
    extend_cgt
from tools.strings_manipulation import save_to_file

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
        ret += "dywer:\t" + str(g.contracts[0].guarantees.formula) + "\n"
        ret += "\n"
    return ret


def generate_controller_from_cgt(cgt: CGTGoal, folder_path):
    assum = []
    guaran = []

    for elem in cgt.get_ltl_assumptions().cnf:
        assum.append(elem.formula)

    guaran.append(cgt.get_ltl_guarantees().formula)
    # for elem in cgt.get_ltl_guarantees().cnf:
    #     guaran.append(elem.formula)

    uncontrollable = []
    controllable = []

    variables = cgt.get_variables()
    for var in variables:
        if var.controllable:
            controllable.append(var.name)
        else:
            uncontrollable.append(var.name)

    save_to_file(generate_controller_input_text(assum, guaran, uncontrollable, controllable),
                 folder_path + "specification.txt")

    exec_time = 0.0
    realizable = False
    mealy_machine = None

    realizable, mealy_machine, exec_time = create_controller_if_exists(folder_path + "specification.txt")

    return realizable, mealy_machine, exec_time


def generate_controllers_for_cgt(cgt: CGTGoal, folder_path):
    """Synthetize the controller for each node of the CGT"""
    list_cgt = cgt.get_all_nodes()
    for i, goal in enumerate(list_cgt):
        sub_folder_path = folder_path + goal.id + "/"
        try:
            realizable, mealy_machine, exec_time = generate_controller_from_cgt(goal, sub_folder_path)

            goal.realizable = realizable
            goal.controller = mealy_machine
            goal.time_synthesis = exec_time

        except SynthesisException as e:
            if e.os_not_supported:
                print("Os not supported for synthesis. Only linux can run strix")
                return
            elif e.trivial:
                print("The assumptions are not satisfiable. The controller is trivial.")
                raise Exception("Assumptions unsatisfiable in a CGT is impossible.")
            elif e.out_of_memory:
                print("STRIX went out of memory")
                goal.realizable = False
                goal.controller = None
                goal.time_synthesis = -200
            elif e.timeout:
                print("timeout occurred")
                goal.realizable = False
                goal.controller = None
                goal.time_synthesis = e.timeout_value


def generate_controllers_from_cgt_clustered(cgt: CGTGoal, folder_path, complete=False):
    realizables = []
    exec_times = []
    """Synthetize the controller for each node of the CGT"""
    print("\n\nSynthetize the controller for each cluster")
    for i, goal in enumerate(cgt.refined_by):
        sub_folder_path = folder_path + "cluster_" + str(i) + "/"
        # generate_buchi(goal.context, sub_folder_path + "context")
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
        cgt = create_cgt(context_goals, rules_dict)
    except CGTFailException as e:
        print(pretty_cgt_exception(e))
        sys.exit()

    save_to_file(str(cgt), result_folder + "/CGT_clustered.txt")
    save_to_file(str(cgt.print_cgt_detailed()), result_folder + "/CGT_clustered_details.txt")


    """Try to extent every leaf of the CGT by mapping to the library"""
    try:
        extend_cgt(cgt, library, rules_dict)
    except CGTFailException as e:
        print(pretty_cgt_exception(e))
        sys.exit()

    save_to_file(str(cgt), result_folder + "/CGT_refined.txt")
    save_to_file(str(cgt.print_cgt_detailed()), result_folder + "/CGT_refined_detailed.txt")

    save_to_file(str(cgt.print_cgt_summary()), result_folder + "/CGT_summary.txt")

    """Generate a controller for each node of the CGT"""
    generate_controllers_for_cgt(cgt, result_folder + "/all_goals/")

    save_to_file(str(cgt.print_cgt_summary()), result_folder + "/CGT_summary.txt")
    save_to_file(str(cgt.pretty_print_cgt_summary()), result_folder + "/CGT_summary_pretty.txt")

    print(cgt)


if __name__ == "__main__":
    run(list_of_goals=goals,
        result_folder=results_path)
