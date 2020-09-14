import sys, os, shutil

from formula.patterns.scopes import FP_between_Q_and_R
from goal import Goal
from formula.robotic_patterns import *
from world_models.care_center import get_world_model

results_path = os.path.dirname(os.path.abspath(__file__)) + "/output/results"
try:
    shutil.rmtree(results_path)
except:
    pass

sys.path.append(os.path.join(os.getcwd(), os.path.pardir))

environment_rules, system_rules, ap = get_world_model()

if __name__ == '__main__':
    goals = [
        Goal(
            name="patrolling",
            description="patrol the care-center",
            specification=Patrolling([ap["care_center"]])),
        Goal(
            name="serve-pharmacy",
            description="serve pharmacy during the day",
            specification=DelayedReaction(
                trigger=ap["get_med"],
                reaction=ap["give_med"])
        ),
        Goal(
            name="welcome-patients",
            description="welcome patients at their arrival and check their temperature",
            specification=PromptReaction(
                trigger=ap["human_entered"],
                reaction=ap["welcome_patient"])
        ),
        Goal(
            name="low-battery",
            description="always go the charging point when the battery is low",
            specification=FP_between_Q_and_R(
                q=ap["low_battery"],
                p=ap["charging"],
                r=ap["full_battery"]
            )
        )
    ]
