import os
import shutil

from controller.synthesis import SynthesisException
from goals.helpers import realize_specification
from tests.synthesis.world_models.yehia_2 import get_world_model
from typescogomo.subtypes.robotic_patterns import *

folder_path = os.path.dirname(os.path.abspath(__file__)) + "/output/"
try:
    shutil.rmtree(folder_path)
except:
    pass

environment_rules, system_rules, ap = get_world_model()

system_goals = [
    OrderedPatrolling(locations=[ap["r1"], ap["r5"]])
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
    print(e.message)
