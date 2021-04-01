from __future__ import annotations
from tabulate import tabulate
import os
import subprocess
import platform
import time
from typing import Tuple, List, Dict
from graphviz import Source

from controller.exceptions import SynthesisTimeout, OutOfMemoryException, UnknownStrixResponse
from specification.atom import Atom
from tools.logic import Logic
from tools.strings import StringMng
from type import Boolean
from worlds import World

strix_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'bin', 'ubuntu_19_10', 'strix'))


class Controller:

    def __init__(self,
                 mealy_machine: str,
                 world: World):

        self.world = world
        self.mealy_machine = mealy_machine

    def __str__(self):
        output = f"States          \t {', '.join(self.states)}" + \
                 f"\nInital State    \t {self.initial_state}" + \
                 f"\nInput  Alphabet \t {', '.join([str(x) for x in self.input_alphabet])}" + \
                 f"\nOutput Alphabet \t {', '.join([str(x) for x in self.output_alphabet])}\n\n"

        headers = ["true_ins", "s", "s'", "true_outs"]
        entries = []
        for (inputs, state), (next_state, outputs) in self.transitions.items():
            line = []
            inputs_str = []
            for x in inputs:
                if x.dontcare:
                    inputs_str.append("-")
                elif not x.negated:
                    inputs_str.append(str(x))
            line.append(' '.join(inputs_str))
            line.append(state)
            line.append(next_state)
            outputs_str = []
            for alternatives in outputs:
                alternatives_str = []
                for x in alternatives:
                    if not x.negated and not x.dontcare:
                        alternatives_str.append(str(x))
                outputs_str.append(' '.join(alternatives_str))
            line.append(' | '.join(outputs_str))
            entries.append(line)

        output += tabulate(entries, headers=headers)

        return output

    @property
    def world(self) -> World:
        return self.__world

    @world.setter
    def world(self, value: World):
        self.__world = value

    @property
    def mealy_machine(self) -> str:
        return self.__mealy_machine

    def react(self, inputs: Tuple[Atom]) -> Tuple[Tuple[Atom]]:
        """Take a reaction in the mealy machine"""
        (next_state, outputs) = self.__transitions[(inputs, self.__current_state)]
        self.__current_state = next_state
        return outputs

    def reset(self):
        """Reset mealy machine"""
        self.__current_state = self.__initial_state

    @mealy_machine.setter
    def mealy_machine(self, value: str):
        self.__mealy_machine = value

        self.__states: List[str] = StringMng.get_states_from_kiss(value)
        self.__initial_state: str = StringMng.get_initial_state_from_kiss(value)
        self.__current_state = self.__initial_state

        inputs_str: List[str] = StringMng.get_inputs_from_kiss(value)
        self.__input_alphabet: List[Boolean] = []
        for input in inputs_str:
            self.__input_alphabet.append(self.world[input])

        outputs_str: List[str] = StringMng.get_outputs_from_kiss(value)
        self.__output_alphabet: List[Boolean] = []
        for output in outputs_str:
            self.__output_alphabet.append(self.world[output])

        """For each input and variables, returns the AP tuple corresponding to its true/false/dontcare assignment"""
        self.__inputs_ap: Dict[Boolean, Tuple[Atom, Atom, Atom]] = {}
        for input_type in self.__input_alphabet:
            atom = input_type.to_atom()
            self.__inputs_ap[input_type] = (atom, ~atom, atom.get_dontcare())
        self.__outputs_ap: Dict[Boolean, Tuple[Atom, Atom, Atom]] = {}
        for output_type in self.__output_alphabet:
            atom = output_type.to_atom()
            self.__outputs_ap[output_type] = (atom, ~atom, atom.get_dontcare())

        """Transition is from (inputs, state) to (state, output), i.e. I x S -> S x O"""
        self.__transitions: Dict[Tuple[Tuple[Atom], str], Tuple[str, Tuple[Tuple[Atom]]]] = {}
        for line in value.splitlines()[7:]:
            transition = line.split()
            if(len(self.__input_alphabet) == 0):
                input_str = ""
                cur_state_str = transition[0]
                next_state_str = transition[1]
                output_str_list = []
                for element in transition[2:]:
                    if "+" in element:
                        continue
                    output_str_list.append(element)
            else:
                input_str = transition[0]
                cur_state_str = transition[1]
                next_state_str = transition[2]
                output_str_list = []
                for element in transition[3:]:
                    if "+" in element:
                        continue
                    output_str_list.append(element)

            list_inputs: List[Atom] = []
            for i, input in enumerate(input_str):
                if input == "1":
                    list_inputs.append(self.__inputs_ap[self.__input_alphabet[i]][0])
                elif input == "0":
                    list_inputs.append(self.__inputs_ap[self.__input_alphabet[i]][1])
                else:
                    list_inputs.append(self.__inputs_ap[self.__input_alphabet[i]][2])

            output_alternatives = []
            for output_str in output_str_list:
                list_outputs: List[Atom] = []
                for i, output in enumerate(output_str):
                    if output == "1":
                        list_outputs.append(self.__outputs_ap[self.__output_alphabet[i]][0])
                    elif output == "0":
                        list_outputs.append(self.__outputs_ap[self.__output_alphabet[i]][1])
                    else:
                        list_outputs.append(self.__outputs_ap[self.__output_alphabet[i]][2])
                output_alternatives.append(tuple(list_outputs))

            self.__transitions[(tuple(list_inputs), cur_state_str)] = (next_state_str, tuple(output_alternatives))

    @property
    def states(self) -> List[str]:
        return self.__states

    @property
    def input_alphabet(self) -> List[Boolean]:
        return self.__input_alphabet

    @property
    def output_alphabet(self) -> List[Boolean]:
        return self.__output_alphabet

    @property
    def transitions(self) -> Dict[Tuple[List[Atom], str], Tuple[str, Tuple[List[Atom]]]]:
        return self.__transitions

    @property
    def initial_state(self) -> str:
        return self.__initial_state

    @property
    def current_state(self) -> str:
        return self.__current_state

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
            result_kiss = subprocess.check_output([command_kiss], shell=True, timeout=timeout,
                                                  encoding='UTF-8').splitlines()

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
