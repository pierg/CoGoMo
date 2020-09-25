from typing import List, Union
from formula.patterns import Pattern
from tools.logic import And
from formula import LTL
from typeset import Typeset
from typeset.types.basic import Boolean


class RoboticPatterns(Pattern):
    """
    General RoboticPatterns Class
    """

    def __init__(self, formula: str, variables: Typeset, kind=None):
        if kind is None:
            kind = "robotic_pattern"

        super().__init__(formula=formula, variables=variables, kind=kind)


class CoreMovement(RoboticPatterns):
    """Core Movements RoboticPatternss
    All the variables are locations where there robot can be at a certain time"""

    def __init__(self, formula: str, variables: Typeset, kind=None):
        if kind is None:
            kind = "movement_robotic_pattern"

        super().__init__(formula=formula, variables=variables, kind=kind)


class Visit(CoreMovement):
    """Visit a set of locations in an unspecified order"""

    def __init__(self, locations: Union[List[LTL], List[Boolean]]):
        for i, elem in enumerate(locations):
            if isinstance(elem, Boolean):
                locations[i] = elem.assign_true()

        variables = Typeset()
        formula = []

        for location in locations:
            variables |= location.variables
            formula.append("F(" + location.formula + ")")

        formula = And(formula)

        super().__init__(formula=formula, variables=variables, kind="visit_robotic_pattern")


class SequencedVisit(CoreMovement):
    """Visit a set of locations in sequence, one after the other"""

    def __init__(self, locations: Union[List[LTL], List[Boolean]]):
        for i, elem in enumerate(locations):
            if isinstance(elem, Boolean):
                locations[i] = elem.assign_true()

        variables = Typeset()
        formula = "F("

        for n, location in enumerate(locations):
            variables |= location.variables
            formula += location.formula
            if n == len(locations) - 1:
                for _ in range(len(locations)):
                    formula += ")"
            else:
                formula += " & F("

        super().__init__(formula=formula, variables=variables, kind="visit_robotic_pattern")


class Patrolling(CoreMovement):
    """Keep visiting a set of locations, but not in a particular order"""

    def __init__(self, locations: Union[List[LTL], List[Boolean]] = None):
        for i, elem in enumerate(locations):
            if isinstance(elem, Boolean):
                locations[i] = elem.assign_true()

        variables = Typeset()
        formula = []

        for location in locations:
            variables |= location.variables
            formula.append("G(F(" + location.formula + "))")

        formula = And(formula)

        super().__init__(formula=formula, variables=variables, kind=None)


class SequencedPatrolling(CoreMovement):
    """Keep visiting a set of locations in sequence, one after the other"""

    def __init__(self, locations: Union[List[LTL], List[Boolean]] = None):
        for i, elem in enumerate(locations):
            if isinstance(elem, Boolean):
                locations[i] = elem.assign_true()

        variables = Typeset()
        formula = "G(F("

        for n, location in enumerate(locations):
            variables |= location.variables
            formula += location.formula
            if n == len(locations) - 1:
                for _ in range(len(locations)):
                    formula += ")"
            else:
                formula += " & F("

        formula += ")"

        super().__init__(formula=formula, variables=variables, kind=None)


class OrderedPatrolling(CoreMovement):
    """Keep visiting a set of locations, in a particular order"""

    def __init__(self, locations: Union[List[LTL], List[Boolean]] = None):
        for i, elem in enumerate(locations):
            if isinstance(elem, Boolean):
                locations[i] = elem.assign_true()

        variables = Typeset()
        formula = []

        sub_formula = "G("
        for i, location in enumerate(locations):
            variables |= location.variables
            sub_formula += "F(" + location.formula
            if i < len(locations) - 1:
                sub_formula += " & "
        for i in range(0, len(locations)):
            sub_formula += ")"
        sub_formula += ")"

        formula.append(sub_formula)

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                formula.append("(!" + locations[n + 1].formula + " U " + locations[n].formula + ")")

        for n, location in enumerate(locations):
            if n < len(locations):
                formula.append("G(" + locations[(n + 1) % len(locations)].formula + " ->  " +
                               "X((!" + locations[(n + 1) % len(locations)].formula + ") U " + locations[
                                   n].formula + "))")

        formula = And(formula)

        super().__init__(formula=formula, variables=variables, kind=None)


