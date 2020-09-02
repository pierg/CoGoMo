import os
import shutil

from controller.synthesis import SynthesisException
from goals.helpers import realize_specification
from helper.reactive_synthesis import general_str_to_LTL
from tests.synthesis.world_models.nemo_v2 import get_world_model

folder_path = os.path.dirname(os.path.abspath(__file__)) + "/output/"
try:
    shutil.rmtree(folder_path)
except:
    pass

environment_rules, system_rules, ap = get_world_model()

system_goals = [
    general_str_to_LTL(
        formula="G (! (X nemo) -> ! (X camera_on) )",
        variables_str=["camera_on", "nemo"],
        ap=ap
    ),
    general_str_to_LTL(
        formula="G (F (r1 | nemo)) & G (F (r3 | nemo)) & G (F (r5 | nemo)) & G (F (r8 | nemo))",
        variables_str=["r1", "r3", "r5", "r8", "nemo"],
        ap=ap
    )
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
