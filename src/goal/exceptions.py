from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from goal import Goal
    from typing import List

from enum import Enum

class FailOperations(Enum):
    composition = 0
    conjunction = 1
    refinement = 2
    search_goal = 3


class FailMotivations(Enum):
    goal_not_found = 0
    inconsistent = 1
    incompatible = 2
    unfeasible = 3


class GoalFailException(Exception):
    def __init__(self,
                 failed_operation: FailOperations,
                 faild_motivation: FailMotivations,
                 goals_involved_a: List[Goal],
                 goals_involved_b: List[Goal]):
        self.failed_operation = failed_operation
        self.faild_motivation = faild_motivation
        self.goals_involved_a = goals_involved_a
        self.goals_involved_b = goals_involved_b


class GoalException(Exception):
    def __init__(self,
                 failed_operation: FailOperations,
                 faild_motivation: FailMotivations,
                 goal_involved: Goal):
        self.failed_operation = failed_operation
        self.faild_motivation = faild_motivation
        self.goal_involved = goal_involved