class StrictOrderPatrolling(CoreMovement):
    """Keep visiting a set of locations, but not in a particular order"""

    def __init__(self, locations: Union[List[LTL], List[Boolean]] = None):
        for i, elem in enumerate(locations):
            if isinstance(elem, Boolean):
                locations[i] = elem.assign_true()

        variables = Typeset()
        formula = []

        sub_formula = "G("
        for i, location in enumerate(locations):
            variables |= location.variables
            sub_formula += "F(" + location.formula
            if i < len(locations) - 1:
                sub_formula += " & "
        for i in range(0, len(locations)):
            sub_formula += ")"
        sub_formula += ")"

        formula.append(sub_formula)

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                formula.append("(!" + locations[n + 1].formula + " U " + locations[n].formula + ")")

        for n, location in enumerate(locations):
            if n < len(locations):
                formula.append("G(" + locations[(n + 1) % len(locations)].formula + " ->  " +
                               "X((!" + locations[(n + 1) % len(locations)].formula + ") U " + locations[
                                   n].formula + "))")

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                formula.append("G(" + locations[n].formula + " ->  " +
                               "X((!" + locations[n].formula + ") U " + locations[
                                   (n + 1) % len(locations)].formula + "))")

        formula = And(formula)

        super().__init__(formula=formula, variables=variables, kind=None)


class FairPatrolling(CoreMovement):
    """Keep visiting a set of locations, but not in a particular order"""

    def __init__(self, locations: Union[List[LTL], List[Boolean]] = None):
        for i, elem in enumerate(locations):
            if isinstance(elem, Boolean):
                locations[i] = elem.assign_true()

        variables = Typeset()
        sub_formula = []

        for location in locations:
            variables |= location.variables
            sub_formula.append("G(F(" + location.formula + "))")

        sub_formula = [And(sub_formula)]

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                sub_formula.append("G(" + locations[n].formula + " ->  " +
                                   "X( ((!" + locations[n].formula + ") U " + locations[
                                       (n + 1) % len(locations)].formula + ") | G " +
                                   "(!" + locations[n].formula + ")" + " ))")

        formula = And(sub_formula)

        super().__init__(formula=formula, variables=variables, kind=None)


class StrictOrderVisit(CoreMovement):
    """Given a set of locations the robot should visit all the locations following a strict order"""

    def __init__(self, locations: Union[List[LTL], List[Boolean]] = None):
        for i, elem in enumerate(locations):
            if isinstance(elem, Boolean):
                locations[i] = elem.assign_true()

        variables = Typeset()
        formula = []

        sub_formula = ""
        for i, location in enumerate(locations):
            variables |= location.variables
            sub_formula += "F(" + location.formula
            if i < len(locations) - 1:
                sub_formula += " & "
        for i in range(0, len(locations)):
            sub_formula += ")"

        formula.append(sub_formula)

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                formula.append("(!" + locations[n + 1].formula + " U " + locations[n].formula + ")")

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                formula.append(
                    "(!" + locations[n].formula + " U (" + locations[n].formula + " & X(!" + locations[
                        n].formula + " U(" + locations[n + 1].formula + "))))")

        formula = And(formula)

        super().__init__(formula=formula, variables=variables, kind=None)


class OrderedVisit(CoreMovement):
    """Sequence visit does not forbid to visit a successor location before its predecessor, but only that after the
    predecessor is visited the successor is also visited. Ordered visit forbids a successor to be visited
    before its predecessor."""

    def __init__(self, locations: Union[List[LTL], List[Boolean]]):
        for i, elem in enumerate(locations):
            if isinstance(elem, Boolean):
                locations[i] = elem.assign_true()

        variables = Typeset()
        formula = []

        sub_formula = "F("
        for n, location in enumerate(locations):
            variables |= location.variables
            sub_formula += location.formula
            if n == len(locations) - 1:
                for _ in range(len(locations)):
                    sub_formula += ")"
            else:
                sub_formula += " & F("

        formula.append(sub_formula)

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                formula.append("(!" + locations[n + 1].formula + " U " + locations[n].formula + ")")

        formula = And(formula)

        super().__init__(formula=formula, variables=variables, kind=None)


