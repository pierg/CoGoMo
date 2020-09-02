import os

from controller.synthesis import SynthesisException
from goals.helpers import realize_specification
from tests.synthesis.world_models.yehia import get_world_model, general_LTL
from typescogomo.subtypes.patterns import *

folder_path = os.path.dirname(os.path.abspath(__file__)) + "/"

environment_rules, system_rules, ap = get_world_model()

system_goals = [
    SequencedPatrolling(locations=[ap["r1"], ap["r4"], ap["r2"]])
]

try:
    realizable, mealy_machine, exec_time = realize_specification(environment_rules,
                                                                 system_rules,
                                                                 system_goals,
                                                                 ap,
                                                                 folder_path)

    if realizable:
        print("REALIZABLE\t\tYES\t\t" + str(exec_time) + "sec")
    else:
        print("REALIZABLE\t\tNO")


except SynthesisException as e:
    if e.os_not_supported:
        print("Os not supported for synthesis. Only linux can run strix")
    elif e.trivial:
        print("The assumptions are not satisfiable. The controller is trivial.")
        raise Exception("Assumptions unsatisfiable in a CGT is impossible.")
    elif e.out_of_memory:
        print("STRIX went out of memory")
        realizable = False
        controller = None
        time_synthesis = -200
    elif e.timeout:
        print("timeout occurred")
        realizable = False
        controller = None
        time_synthesis = e.timeout_value
