from __future__ import annotations
from typing import TYPE_CHECKING

from goal.exceptions import NoGoalFoundException
from library import Library
from world import World

if TYPE_CHECKING:
    from library import Library


def map(self: Goal, library: Library, world: World):

    try:
        goal = library.extract_selection(self)
        print("Extending\t" + self.name + "\t...")
        goal.apply_rules(rules_dict)
        self.refine_by(goal, skip_check=True)
        print(self.name + "\textended with\t" + goal.name)
        goal.extend_from_library(library, rules_dict)

    except NoGoalFoundException:
        return