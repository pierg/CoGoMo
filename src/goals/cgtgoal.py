import hashlib
import random
import string
from copy import deepcopy
from typing import List, Dict, Tuple, Union

from contracts.contract import Contract
from typescogomo.formula import LTL
from src.checks.tools import Or, And
from typescogomo.variables import Variables


class CGTGoal:
    """Contract-based Goal Tree"""

    def __init__(self,
                 id: str = None,
                 name: str = None,
                 description: str = None,
                 contracts: List[Contract] = None,
                 refined_by: List['CGTGoal'] = None,
                 refined_with: str = None,
                 context: Union[LTL, List[LTL]] = None):

        self.__connected_to = None

        for c in contracts:
            print(c.context)

        if name is None:
            self.__name: str = ""
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

            """5 character ID generated from a random string"""
            self.__id = hashlib.sha1(random_string.encode("UTF-8")).hexdigest()[:5]
        else:
            self.__name: str = name

            """5 character ID generated from the name"""
            self.__id = hashlib.sha1(name.encode("UTF-8")).hexdigest()[:5]

        if description is None:
            self.__description: str = ""
        else:
            self.__description: str = description

        if contracts is None:
            self.__contracts: List[Contract] = []
        else:
            self.__contracts: List[Contract] = contracts

        if refined_by is None and refined_with is None:
            self.__refined_by = None
            self.__refined_with = None
        elif refined_by is not None and refined_with is not None:
            self.__refined_by: List['CGTGoal'] = refined_by
            self.__refined_with: str = refined_with
            for goal in refined_by:
                goal.connected_to = self
        else:
            raise AttributeError

        if context is not None:
            if isinstance(context, list):
                list_of_goals = []
                for c in context:
                    list_of_goals.append(CGTGoal(
                        name=name + " & " + c.formula,
                        description=description + " in " + c.formula,
                        context=c,
                        contracts=deepcopy(contracts)
                    ))
                from goals.operations import conjunction
                conjunction(list_of_goals, connect_to=self)
            else:
                self.set_context(context)

        """Is the current node realizable"""
        self.__realizable = None

        """Mealy machine of the controller (if node is realizable)"""
        self.__controller = None

        """Synthesis time"""
        self.__time_synthesis = None

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def contracts(self):
        return self.__contracts

    @contracts.setter
    def contracts(self, value):
        self.__contracts = value

    @property
    def refined_by(self):
        return self.__refined_by

    @refined_by.setter
    def refined_by(self, goals: List['CGTGoal']):
        self.__refined_by = goals
        if goals is not None:
            for goal in goals:
                goal.connected_to = self

    @property
    def refined_with(self):
        return self.__refined_with

    @refined_with.setter
    def refined_with(self, value):
        self.__refined_with = value

    @property
    def context(self) -> LTL:
        cgt_context = deepcopy(self.contracts[0].context)
        for c in self.contracts[1:]:
            cgt_context |= c.context
        return cgt_context

    @context.setter
    def context(self, value: LTL):
        self.__context = value
        self.set_context(value)

    @property
    def connected_to(self):
        return self.__connected_to

    @connected_to.setter
    def connected_to(self, value):
        self.__connected_to = value

    @property
    def realizable(self) -> bool:
        return self.__realizable

    @realizable.setter
    def realizable(self, value: bool):
        self.__realizable = value

    @property
    def controller(self) -> str:
        return self.__controller

    @controller.setter
    def controller(self, value: str):
        self.__controller = value

    @property
    def time_synthesis(self) -> int:
        return round(self.__time_synthesis, 2)

    @time_synthesis.setter
    def time_synthesis(self, value: int):
        self.__time_synthesis = value

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def get_refinement_by(self) -> Tuple[List['CGTGoal'], str]:
        return self.refined_by, self.refined_with

    def get_all_goals_with_name(self, name, copies=False):
        """Depth-first search. Returns all goals are name"""
        result = []
        if self.refined_by is not None:
            for child in self.refined_by:
                if copies:
                    child_name = child.name.replace('_copy', '')
                else:
                    child_name = child.name
                if child_name == name:
                    result.append(child)
                else:
                    result.extend(child.get_all_goals_with_name(name, copies))
        return result

    def get_all_leaf_nodes(self) -> List['CGTGoal']:
        """Depth-first search"""
        result = []
        if self.refined_by is not None:
            for child in self.refined_by:
                result.extend(child.get_all_leaf_nodes())
        else:
            result.append(self)
        return result

    def get_all_nodes(self) -> List['CGTGoal']:

        """Depth-first search"""
        result = []
        result.append(self)
        if self.refined_by is not None:
            for child in self.refined_by:
                result.extend(child.get_all_nodes())
        return result

    def synthetize(self):
        """Synthetize current node"""
        pass

    def get_goal_with_name(self, name) -> 'CGTGoal':
        """Return the goal of name 'name'"""
        res = self.get_all_goals_with_name(name)
        if len(res) == 0:
            raise Exception("No Goal with that name")
        elif len(res) == 1:
            return res[0]
        else:
            raise Exception("Multiple goals with the same name")

    def refine_by(self, refined_by: 'CGTGoal', consolidate=True, skip_check=False):
        """Refine by 'refined_by' with 'refined_with'"""
        """If type 'REFINEMENT', propagating the assumptions from the refined goal"""
        for i, contract in enumerate(self.contracts):
            contract.propagate_assumptions_from(
                refined_by.contracts[i]
            )
            from goals.operations import CGTFailException
            if not skip_check:
                if not refined_by.contracts[i] <= contract:
                    raise CGTFailException(
                        failed_operation="propagation",
                        faild_motivation="wrong refinement",
                        goals_involved_a=[self],
                        goals_involved_b=[refined_by]
                    )

        self.__refined_by = [refined_by]
        self.__refined_with = "REFINEMENT"
        if consolidate:
            self.consolidate_bottom_up()

    def provided_by(self, goal):
        """Indicates that the assumptions of 'self' are provided by the guarantees of 'goal'.
        Connects the two goal by a 'PROVIDED BY' link"""
        self.__refined_by = [goal]
        self.__refined_with = "PROVIDED_BY"
        goal.connected_to = self

    def set_context(self, context: LTL):
        """Add context to guarantees as G(context -> guarantee)"""
        for contract in self.contracts:
            contract.set_context(context)

    def add_assumption(self, assumption: LTL):

        for contract in self.contracts:
            contract.add_assumption(assumption)

        self.consolidate_bottom_up()

    def apply_rules(self, rules_dict: Dict):
        """Apply rules on the current node, if applicable"""

        for kind, rules in rules_dict.items():
            """Context rules -> Assumptions"""
            if kind == "context":
                for rule in rules:
                    for c in self.contracts:
                        if len(rule.variables & c.variables) > 0:
                            c.add_assumption(rule)

            if kind == "context_gridworld":
                for rule in rules:
                    for c in self.contracts:
                        if len(rule.variables & c.variables) > 0:
                            c.add_assumption(rule)

            """System and transition map rules -> Guarantees"""
            if kind == "gridworld":
                for rule in rules:
                    for c in self.contracts:
                        if len(rule.variables & c.guarantees.objective_variables) > 0:
                            c.add_guarantee(rule)

            if kind == "constraints":
                for rule in rules:
                    for c in self.contracts:
                        if len(rule.variables & c.guarantees.objective_variables) > 0:
                            c.add_guarantee(rule)

    def extend_from_library(self, library: 'GoalsLibrary', rules_dict: Dict):

        if len(self.contracts) > 1:
            raise Exception("Goals that have multiple conjoined contracts are not supported for extension")

        print("Extending\t" + self.name + "\t...")
        try:
            goal = library.extract_selection(self)
            print("Extending\t" + self.name + "\t...")
            goal.apply_rules(rules_dict)
            self.refine_by(goal, skip_check=True)
            print(self.name + "\textended with\t" + goal.name)
            goal.extend_from_library(library, rules_dict)

        except NoGoalFoundException:
            return

    def add_domain_properties(self):
        """Adding Domain Properties to 'cgt' (i.e. descriptive statements about the problem world (such as physical laws)
        These properties are intrinsic to the Contract/Pattern and get added as assumptions"""
        for contract in self.contracts:
            try:
                contract.add_domain_properties()
            except AttributeError:
                pass
        if self.refined_by is None:
            self.consolidate_bottom_up()
        else:
            for goal in self.refined_by:
                goal.add_domain_properties()

    def add_expectations(self, expectations: List[Contract]):
        """Domain Hypothesis or Expectations (i.e. prescriptive assumptions on the environment)
        Expectations are conditional assumptions, they get added to each contract of the CGT
        only if the Contract guarantees concern the 'expectations' guarantees and are consistent with them"""
        for contract in self.contracts:
            for expectation in expectations:
                if len(list(set(contract.variables.set) & set(expectation.variables.set))) > 0:
                    if contract.guarantees.is_satisfiable_with(expectation.guarantees):
                        contract.assumptions &= expectation.assumptions

        if self.refined_by is None:
            self.consolidate_bottom_up()
        else:
            for goal in self.refined_by:
                goal.add_expectations(expectations)

    def update_with(self, goal: 'CGTGoal', consolidate=True):
        """Update the current node of the CGT with 'goal' keeping the connection to the current parent goal
        and consolidating the tree up to the root node"""

        if self.connected_to is not None:
            parent = self.connected_to
            for n, child in enumerate(parent.refined_by):
                if child == self:
                    parent.refined_by[n] = goal

            if consolidate:
                self.consolidate_bottom_up()
        else:
            """Update Parameters"""
            self.name = goal.name
            self.description = goal.description
            self.contracts = goal.contracts
            self.refined_by = goal.refined_by
            self.refined_with = goal.refined_with

    def substitute_with(self, goal_name: str, goal_name_update: str):

        goals_to_substitute = self.get_all_goals_with_name(goal_name)
        goals_substitute = self.get_all_goals_with_name(goal_name_update)

        substituted = False

        for goal_to_substitute in goals_to_substitute:
            for goal_substitute in goals_substitute:
                if goal_to_substitute.refined_by == [goal_substitute] and \
                        goal_to_substitute.refined_with == "REFINEMENT":
                    goal_to_substitute.update_with(goal_substitute)
                    substituted = True

        if substituted:
            print("Substitution successful: " + goal_name + "with" + goal_name_update)
        else:
            print("No substitution has been performed")

    def abstract_guarantees_of(self, goal_name: str, guarantees: LTL, abstract_name: str = None):

        goals = self.get_all_goals_with_name(goal_name)
        if abstract_name is None:
            abstract_name = goal_name + "_abstracted"

        for goal in goals:
            if len(goal.contracts) > 1:
                raise Exception("At the moment you can only abstract goals that have only one conjunction")

            """Create a new abstract goal with 'guarantees' """
            refined_goal = CGTGoal()
            refined_goal.name = goal.name
            refined_goal.description = goal.description
            refined_goal.contracts = deepcopy(goal.contracts)
            refined_goal.refined_by = goal.refined_by
            refined_goal.refined_with = goal.refined_with

            """Goal become the abstract goal which is then refined with it self"""
            goal.name = abstract_name
            goal.contracts[0].guarantees = guarantees

            goal.refine_by(refined_goal)

        print("Abstraction of " + goal_name + " completed")

    def consolidate_bottom_up(self):
        """It recursivly re-perfom composition and conjunction and refinement operations up to the rood node"""
        from src.goals.operations import conjunction, composition
        if self.connected_to is not None:
            node = self.connected_to
            refined_by, refined_with = node.get_refinement_by()
            if refined_with == "CONJUNCTION":
                conjunction(refined_by, connect_to=node)
            elif refined_with == "COMPOSITION":
                composition(refined_by, connect_to=node)
            elif refined_with == "REFINEMENT":
                node.refine_by(refined_by, consolidate=False)
            else:
                raise Exception(refined_with + " consolidation not supported")

            node.consolidate_bottom_up()
        else:
            return

    def get_ltl_assumptions(self) -> LTL:
        if len(self.contracts) > 1:
            """conjunction"""
            a_list = []
            vars = Variables()
            for c in self.contracts:
                a_list.append(c.assumptions.formula)
                vars |= c.assumptions.variables
            new_formula = Or(a_list)
            return LTL(new_formula, vars, skip_checks=True)
        else:
            """composition"""
            return self.contracts[0].assumptions

    def get_ltl_guarantees(self) -> LTL:
        if len(self.contracts) > 1:
            """conjunction"""
            g_list = []
            for c in self.contracts:
                g_list.append(c.guarantees)
            return LTL(cnf=set(g_list), skip_checks=True)
        else:
            """composition"""
            return self.contracts[0].guarantees

    def get_variables(self) -> Variables:
        vars = Variables()
        for c in self.contracts:
            vars |= c.guarantees.variables
            vars |= c.assumptions.variables
        return vars

    def print_cgt_CROME(self, level=0):
        """Override the print behavior"""
        ret = "\t" * level + "GOAL    :\t" + repr(self.name) + "\n"
        ret += "\t" * level + "SCENARIO:\t" + str(self.context.formula) + "\n"
        for n, contract in enumerate(self.contracts):
            if n > 0:
                ret += "\t" * level + "\t/\\ \n"

            ret += "\t" * level + "CONTRACT:\t" + str(contract.guarantees) + "\n"

        ret += "\n"
        if self.refined_by is not None:
            ret += "\t" * level + "\t" + self.refined_with + "\n"
            level += 1
            for child in self.refined_by:
                try:
                    ret += child.print_cgt_CROME(level + 1)
                except:
                    print("ERROR IN PRINT")
        return ret

    def print_cgt_summary(self, level=0):
        """Override the print behavior"""

        """Override the print behavior"""
        ret = "\t" * level + "GOAL:\t" + repr(self.name) + "\n"
        ret += "\t" * level + "ID:\t" + repr(self.id) + "\n"

        if self.realizable is not None:
            if self.realizable:
                ret += "\t" * level + "REALIZABLE :\tYES\n"
                ret += "\t" * level + "SYNTH TIME:\t" + str(self.time_synthesis) + "\n"
            else:
                ret += "\t" * level + "REALIZABLE:\tNO\n"
                if self.time_synthesis == -200:
                    ret += "\t" * level + "OUT OF MEMORY" + "\n"
                else:
                    ret += "\t" * level + "TIME-OUT OCCURRED : " + str(self.time_synthesis) + " seconds\n"

        ret += "\n"
        if self.refined_by is not None:
            ret += "\t" * level + "\t" + self.refined_with + "\n"
            level += 1
            for child in self.refined_by:
                try:
                    ret += child.print_cgt_summary(level + 1)
                except:
                    print("ERROR IN PRINT")
        return ret

    def pretty_print_cgt_summary(self, level=0):
        """Override the print behavior"""

        """Override the print behavior"""
        ret = "\t" * level + "GOAL NAME:\t" + repr(self.name) + "\n"
        # ret += "\t" * level + "ID:\t" + repr(self.id) + "\n"
        if self.realizable is not None:
            if self.realizable:
                ret += "\t" * level + "REALIZABLE :\tYES\n"
                ret += "\t" * level + "SYNTH TIME:\t" + str(self.time_synthesis) + "\n"
            else:
                ret += "\t" * level + "REALIZABLE:\tNO"
                if self.time_synthesis == -200:
                    ret += "\t" * level + "(OUT OF MEMORY)" + "\n"
                else:
                    ret += "\t" * level + "(TIME-OUT OCCURRED : " + str(self.time_synthesis) + " seconds)\n"

        ret += "\n"
        if self.refined_by is not None:
            ret += "\t" * level + "\t" + self.refined_with + "\n"
            level += 1
            for child in self.refined_by:
                try:
                    ret += child.pretty_print_cgt_summary(level + 1)
                except:
                    print("ERROR IN PRINT")
        return ret

    def print_cgt_detailed(self, level=0):
        """Override the print behavior"""
        ret = "\t" * level + "GOAL:\t" + repr(self.name) + "\n"
        ret += "\t" * level + "ID:\t" + repr(self.id) + "\n"
        for n, contract in enumerate(self.contracts):
            if n > 0:
                ret += "\t" * level + "\t/\\ \n"
            ret += "\t" * level + "  ASSUMPTIONS:\n"
            for a in contract.assumptions.cnf:
                ret += "\t" * level + "  \t\t[" + a.kind + "]\t\t\t" + a.formula + "\n"

            ret += "\t" * level + "  GUARANTEES:\n"
            for g in contract.guarantees.cnf:
                if g.kind == "constraints":
                    ret += "\t" * level + "  \t\t[" + g.kind + "]\t\t" + g.formula + "\n"
                elif g.kind == "scope":
                    ret += "\t" * level + "  \t\t[" + g.kind + "]\t\t\t\t" + g.formula + "\n"
                else:
                    ret += "\t" * level + "  \t\t[" + g.kind + "]\t\t\t" + g.formula + "\n"

        ret += "\n"
        if self.refined_by is not None:
            ret += "\t" * level + "\t" + self.refined_with + "\n"
            level += 1
            for child in self.refined_by:
                try:
                    ret += child.print_cgt_detailed(level + 1)
                except:
                    print("ERROR IN PRINT")
        return ret

    def __str__(self, level=0):
        """Override the print behavior"""
        ret = "\t" * level + "GOAL:\t" + repr(self.name) + "\n"
        ret += "\t" * level + "ID:\t" + repr(self.id) + "\n"
        for n, contract in enumerate(self.contracts):
            if n > 0:
                ret += "\t" * level + "\t/\\ \n"

            a_assumed = contract.assumptions.get_kind("")
            a_context = contract.assumptions.get_kind("context")
            a_context_gridworld = contract.assumptions.get_kind("context_gridworld")

            if a_assumed is not None:
                ret += "\t" * level + "  A:\t\t" + ' & '.join(map(str, a_assumed)) + "\n"
            else:
                ret += "\t" * level + "  A:\t\t" + "" + "\n"

            if a_context is not None:
                ret += "\t" * level + " \tCTX:\t" + ', '.join(map(str, a_context)) + "\n"

            if a_context_gridworld is not None:
                ret += "\t" * level + " \tCGR:\t" + ', '.join(map(str, a_context_gridworld)) + "\n"

            g_objective = contract.guarantees.get_kind("pattern")
            g_objective.extend(contract.guarantees.get_kind("scope"))

            a_gridworld = contract.guarantees.get_kind("gridworld")
            a_constraints = contract.guarantees.get_kind("constraints")

            ret += "\t" * level + "  G:\t\t" + ' & '.join(map(str, g_objective)) + "\n"
            # ret += "\t" * level + "  Gs:\t\t" + contract.guarantees.formula + "\n"

            if a_gridworld is not None:
                ret += "\t" * level + " \tGRD:\t" + ', '.join(map(str, a_gridworld)) + "\n"

            if a_constraints is not None:
                ret += "\t" * level + " \tSYS:\t" + ', '.join(map(str, a_constraints)) + "\n"

        ret += "\n"
        if self.refined_by is not None:
            ret += "\t" * level + "\t" + self.refined_with + "\n"
            level += 1
            for child in self.refined_by:
                try:
                    ret += child.__str__(level + 1)
                except:
                    print("ERROR IN PRINT")
        return ret


