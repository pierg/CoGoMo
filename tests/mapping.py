import sys, os, shutil

from contract import Contract
from formula.patterns.dywer.scopes import FP_between_Q_and_R
from goal import Goal
from formula.patterns.robotic_patterns import *
from old_src.goals import create_contextual_clusters
from library import Library
from variable import BoundedNat, Boolean
from world_models.care_center import get_world_model

results_path = os.path.dirname(os.path.abspath(__file__)) + "/output/results"
try:
    shutil.rmtree(results_path)
except:
    pass

sys.path.append(os.path.join(os.getcwd(), os.path.pardir))

environment_rules, system_rules, ap = get_world_model()

specifications = [
        Goal(
            name="welcome-patients",
            description="welcome patients at their arrival and check their temperature",
            context=ap["day"] & ap["entrance"],
            specification=PromptReaction(
                trigger=ap["human_entered"],
                reaction=ap["welcome_patient"])
        ),
        Goal(
            name="low-battery",
            description="always go the charging point when the battery is low",
            specification=FP_between_Q_and_R(
                q=ap["low_battery"],
                p=ap["charge_battery"],
                r=ap["full_battery"])
        ),
        Goal(
            name="pickup_item",
            description="always pickup the packages arriving at the entrance",
            context=ap["night"] & ap["entrance"],
            specification=DelayedReaction(
                trigger=ap["package_arrived"],
                reaction=ap["package_pickup"])
        )
    ]

expectations = [
    Contract(
        assumptions=LTL(
            formula="G(lifting_power > 10)",
            variables=Variables({BoundedNat("lifting_power")}),
        ),
        guarantees=LTL(
            formula="G(package_pickup)",
            variables=Variables({Boolean("package_pickup")}),
        )
    )
]

context_goals = create_contextual_clusters(specifications, "MUTEX", rules_dict["context"])


goals_library = [

]

if __name__ == '__main__':
    library = Library(name="robots_library",
                      goals=goals)

    print(library)
    print("CIAO")