class Avoidance(RoboticPatterns):
    def __init__(self, formula: str, variables: Typeset, kind=None):
        if kind is None:
            kind = "avoidance_robotic_pattern"

        super().__init__(formula=formula, variables=variables, kind=kind)


class GlobalAvoidance(Avoidance):
    """Always avoid"""

    def __init__(self, proposition: Union[List[LTL], List[Boolean]]):
        if isinstance(proposition, Boolean):
            proposition = proposition.assign_true()

        variables = proposition.variables
        formula = "G(!" + proposition.formula + ")"

        super().__init__(formula=formula, variables=variables, kind=None)


"""Trigger RoboticPatterns"""


class Triggers(RoboticPatterns):

    def __init__(self, formula: str, variables: Typeset):
        super().__init__(formula, variables)


class DelayedReaction(Triggers):
    """Delayed Reaction RoboticPatterns"""

    def __init__(self, trigger: Union[LTL, Boolean], reaction: Union[LTL, Boolean]):

        if isinstance(trigger, Boolean):
            trigger = trigger.assign_true()

        if isinstance(reaction, Boolean):
            reaction = reaction.assign_true()

        formula = "G(({t}) -> F({r}))".format(t=trigger.formula, r=reaction.formula)

        super().__init__(formula, trigger.variables | reaction.variables)


class InstantReaction(Triggers):
    """Instant Reaction RoboticPatterns"""

    def __init__(self, trigger: Union[LTL, Boolean], reaction: Union[LTL, Boolean]):

        if isinstance(trigger, Boolean):
            trigger = trigger.assign_true()

        if isinstance(reaction, Boolean):
            reaction = reaction.assign_true()

        formula = "G(({t}) -> ({r}))".format(t=trigger.formula, r=reaction.formula)

        super().__init__(formula, trigger.variables | reaction.variables)


class PromptReaction(Triggers):
    """The occurrence of a stimulus triggers a counteraction promptly, i.e. in the next time instant."""

    def __init__(self, trigger: Union[LTL, Boolean], reaction: Union[LTL, Boolean]):

        if isinstance(trigger, Boolean):
            trigger = trigger.assign_true()

        if isinstance(reaction, Boolean):
            reaction = reaction.assign_true()

        formula = "G(({t}) -> X({r}))".format(t=trigger.formula, r=reaction.formula)

        super().__init__(formula, trigger.variables | reaction.variables)


class BoundReaction(Triggers):
    """A counteraction must be performed every time and only when a speciﬁc location is entered."""

    def __init__(self, trigger: Union[LTL, Boolean], reaction: Union[LTL, Boolean]):

        if isinstance(trigger, Boolean):
            trigger = trigger.assign_true()

        if isinstance(reaction, Boolean):
            reaction = reaction.assign_true()

        formula = "G( (({t}) -> ({r})) & (({r}) -> ({t})))".format(t=trigger.formula, r=reaction.formula)

        super().__init__(formula, trigger.variables | reaction.variables)


class BoundDelay(Triggers):
    """A counteraction must be performed, in the next time instant,
    every time and only when a speciﬁc location is entered."""

    def __init__(self, trigger: Union[LTL, Boolean], reaction: Union[LTL, Boolean]):

        if isinstance(trigger, Boolean):
            trigger = trigger.assign_true()

        if isinstance(reaction, Boolean):
            reaction = reaction.assign_true()

        formula = "G( (({t}) -> X({r})) & (X({r}) -> ({t})))".format(t=trigger.formula, r=reaction.formula)

        super().__init__(formula, trigger.variables | reaction.variables)


class Wait(Triggers):
    """Applies when a counteraction must be performed every time and only when a specific location is entered"""

    def __init__(self, where: LTL, until: LTL):
        formula = "(({w}) U ({u}))".format(w=where.formula, u=until.formula)

        super().__init__(formula, where.variables | until.variables)
