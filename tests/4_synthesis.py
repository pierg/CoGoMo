from goal import Goal
from goal.cgg import Node
from goal.exceptions import GoalException
from specification.atom.pattern.basic import Init
from specification.atom.pattern.robotics.coremovement.surveillance import Patrolling
from worlds.simple_gridworld import SimpleGridWorld

"""Let us instantiate a world"""
sw = SimpleGridWorld()
t = sw.typeset

"""Definition of a goals"""

g1 = Goal(name="patrol_a_b",
          description="Patrolling of locations a and b and init a",
          specification=Patrolling([t["a"], t["b"]]))

try:
    g1.realize_to_controller()
except GoalException as e:
    pass

g1 = Goal(name="patrol_a_b_init_a_and_b",
          description="Patrolling of locations a and b and init a and b",
          specification=Patrolling([t["a"], t["b"]]) & Init(t["a"]))

try:
    g1.realize_to_controller()
except GoalException as e:
    raise e

n1 = Node(goal=g1)

n2 = Node(name="patrol_c_d",
          description="Patrolling of locations c and d",
          specification=Patrolling([t["c"], t["d"]]))


try:
    n2.realize_to_controller()
except GoalException as e:
    raise e

try:
    cgg = Node.composition({n1, n2})
    print(cgg)
    cgg.realize_to_controller()
except GoalException as e:
    raise e
