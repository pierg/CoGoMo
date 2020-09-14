from enum import Enum
from typing import List

from goal import Goal


class FailOperations(Enum):
    composition = 0
    conjunction = 1
    refinement = 2
    search_goal = 3


class FailMotivations(Enum):
    goal_not_found = 0


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
