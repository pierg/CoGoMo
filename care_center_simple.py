from formula.patterns.robotic_patterns import *
from goal import Goal
from goal.operations import create_cgt
from typeset.types.basic import MutexType
from typeset.types.subtypes.context import *
from typeset.types.subtypes.locations import ReachLocation


class MutexContextTime(MutexType):
    pass


class MutexLocation(MutexType):
    pass


class Day(ContextBooleanTime, MutexContextTime):

    def __init__(self, name: str = "day"):
        super().__init__(name)


class Night(ContextBooleanTime, MutexContextTime):

    def __init__(self, name: str = "night"):
        super().__init__(name)


class GoX(ReachLocation, MutexLocation):

    def __init__(self, name: str = "x"):
        super().__init__(name, adjacent_to={"GoA", "GoB", "GoC", "GoD"})


class GoA(ReachLocation, MutexLocation):

    def __init__(self, name: str = "a"):
        super().__init__(name, adjacent_to={"GoX", "GoB"})


class GoB(ReachLocation, MutexLocation):

    def __init__(self, name: str = "b"):
        super().__init__(name, adjacent_to={"GoX", "GoA"})


class GoC(ReachLocation, MutexLocation):

    def __init__(self, name: str = "c"):
        super().__init__(name, adjacent_to={"GoX", "GoD"})


class GoD(ReachLocation, MutexLocation):

    def __init__(self, name: str = "d"):
        super().__init__(name, adjacent_to={"GoX", "GoC"})


"""Instantiation"""
day: LTL = Day().assign_true()
night: LTL = Night().assign_true()

x: LTL = GoX().assign_true()
a: LTL = GoA().assign_true()
b: LTL = GoB().assign_true()
c: LTL = GoC().assign_true()
d: LTL = GoD().assign_true()

"""Adjacency"""

goals_simple = {
    Goal(
        name="day-ab",
        context=day,
        specification=StrictOrderPatrolling([a, b])
    ),
    Goal(
        name="night-cd",
        context=night,
        specification=StrictOrderPatrolling([c, d])
    )
}

for goal in goals_simple:
    print(goal)

# cgt = create_cgt(goals_simple)
#
# print(cgt)