class GoalsLibrary:
    """Goals Library defined a list of goals and the operations on them"""

    def __init__(self,
                 name: str,
                 goals: List[CGTGoal] = None):

        """Name of the Goals Library"""
        self.__name = name

        """List of Goals in the Library"""
        if goals is None:
            self.__goals = []
        else:
            self.__goals = goals

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def goals(self):
        return self.__goals

    @goals.setter
    def goals(self, value: List[CGTGoal]):
        self.__goals = value

    def add_goal(self, goal: CGTGoal):

        self.goals.append(goal)

    def add_goals(self, goals: List[CGTGoal]):

        for goal in goals:
            self.add_goal(goal)

    def extract_selection(self,
                          goal_to_refine: 'CGTGoal') -> 'CGTGoal':
        """"Returns the first goal that can refine"""

        to_be_refined = goal_to_refine.contracts[0].guarantees

        for goal in self.goals:
            if goal.id != goal_to_refine.id:
                print("\n\nMAPPING?\n" + goal.contracts[0].guarantees.formula + " -> " + to_be_refined.formula + "\n\n")
                if goal.contracts[0].guarantees < to_be_refined:
                    goal_copy = deepcopy(goal)
                    return goal_copy

        raise NoGoalFoundException()


class NoGoalFoundException(Exception):
    pass
