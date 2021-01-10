from goal import Goal
from goal.cgg import Node, GraphTraversal
from goal.exceptions import GoalException
from specification.atom.pattern.basic import Init
from specification.atom.pattern.robotics.coremovement.surveillance import Patrolling
from worlds.abcd_gridworld import ABCDGridworld
from worlds.simple_gridworld import SimpleGridWorld

"""Let us instantiate a world"""
sw = SimpleGridWorld()
""""
    A   B   
      X
    C   D
"""
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

    print(
        "The CGG is unrealizable because a-b, c-d are adjacent within each other but there is no way to go from a-b to c-d")

    """Let us instantiate a different world"""
    sw = ABCDGridworld()
    """"
        A   B   
        C   D
    """
    t = sw.typeset

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

    print("Now the CGG is realizable and the controller is generated")
    cgg.save()


except GoalException as e:

    raise e
