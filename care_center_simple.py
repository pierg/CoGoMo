from contract import Contract
from formula.patterns.robotic_patterns import *
from goal import Goal
from goal.operations import create_cgt
from typeset.types.basic import MutexType
from typeset.types.subtypes.actions import BooleanAction
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
        super().__init__(name)


class GoA(ReachLocation, MutexLocation):

    def __init__(self, name: str = "a"):
        super().__init__(name)


class GoB(ReachLocation, MutexLocation):

    def __init__(self, name: str = "b"):
        super().__init__(name)


class GoC(ReachLocation, MutexLocation):

    def __init__(self, name: str = "c"):
        super().__init__(name)


class GoD(ReachLocation, MutexLocation):

    def __init__(self, name: str = "d"):
        super().__init__(name)


day: LTL = Day().assign_true()
night: LTL = Night().assign_true()
x: LTL = GoX().assign_true()
a: LTL = GoA().assign_true()
b: LTL = GoB().assign_true()
c: LTL = GoC().assign_true()
d: LTL = GoD().assign_true()

goals_simple = {
    Goal(
        name="day-ab",
        context=day,
        specification=StrictOrderPatrolling([a, b])
    ),
    Goal(
        name="night-cd",
        context=night,
        specification=Patrolling([c, d])
    )
}

cgt = create_cgt(goals_simple)

print(cgt)
