from contract import Contract
from goal import Goal
from goal.exceptions import GoalException
from specification.atom.pattern.basic import Init
from specification.atom.pattern.robotics.coremovement.surveillance import Patrolling
from worlds.simple_gridworld import SimpleGridWorld

"""Let us instantiate a world"""
sw = SimpleGridWorld()
t = sw.typeset

"""Definition of a goals"""

g1_a = Goal(name="init_a",
            description="Begin from location a",
            specification=Init(t["a"]))

g1_b = Goal(name="patrol_a_b",
            description="Patrolling of locations a and b",
            specification=Patrolling([t["a"], t["b"]]) & Init(t["a"]))

try:
    g1 = Goal.composition({g1_a, g1_b})
    print(g1)
except GoalException as e:
    raise e

g1 = Goal(name="patrol_a_b_init_a",
          description="Patrolling of locations a and b, beginning from location a",
          specification=Patrolling([t["a"], t["b"]]) & Init(t["a"]))

g2 = Goal(name="patrol_c_d_init_c",
          description="Patrolling of locations c and d, beginning from location c",
          specification=Patrolling([t["c"], t["d"]]) & Init(t["c"]))

try:
    g12 = Goal.composition({g1, g2})
    print(g12)
except GoalException as e:
    print("Initial location is both 'a' and 'c'")

try:
    g12 = Goal.conjunction({g1, g2})
    print(g12)
except GoalException as e:
    print("Conjunction has also failed since both goals have same ('TRUE') assumptions")
