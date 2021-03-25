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
                 source: Source = None,
                 mealy_machine: str = None):
        self.source = source
        self.mealy_machine = mealy_machine

    @property
    def source(self) -> Source:
        return self.__source

    @source.setter
    def source(self, value: Source):
        self.__source = value

    @property
    def mealy_machine(self) -> str:
        return self.__mealy_machine

    @mealy_machine.setter
    def mealy_machine(self, value: str):
        print(value)
        self.__mealy_machine = value

    @staticmethod
    def generate_controller(assumptions: str, guarantees: str, ins: str, outs: str) -> Tuple[bool, str, str, float]:
        """It returns:
            bool: indicating if a contorller has been synthetised
            str: mealy machine of the controller (if found) or of the counter-example if not found in dot format
            float: indicating the controller time"""

        global command_dot, timeout
        try:
            if ins == "":
                strix_specs = Logic.implies_(assumptions, guarantees) + '" --outs="' + outs + '"'
            else:
                strix_specs = Logic.implies_(assumptions, guarantees) + '" --ins="' + ins + '" --outs="' + outs + '"'
            command_dot = ""
            if platform.system() != "Linux":
                docker_command = 'docker run lazkany/strix'
                docker_params_dot = ' -f "' + strix_specs + " --k --dot"
                docker_params_kiss = ' -f "' + strix_specs + " --kiss"
                command_dot = docker_command + docker_params_dot
                command_kiss = docker_command + docker_params_kiss
            else:
                params_dot = ' -k --dot -f "' + strix_specs
                params_kiss = ' -k --kiss -f "' + strix_specs
                command_dot = strix_path + params_dot
                command_kiss = strix_path + params_kiss
            timeout = 3600
            print("\n\nRUNNING COMMAND:\n\n" + command_dot + "\n\n")
            start_time = time.time()
            result_dot = subprocess.check_output([command_dot], shell=True, timeout=timeout, encoding='UTF-8').split()
            result_kiss = subprocess.check_output([command_kiss], shell=True, timeout=timeout, encoding='UTF-8').splitlines()

        except subprocess.TimeoutExpired:
            raise SynthesisTimeout(command=command_dot, timeout=timeout)
        except Exception as e:
            raise UnknownStrixResponse(command=command_dot, response=e.__str__())

        exec_time = time.time() - start_time
        dot_format = ""
        kiss_format = ""
        if "REALIZABLE" in result_dot:
            realizable = True
        elif "UNREALIZABLE" in result_dot:
            realizable = False
        else:
            raise UnknownStrixResponse(command=command_dot, response="\n".join(result_dot))
        for i, line in enumerate(result_dot):
            if "digraph" not in line:
                continue
            else:
                dot_format = "".join(result_dot[i:])
                break
        for i, line in enumerate(result_kiss):
            if ".inputs" not in line:
                continue
            else:
                kiss_format = "\n".join(result_kiss[i:])
                break
        return realizable, dot_format, kiss_format, exec_time
