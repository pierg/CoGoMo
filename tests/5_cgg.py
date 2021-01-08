from goal import Goal
from goal.cgg import Node, GraphTraversal
from goal.exceptions import GoalException
from specification.atom.pattern.basic import Init
from specification.atom.pattern.robotics.coremovement.surveillance import Patrolling
from worlds.simple_gridworld import SimpleGridWorld

"""Let us instantiate a world"""
sw = SimpleGridWorld()
t = sw.typeset

"""Definition of a goals"""
try:

    n1 = Node(name="patrol_a_b_init_a_and_b",
              description="Patrolling of locations a and b and init a and b",
              specification=Patrolling([t["a"], t["b"]]) & Init(t["a"]))

    n2 = Node(name="patrol_c_d",
              description="Patrolling of locations c and d",
              specification=Patrolling([t["c"], t["d"]]))

    cgg = Node.composition({n1, n2})
    print(cgg)
    cgg.realize_all(GraphTraversal.DFS)
    print(cgg)

except GoalException as e:
    raise e
