import os
import shutil

from controller.synthesis import SynthesisException
from old_src.goals import realize_specification
from tests.synthesis.world_models.yehia import get_world_model, general_str_to_LTL

folder_path = os.path.dirname(os.path.abspath(__file__)) + "/output/"
try:
    shutil.rmtree(folder_path)
except:
    pass

environment_rules, system_rules, ap = get_world_model()

system_goals = [
    general_str_to_LTL("F(r4)", variables_str=["r4"], ap=ap)
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