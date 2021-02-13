from goal.cgg import Node
from goal.cgg.exceptions import CGGException
from specification.atom.pattern.basic import Init
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.atom.pattern.robotics.trigger.triggers import InstantaneousReaction
from worlds.illustrative_example import IllustrativeExample

"""Illustrative Example:
GOALS to model:
during context day => start from a1, patrol a1, a2 
during context night => start from b1, patrol b1, b2 
always => if see a person, greet
"""

"""We import the world"""
w = IllustrativeExample()

"""Start from a1 and Ordered Patrolling Location a1, a2"""
ordered_patrol_a = Init(w["a1"]) & OrderedPatrolling([w["a1"], w["a2"]])

"""Start from b1 and Ordered Patrolling Location b1, b2"""
ordered_patrol_b = Init(w["b1"]) & OrderedPatrolling([w["b1"], w["b2"]])

"""If see a person greet"""
greet = InstantaneousReaction(w["person"], w["greet"])

try:

    n1 = Node(name="day_patrol_a",
              context=w["day"],
              specification=ordered_patrol_a,
              world=w)

    n3 = Node(name="greet_person",
              specification=greet,
              world=w)

    n2 = Node(name="night_patrol_b",
              context=w["night"],
              specification=ordered_patrol_b,
              world=w)

    cgg = Node.disjunction({n1, n2})

    cgg = Node.composition({cgg, n3})

    cgg.session_name = "illustrative_example"

    cgg.translate_all_to_buchi()
    cgg.realize_all()
    cgg.save()

    print(cgg)



except CGGException as e:
    raise e
