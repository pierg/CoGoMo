from __future__ import annotations

import os
import subprocess
import platform
import time
from typing import Tuple
from graphviz import Source

from controller.exceptions import SynthesisTimeout, OutOfMemoryException, UnknownStrixResponse
from tools.logic import Logic

strix_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'bin', 'ubuntu_19_10', 'strix'))


class Controller:

    def __init__(self,
                 source: Source = None):
        self.__source = source

    @property
    def source(self):
        return self.__source

    @staticmethod
    def generate_controller(assumptions: str, guarantees: str, ins: str, outs: str) -> Tuple[bool, str, float]:
        """It returns:
            bool: indicating if a contorller has been synthetised
            str: mealy machine of the controller (if found) or of the counter-example if not found in dot format
            float: indicating the synthesis time"""

        global command, timeout
        try:
            if ins == "":
                strix_specs = Logic.implies_(assumptions, guarantees) + '" --outs="' + outs + '"'
            else:
                strix_specs = Logic.implies_(assumptions, guarantees) + '" --ins="' + ins + '" --outs="' + outs + '"'
            command = ""
            if platform.system() != "Linux":
                docker_command = 'docker run lazkany/strix'
                docker_params = ' -f "' + strix_specs + " --k --dot"
                command = docker_command + docker_params
            else:
                params = ' -k --dot -f "' + strix_specs
                command = strix_path + params
            timeout = 3600
            print("\n\nRUNNING COMMAND:\n\n" + command + "\n\n")
            start_time = time.time()
            result = subprocess.check_output([command], shell=True, timeout=timeout, encoding='UTF-8').split()

        except subprocess.TimeoutExpired:
            raise SynthesisTimeout(command=command, timeout=timeout)
        except Exception as e:
            raise UnknownStrixResponse(command=command, response=e.__str__())

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
            raise UnknownStrixResponse(command=command, response="\n".join(result))
