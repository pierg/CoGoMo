import os
import subprocess
import sys
import platform
import time
from typing import Tuple

from graphviz import Source

from checks.nusmv import check_satisfiability
from checks.tools import Implies
from controller.parser import parse_controller
from helper.tools import save_to_file

strix_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'bin', 'ubuntu_19_10', 'strix'))

output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'clustering'))


class SynthesisException(Exception):
    def __init__(self, reason: str, timeout_value: int = None):

        self.os_not_supported = False
        self.trivial = False
        self.timeout = False
        self.timeout_value = timeout_value

        if reason == "os_not_supported":
            self.os_not_supported = True
        elif reason == "trivial":
            self.trivial = True
        elif reason == "out_of_memory":
            self.out_of_memory = True
        elif reason == "timeout":
            self.timeout = True
        else:
            raise Exception("Unknown exeption: " + reason)


def is_realizable(assumptions: str, guarantees: str, ins: str, outs: str) -> bool:
    try:
        params = ' --realizability -f "' + Implies(assumptions,
                                                   guarantees) + '" --ins="' + ins + '" --outs="' + outs + '"'
        command = strix_path + params
        print("\n\nRUNNING COMMAND:\n\n" + command + "\n\n")
        stdoutdata = subprocess.getoutput(command).splitlines()
        if stdoutdata[0] == "REALIZABLE":
            return True
        if stdoutdata[0] == "UNREALIZABLE":
            return False
        else:
            raise Exception("Unknown strix response: " + stdoutdata[0])
    except Exception as e:
        raise e


def get_controller(assumptions: str, guarantees: str, ins: str, outs: str) -> Tuple[bool, str, float]:
    try:
        print("Formatting TRUE as true for strix")
        assumptions = assumptions.replace("TRUE", "true")
        guarantees = guarantees.replace("TRUE", "true")
        docker_command = 'docker run lazkany/strix'
        docker_params = ' -f "' + Implies(assumptions,
                                          guarantees) + '" --ins="' + ins + '" --outs="' + outs + '"' + " --k --dot"
        params = ' -k --dot -f "' + Implies(assumptions, guarantees) + '" --ins="' + ins + '" --outs="' + outs + '"'
        command = strix_path + params
        print("\n\nRUNNING COMMAND:\n\n" + command + "\n\n")
        start_time = time.time()
        result = []
        timeout = 3600
        try:
            if platform.system() != "Linux":
                print("Launching docker...")
                result = subprocess.check_output([docker_command + docker_params], shell=True, timeout=timeout,
                                                 encoding='UTF-8').split()
            else:
                result = subprocess.check_output([strix_path + params], shell=True, timeout=timeout,
                                                 encoding='UTF-8').split()
        except subprocess.TimeoutExpired:
            print("TIMEOUT for synthesis, more than 100 sec")
            raise SynthesisException("timeout", timeout=timeout)
        except Exception as e:
            print("EXCEPTION OCCURRED:\n" + str(e))
            print("FINISH EXCEPTION\n\n")
            raise SynthesisException("out_of_memory")
        exec_time = time.time() - start_time
        if "REALIZABLE" in result:
            dot_format = ""
            for i, line in enumerate(result):
                if "digraph" not in line:
                    continue
                else:
                    dot_format = "".join(result[i:])
                    break
            return True, dot_format, exec_time
        elif "UNREALIZABLE" in result:
            dot_format = ""
            for i, line in enumerate(result):
                if "digraph" not in line:
                    continue
                else:
                    dot_format = "".join(result[i:])
                    break
            return False, dot_format, exec_time
        else:
            print("\n\nSTRIX RESPONSE:\n\n")
            for l in result:
                print(l)
            raise Exception("Unknown strix response: " + result)
    except Exception as e:
        raise e


def create_controller_if_exists(controller_input_file: str) -> Tuple[bool, str, float]:
    """Return true if controller has been synthesized False otherwise.
    It also return the time needed"""

    if platform.system() != "Linux":
        # print(platform.system() + " is not supported for synthesis")
        # raise SynthesisException("os_not_supported")
        print(platform.system() + " is not supported for synthesis directly. Calling docker image instead...")

    print("controller_input_file: " + controller_input_file)
    a, g, i, o = parse_controller(controller_input_file)

    # variables = [var.strip() + ": boolean" for var in i.split(',')]
    # assumptions_satisfiable = check_satisfiability(variables, a)
    #
    # if not assumptions_satisfiable:
    #     raise SynthesisException("trivial")

    realizable, mealy_machine, exec_time = get_controller(a, g, i, o)

    if realizable:
        print(controller_input_file + " IS REALIZABLE")
        dot_file_path = os.path.dirname(controller_input_file)
        dot_file_name = os.path.splitext(controller_input_file)[0]

        dot_file_name = dot_file_name.replace("specification", "controller")

        save_to_file(mealy_machine, dot_file_name + ".dot")
        print("DOT file generated")

        src = Source(mealy_machine, directory=dot_file_path, filename=dot_file_name, format="eps")
        src.render(cleanup=True)
        print(dot_file_name + ".eps  ->   mealy machine generated")

        return True, mealy_machine, exec_time

    else:
        print(controller_input_file + " IS UNREALIZABLE")
        dot_file_path = os.path.dirname(controller_input_file)
        dot_file_name = os.path.splitext(controller_input_file)[0]

        dot_file_name = dot_file_name.replace("specification", "inverted_controller")

        save_to_file(mealy_machine, dot_file_name + ".dot")
        print("DOT file generated")

        src = Source(mealy_machine, directory=dot_file_path, filename=dot_file_name, format="eps")
        src.render(cleanup=True)
        print(dot_file_name + ".eps  ->   inverted mealy machine generated")

        return False, mealy_machine, exec_time


if __name__ == '__main__':
    controller_file = sys.argv[1]
    file_path = output_path + "/" + sys.argv[1]
    controller_output = create_controller_if_exists(file_path)
