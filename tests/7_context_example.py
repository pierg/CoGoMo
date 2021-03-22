from goal.cgg import Node
from goal.cgg.exceptions import CGGException
from specification.atom.pattern.basic import Init
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.atom.pattern.robotics.trigger.triggers import InstantaneousReaction
from worlds.illustrative_example import IllustrativeExample

"""Illustrative Example:
GOALS to model:
during context day => start from r1, patrol r1, r2 
during context night => start from r3, patrol r3, r4 
always => if see a person, greet
"""

"""We import the world"""
w = IllustrativeExample()

"""Start from r1 and Ordered Patrolling Location r1, r2"""
ordered_patrol_day = Init(w["r1"]) & OrderedPatrolling([w["r1"], w["r2"]])

"""Start from r3 and Ordered Patrolling Location r3, r4"""
ordered_patrol_night = Init(w["r3"]) & OrderedPatrolling([w["r3"], w["r4"]])

"""If see a person greet"""
greet = InstantaneousReaction(w["person"], w["greet"])

try:

    n_day = Node(name="day_patrol_a",
                 context=w["day"],
                 specification=ordered_patrol_day,
                 world=w)

    n_night = Node(name="night_patrol_b",
                   context=w["night"],
                   specification=ordered_patrol_night,
                   world=w)

    n_greet = Node(name="greet_person",
                   specification=greet,
                   world=w)

    # CGG 1
    cgg_1 = Node.disjunction({n_day, n_night})
    cgg_1 = Node.composition({cgg_1, n_greet})
    cgg_1.session_name = "illustrative_example_1"
    cgg_1.translate_all_to_buchi()
    cgg_1.realize_all()
    cgg_1.save()
    print(cgg_1)

    # CGG 2
    n_day_2 = Node.composition({n_day, n_greet})
    n_night_2 = Node.composition({n_night, n_greet})
    cgg_2 = Node.disjunction({n_day_2, n_night_2})
    cgg_2.session_name = "illustrative_example_2"
    cgg_2.translate_all_to_buchi()
    cgg_2.realize_all()
    cgg_2.save()
    print(cgg_2)

    print(cgg_1.specification.guarantees == cgg_2.specification.guarantees)



except CGGException as e:
    raise e
