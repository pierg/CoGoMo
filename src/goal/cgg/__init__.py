from __future__ import annotations

from enum import Enum, auto
from typing import Dict, Set, Union

from contract import Contract, Specification
from goal import Goal
from goal.cgg.exceptions import CGGOperationFail, CGGFailOperations
from goal.exceptions import GoalException
from tools.storage import Store
from worlds import World


class Link(Enum):
    REFINEMENT = 0
    COMPOSITION = 1
    CONJUNCTION = 2


class GraphTraversal(Enum):
    DFS = auto()
    BFS = auto()


class Node(Goal):

    def __init__(self,
                 name: str = None,
                 description: str = None,
                 specification: Union[Specification, Contract] = None,
                 context: Specification = None,
                 world: World = None,
                 goal: Goal = None):
        """Graph properties"""

        if goal is None:
            super().__init__(name, description, specification, context, world)
        elif goal is not None and name is None and description is None and specification is None and context is None and world is None:
            super().__init__(goal.name, goal.description, goal.specification, goal.context, goal.world)
        else:
            raise AttributeError

        """Dictionary Link -> Set[Node]"""
        self.__parents = {}

        """Dictionary Link -> Set[Node]"""
        self.__children = {}

        self.__cgg_folder_name = f"cgg_root_{self.id}"

    from ._printing import __str__

    @property
    def cgg_folder_name(self) -> str:
        if self.session_name is None:
            return f"{self.__cgg_folder_name}"
        else:
            return f"{self.session_name}/{self.__cgg_folder_name}"

    @property
    def parents(self) -> Dict[Link, Set[Node]]:
        return self.__parents

    @property
    def children(self) -> Dict[Link, Set[Node]]:
        return self.__children

    def add_parents(self, link: Link, nodes: Set[Node]):
        if link in self.__parents.keys():
            self.__parents[link] |= nodes
        else:
            self.__parents[link] = nodes

    def add_children(self, link: Link, nodes: Set[Node]):
        if link == Link.COMPOSITION or link == Link.CONJUNCTION:
            if link in self.__children.keys():
                raise Exception("A composition/conjunction children link already exists!")
            self.__children[link] = nodes
        else:
            """Link.REFINEMENT"""
            if link in self.__children.keys():
                self.__children[link] |= nodes
            else:
                self.__children[link] = nodes
        for goal in self.__children[link]:
            goal.add_parents(link=link, nodes={self})

    def parents_nodes(self) -> Set[Node]:
        ret = set()
        if len(self.__parents) > 0:
            for link, values in self.__parents.items():
                ret |= values
        return ret

    def children_nodes(self) -> Set[Node]:
        ret = set()
        if len(self.__children) > 0:
            for link, values in self.__children.items():
                ret |= values
        return ret


    def translate_all_to_buchi(self, traversal: GraphTraversal = GraphTraversal.DFS, explored: Set[Node] = None, root = None):
        """Realize all nodes of the CGG"""

        if root is None:
            root = self

        if explored is None:
            explored = set()

        if traversal == GraphTraversal.DFS:
            """Dept-First Search"""
            """Label current node as explored"""
            explored.add(self)
            for node in self.children_nodes():
                if node not in explored:
                    node.translate_all_to_buchi(traversal, explored, root)

            self.translate_to_buchi(cgg_path=root.cgg_folder_name)

        if traversal == GraphTraversal.BFS:
            raise NotImplemented

    def realize_all(self, traversal: GraphTraversal = GraphTraversal.DFS, explored: Set[Node] = None, root = None):
        """Realize all nodes of the CGG"""

        if root is None:
            root = self

        if explored is None:
            explored = set()

        if traversal == GraphTraversal.DFS:
            """Dept-First Search"""
            """Label current node as explored"""
            explored.add(self)
            for node in self.children_nodes():
                if node not in explored:
                    node.realize_all(traversal, explored, root)

            self.realize_to_controller(cgg_path=root.cgg_folder_name)

        if traversal == GraphTraversal.BFS:
            raise NotImplemented

    def save(self):
        Store.save_to_file(str(self), "cgg.txt", self.cgg_folder_name)

    @staticmethod
    def composition(nodes: Set[Node], name: str = None, description: str = None) -> Node:

        try:
            new_goal = Goal.composition(nodes, name, description)
        except GoalException as e:
            raise CGGOperationFail(nodes=nodes, operation=CGGFailOperations.algebra_op, goal_ex=e)

        new_node = Node(goal=new_goal)

        new_node.add_children(link=Link.COMPOSITION, nodes=set(nodes))

        return new_node

    @staticmethod
    def conjunction(nodes: Set[Node], name: str = None, description: str = None) -> Node:

        try:
            new_goal = Goal.conjunction(nodes, name, description)
        except GoalException as e:
            raise CGGOperationFail(nodes=nodes, operation=CGGFailOperations.algebra_op, goal_ex=e)

        new_node = Node(goal=new_goal)

        new_node.add_children(link=Link.CONJUNCTION, nodes=nodes)

        return new_node
