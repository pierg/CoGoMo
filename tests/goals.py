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

g1 = Goal(name="patrol_a_b",
          description="Patrolling of locations a and b, beginning from location a",
          specification=Patrolling([t["a"], t["b"]]) & Init(t["a"]))

g2 = Goal(name="patrol_c_d",
          description="Patrolling of locations c and d, beginning from location c",
          specification=Patrolling([t["c"], t["d"]]) & Init(t["c"]))


try:
    print(g1.specification)
    print(g2.specification)

    g12 = Goal.composition({g1, g2})
    print(g12)
except GoalException as e:
    print("Initial location is both 'a' and 'c'")


