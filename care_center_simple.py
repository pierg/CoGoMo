from contract import Contract
from formula.patterns.dywer.scopes import FP_between_Q_and_R
from formula.patterns.robotic_patterns import *
from goal import Goal
from goal.operations import create_cgt
from world.care_center.types.sensors import *
from world.care_center.types.actions import *
from world.care_center.types.locations import *
from world.care_center.types.context import *

variables = {
    LiftingPower(), ObjectRecognition("see_package"), BatteryIndicator(),
    Pickup("pick_package"), Greeting(), Charge(),
    GoCareCenter(), GoCorridor(), GoPharmacy(), GoEntrance(), GoMedicalRoom(), GoWaitingRoom(),
    GoB(), GoC(), GoE(), GoF(), GoCommon(), GoIsolation(), GoA(), GoD(), GoG(), GoCharging(),
    Mild(), Severe(), Time(), Positive(), Negative(), Pharmacy(), Corridoor(), Entrance()
}

t = Typeset(variables)

# day: LTL = (t["time"] > 17) | (t["time"] < 9)
# night: LTL = ~day
# mild: LTL = t["mild_symptoms"].assign_true()
# severe: LTL = t["severe_symptoms"].assign_true()
#
# low_battery: LTL = t["battery"] < 10
# full_battery: LTL = t["battery"] == 100
#
# goals = {
#     Goal(
#         name="patrol",
#         description="patrol the care-center",
#         context=[day, night],
#         specification=Patrolling([t["go_care_center"]])
#     ),
#     Goal(
#         name="pickup-package",
#         description="pickup package when at the pharmacy",
#         context=day & pharmacy,
#         specification=Contract(
#             guarantees=PromptReaction(
#                 trigger=t["see_package"],
#                 reaction=t["pick_package"])
#         )
#     ),
#     Goal(
#         name="welcome-patients",
#         description="welcome patients at their arrival and check their temperature",
#         context=[day & entrance & mild, day & entrance & severe],
#         specification=Patrolling([t["go_corridor"]])
#     ),
#     Goal(
#         name="low-battery",
#         description="always go the charging point when the battery is low",
#         specification=FP_between_Q_and_R(
#             q=low_battery,
#             p=t["do_charge"].assign_true(),
#             r=full_battery
#         )
#     )
# }
#


pharmacy: LTL = t["pharmacy"].assign_true()
entrance: LTL = t["entrance"].assign_true()


goals_simple = {
    Goal(
        name="patrol",
        description="patrol the care-center",
        specification=Patrolling([t["go_care_center"]])
    ),
    Goal(
        name="pickup-package",
        description="pickup package when at the pharmacy",
        context=pharmacy,
        specification=Contract(
            guarantees=PromptReaction(
                trigger=t["see_package"],
                reaction=t["pick_package"])
        )
    ),
    Goal(
        name="welcome-patients",
        description="welcome patients at their arrival and check their temperature",
        context=entrance,
        specification=Patrolling([t["go_corridor"]])
    )
}

cgt = create_cgt(goals_simple)

library = [
    Goal(
        name="patrol_b",
        specification=Patrolling([t["go_b"]])
    ),
    Goal(
        name="patrol_b_c_d_e",
        specification=Patrolling([t["go_b"], t["go_c"], t["go_d"], t["go_e"]])
    ),
]
