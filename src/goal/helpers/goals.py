
from typing import Set

from goal import Link, Goal

def flat_goals(goals: Set[Goal]) -> Set[Goal]:
    """Extract goals that are already conjoined by the designer"""
    goals_flat = set()
    for goal in goals:
        if len(goal.children) > 0 and Link.CONJUNCTION in goal.children.keys():
            for link, goals in goal.children.items():
                if link == Link.CONJUNCTION:
                    goals_flat |= goals
        else:
            goals_flat.add(goal)
    return goals_flat

