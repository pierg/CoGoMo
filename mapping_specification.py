import os

from contracts.contract import PContract
from src.goals.cgtgoal import *
from typescogomo.subtypes.patterns import *
# from typescogomo.formula import AndLTL, NotLTL
from typescogomo.subtypes.scopes import *


def get_inputs():
    """The designer specifies a mission using the predefined catalogue of patterns
       In addition to the patterns to use the designer specifies also in which context each goal can be active"""

    print("CUSTOM SPEC c2:")
    print(os.path.dirname(os.path.abspath(__file__)))

    """ Atomic propositions divided in
            s - sensor propositions (uncontrollable)
            l - location propositions (controllable e.g. goto)
            a - action propositions (controllable)"""
    ap = {
        "s": {
            "day_time": LTL("day_time"),
            "night_time": LTL("night_time"),
            "warehouse": LTL("warehouse")
        },
        "l": {
            "go_entrace": LTL("go_entrace"),
            "go_counter": LTL("go_counter"),
            "go_back": LTL("go_back"),
            "go_warehouse": LTL("go_warehouse"),
            "go_charging_point": LTL("go_charging_point"),
            "go_safe_loc": LTL("go_safe_loc")
        },
        "a": {
            "heavy_item_pickup": LTL("heavy_item_pickup")
        }
    }

    """List of specifications / goals"""
    list_of_goals = [
        CGTGoal(
            name="night-time-patroling",
            description="patrol warehouse and shop during the night",
            context=Context(cnf={ap["s"]["night_time"]}),
            contracts=[PContract([
                SequencedPatroling([
                    ap["l"]["go_entrace"], ap["l"]["go_counter"], ap["l"]["go_back"], ap["l"]["go_warehouse"]
                ])
            ])]
        ),
        CGTGoal(
            name="day-time-visit",
            description="Visit three locations in order",
            context=Context(cnf={ap["s"]["day_time"]}),
            contracts=[PContract([
                OrderedVisit([
                    ap["l"]["go_entrace"], ap["l"]["go_counter"], ap["l"]["go_warehouse"]
                ])
            ])]
        ),
        CGTGoal(
            name="day-time-avoidance",
            description="Avoid going to the back during the day",
            context=Context(cnf={ap["s"]["day_time"]}),
            contracts=[PContract([
                GlobalAvoidance(ap["l"]["go_back"])
            ])]
        ),
        CGTGoal(
            name="heavy-item-pick-up",
            description="always when in the warehouse, pickup an heavy-item",
            contracts=[PContract([
                DelayedReaction(
                    trigger=ap["s"]["warehouse"],
                    reaction=ap["l"]["heavy_item_pickup"]
                )
            ])]
        )
    ]


    """ Contexts rules, e.g. shop xor warehouse etc..
            Domain rules, e.g. different locations
            Liveness rules, i.e. assumptions when generating the controller e.g. GF alarm, GF !alarm"""
    rules = {
        "context": {
            "mutex": [
                [ap["s"]["day_time"], ap["s"]["night_time"]]
            ],
            "inclusion": [
            ]
        },
        "domain": {
            "mutex": [[
                ap["l"]["go_entrace"],
                ap["l"]["go_counter"],
                ap["l"]["go_back"],
                ap["l"]["go_warehouse"],
                ap["l"]["go_charging_point"],
                ap["l"]["go_safe_loc"]
            ]],
            "inclusion": [
            ]
        },
        "environment": {
            "mutex": [
            ],
            "inclusion": [
            ],
            "liveness": [
            ]
        }
    }

    return ap, rules, list_of_goals
