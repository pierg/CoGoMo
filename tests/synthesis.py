from goal import Goal
from specification.atom.pattern.basic import Init
from specification.atom.pattern.robotics.coremovement.surveillance import Patrolling
from worlds.simple_gridworld import SimpleGridWorld

"""Let us instantiate a world"""
sw = SimpleGridWorld()
t = sw.typeset

"""Definition of a goals"""

g1 = Goal(name="patrol_a_b",
          description="Patrolling of locations a and b",
          specification=Patrolling([t["a"], t["b"]]) & Init(t["a"]))

g1.realize_to_controller()

# n1_a = Node(goal=g1_a)
# n1_b = Node(goal=g1_b)
#
#
#
# n1_a.realize_to_controller()
