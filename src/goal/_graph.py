from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from goal import Goal, Link
    from typing import Set

from goal.exceptions import GoalException, FailOperations, FailMotivations


def get_parent_link(self: Goal, parent: Goal) -> Link:
    return self.parents[parent]


def get_children_link(self: Goal, child: Goal) -> Link:
    return self.children[child]


def get_goals_by_name(self: Goal, name: str, visited_nodes: Set[Goal] = None) -> Set[Goal]:
    """Depth-first search. Returns all goals with name starting from a goal"""
    result = set()
    if visited_nodes is None:
        visited_nodes = set()
    nodes_to_visit = set()
    if self.children is not None:
        nodes_to_visit |= set(self.children.keys())
    if self.parents is not None:
        nodes_to_visit |= set(self.parents.keys())
    for node in nodes_to_visit - visited_nodes:
        visited_nodes |= node
        if node.name == name:
            result |= node
        else:
            result |= node.get_goals_by_name(name, visited_nodes)
    return result


def get_goal_by_id(self: Goal, id: str, visited_nodes: Set[Goal] = None) -> Goal:
    """Depth-first search. Returns all goals with name starting from a goal"""
    if visited_nodes is None:
        visited_nodes = set()
    nodes_to_visit = set()
    if self.children is not None:
        nodes_to_visit |= set(self.children.keys())
    if self.parents is not None:
        nodes_to_visit |= set(self.parents.keys())
    for node in nodes_to_visit - visited_nodes:
        visited_nodes |= node
        if node.id == id:
            return node
        else:
            node.extend(node.get_goals_by_id(id, visited_nodes))
    raise GoalException(failed_operation=FailOperations.search_goal,
                        faild_motivation=FailMotivations.goal_not_found,
                        goal_involved=self)


def get_all_leaf_nodes(self: Goal, visited_nodes: Set[Goal] = None) -> Set[Goal]:
    """Depth-first search. Returns the goal with id if exists"""
    result = set()
    if visited_nodes is None:
        visited_nodes = set()
    nodes_to_visit = set()
    if self.children is not None:
        nodes_to_visit |= set(self.children.keys())
    if self.parents is not None:
        nodes_to_visit |= set(self.parents.keys())
    for node in nodes_to_visit - visited_nodes:
        visited_nodes |= node
        if node.children is None:
            result |= node
        else:
            result |= node.get_all_leaf_nodes(visited_nodes)
    return result


def get_all_nodes(self: Goal, visited_nodes: Set[Goal] = None) -> Set[Goal]:
    """Depth-first search"""
    result = set()
    if visited_nodes is None:
        visited_nodes = set()
    nodes_to_visit = set()
    if self.children is not None:
        nodes_to_visit |= set(self.children.keys())
    if self.parents is not None:
        nodes_to_visit |= set(self.parents.keys())
    for node in nodes_to_visit - visited_nodes:
        visited_nodes |= node
        if node.children is None:
            result |= node
        else:
            result |= node.get_all_leaf_nodes(visited_nodes)
    return result
