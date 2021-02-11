from contract import Contract
from goal.cgg import Node
from goal.cgg.exceptions import CGGException
from specification.atom.pattern.robotics.coremovement.surveillance import *
from type.subtypes.context import ContextBooleanTime
from type.subtypes.locations import ReachLocation
from worlds import World

"""Continuation of 5_modelling_problems:
GOAL to model:
while 'day' is true => continuously visit the office, 
and while 'night' is true => continuously visit the bed
"""

"""Let us define 'day' and 'night' as Context instead"""


class Day(ContextBooleanTime):

    def __init__(self, name: str = "day"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "time"


class Night(ContextBooleanTime):

    def __init__(self, name: str = "night"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "time"


day = Day().to_atom()
night = Night().to_atom()

"""Our goals as before, using the Patrolling Pattern"""


class A1(ReachLocation):

    def __init__(self, name: str = "a1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"A2", "Z"}


class A2(ReachLocation):

    def __init__(self, name: str = "a2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"A1", "A"}


class B1(ReachLocation):

    def __init__(self, name: str = "b1"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"B2", "Z"}


class B2(ReachLocation):

    def __init__(self, name: str = "b2"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"B1", "Z"}


class Z(ReachLocation):

    def __init__(self, name: str = "z"):
        super().__init__(name)

    @property
    def mutex_group(self):
        return "locations"

    @property
    def adjacency_set(self):
        return {"A1", "A2", "B1", "B2"}


gridworld = World({A1(), A2(), B1(), B2(), Z()})


"""Ordered Patrolling Location a1, a2"""
ordered_patrol_a = OrderedPatrolling([A1(), A2()])

"""Ordered Patrolling Location b1, b2"""
ordered_patrol_b = OrderedPatrolling([B1(), B2()])

try:

    n1 = Node(name="day_patrol_a",
              context=day,
              specification=Contract(guarantees=ordered_patrol_a),
              world=gridworld)

    n2 = Node(name="night_patrol_b",
              context=night,
              specification=Contract(guarantees=ordered_patrol_b),
              world=gridworld)

    cgg = Node.conjunction({n1, n2})

    cgg.session_name = "context_example"

    cgg.translate_all_to_buchi()
    cgg.realize_all()
    cgg.save()

    print(cgg)

    print("Although its satisfiable and realizable it does not reflect what we wat i.e.:"
          "when 'day' is true => continuously visit the office, "
          "and when 'night' is true => continuously visit the bed")

except CGGException as e:
    raise e
