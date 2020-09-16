from typing import List
from tools.logic import And
from typescogomo.formula import LTL
from old_src.typescogomo.variables import Variables


class Pattern(LTL):
    """
    General Pattern Class
    """

    def __init__(self, formula: str, variables: Variables):
        super().__init__(formula=formula, variables=variables, kind="robotic_pattern")
        self.domain_properties = []


class CoreMovement(Pattern):
    """Core Movements Patterns
    All the variables are locations where there robot can be at a certain time"""

    def __init__(self, pattern_formula: str, locations: List[LTL], variables: Variables):
        super().__init__(pattern_formula, variables)


class Visit(CoreMovement):
    """Visit a set of locations in an unspecified order"""

    def __init__(self, locations: List[LTL]):
        variables = Variables()
        pattern_formula = []

        for location in locations:
            variables |= location.variables
            pattern_formula.append("F(" + location.formula + ")")

        pattern_formula = And(pattern_formula)

        super().__init__(pattern_formula, locations, variables)


class SequencedVisit(CoreMovement):
    """Visit a set of locations in sequence, one after the other"""

    def __init__(self, locations: List[LTL]):

        variables = Variables()
        pattern_formula = "F("

        for n, location in enumerate(locations):
            variables |= location.variables
            pattern_formula += location.formula
            if n == len(locations) - 1:
                for _ in range(len(locations)):
                    pattern_formula += ")"
            else:
                pattern_formula += " & F("

        super().__init__(pattern_formula, locations, variables)


class Patrolling(CoreMovement):
    """Keep visiting a set of locations, but not in a particular order"""

    def __init__(self, locations: List[LTL] = None):
        variables = Variables()
        pattern_formula = []

        for location in locations:
            variables |= location.variables
            pattern_formula.append("G(F(" + location.formula + "))")

        pattern_formula = And(pattern_formula)

        super().__init__(pattern_formula, locations, variables)


class SequencedPatrolling(CoreMovement):
    """Keep visiting a set of locations in sequence, one after the other"""

    def __init__(self, locations: List[LTL] = None):

        variables = Variables()
        pattern_formula = "G(F("

        for n, location in enumerate(locations):
            variables |= location.variables
            pattern_formula += location.formula
            if n == len(locations) - 1:
                for _ in range(len(locations)):
                    pattern_formula += ")"
            else:
                pattern_formula += " & F("

        pattern_formula += ")"

        super().__init__(pattern_formula, locations, variables)


class OrderedPatrolling(CoreMovement):
    """Keep visiting a set of locations, in a particular order"""

    def __init__(self, locations: List[LTL] = None):
        variables = Variables()
        pattern_formula = []

        formula = "G("
        for i, location in enumerate(locations):
            variables |= location.variables
            formula += "F(" + location.formula
            if i < len(locations) - 1:
                formula += " & "
        for i in range(0, len(locations)):
            formula += ")"
        formula += ")"
        pattern_formula.append(formula)

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                pattern_formula.append("(!" + locations[n + 1].formula + " U " + locations[n].formula + ")")

        for n, location in enumerate(locations):
            if n < len(locations):
                pattern_formula.append("G(" + locations[(n + 1) % len(locations)].formula + " ->  " +
                                       "X((!" + locations[(n + 1) % len(locations)].formula + ") U " + locations[
                                           n].formula + "))")

        pattern_formula = And(pattern_formula)

        super().__init__(pattern_formula, locations, variables)


class StrictOrderPatrolling(CoreMovement):
    """Keep visiting a set of locations, but not in a particular order"""

    def __init__(self, locations: List[LTL] = None):
        variables = Variables()
        pattern_formula = []

        formula = "G("
        for i, location in enumerate(locations):
            variables |= location.variables
            formula += "F(" + location.formula
            if i < len(locations) - 1:
                formula += " & "
        for i in range(0, len(locations)):
            formula += ")"
        formula += ")"
        pattern_formula.append(formula)

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                pattern_formula.append("(!" + locations[n + 1].formula + " U " + locations[n].formula + ")")

        for n, location in enumerate(locations):
            if n < len(locations):
                pattern_formula.append("G(" + locations[(n + 1) % len(locations)].formula + " ->  " +
                                       "X((!" + locations[(n + 1) % len(locations)].formula + ") U " + locations[
                                           n].formula + "))")

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                pattern_formula.append("G(" + locations[n].formula + " ->  " +
                                       "X((!" + locations[n].formula + ") U " + locations[
                                           (n + 1) % len(locations)].formula + "))")

        pattern_formula = And(pattern_formula)

        super().__init__(pattern_formula, locations, variables)


class StrictOrderVisit(CoreMovement):
    """Given a set of locations the robot should visit all the locations following a strict order"""

    def __init__(self, locations: List[LTL] = None):
        variables = Variables()
        pattern_formula = []

        formula = ""
        for i, location in enumerate(locations):
            variables |= location.variables
            formula += "F(" + location.formula
            if i < len(locations) - 1:
                formula += " & "
        for i in range(0, len(locations)):
            formula += ")"
        pattern_formula.append(formula)

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                pattern_formula.append("(!" + locations[n + 1].formula + " U " + locations[n].formula + ")")

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                pattern_formula.append(
                    "(!" + locations[n].formula + " U (" + locations[n].formula + " & X(!" + locations[
                        n].formula + " U(" + locations[n + 1].formula + "))))")

        pattern_formula = And(pattern_formula)

        super().__init__(pattern_formula, locations, variables)


# if __name__ == '__main__':
#     so = StrictOrderPatrolling([LTL("l1"), LTL("l2"), LTL("l3")])
#     print(so)

class OrderedVisit(CoreMovement):
    """Sequence visit does not forbid to visit a successor location before its predecessor, but only that after the
    predecessor is visited the successor is also visited. Ordered visit forbids a successor to be visited
    before its predecessor."""

    def __init__(self, locations: List[LTL]):

        variables = Variables()
        pattern_formula = []

        guarantee = "F("
        for n, location in enumerate(locations):
            variables |= location.variables
            guarantee += location.formula
            if n == len(locations) - 1:
                for _ in range(len(locations)):
                    guarantee += ")"
            else:
                guarantee += " & F("

        pattern_formula.append(guarantee)

        for n, location in enumerate(locations):
            if n < len(locations) - 1:
                pattern_formula.append("(!" + locations[n + 1].formula + " U " + locations[n].formula + ")")

        pattern_formula = And(pattern_formula)

        super().__init__(pattern_formula, locations, variables)


class GlobalAvoidance(Pattern):
    """Always avoid"""

    def __init__(self, proposition: LTL):
        variables = proposition.variables
        pattern_formula = "G(!" + proposition.formula + ")"

        super().__init__(pattern_formula, variables)


"""Trigger Pattern"""


class TriggerPattern(Pattern):

    def __init__(self, formula: str, variables: Variables):
        super().__init__(formula, variables)


class DelayedReaction(TriggerPattern):
    """Delayed Reaction Pattern"""

    def __init__(self, trigger: LTL, reaction: LTL):
        pattern_formula = "G(({t}) -> F({r}))".format(t=trigger.formula, r=reaction.formula)

        super().__init__(pattern_formula, Variables(trigger.variables | reaction.variables))


class InstantReaction(Pattern):
    """Instant Reaction Pattern"""

    def __init__(self, trigger: LTL, reaction: LTL):
        pattern_formula = "G(({t}) -> ({r}))".format(t=trigger.formula, r=reaction.formula)

        super().__init__(pattern_formula, Variables(trigger.variables | reaction.variables))


class PromptReaction(Pattern):
    """The occurrence of a stimulus triggers a counteraction promptly, i.e. in the next time instant."""

    def __init__(self, trigger: LTL, reaction: LTL):
        pattern_formula = "G(({t}) -> X({r}))".format(t=trigger.formula, r=reaction.formula)

        super().__init__(pattern_formula, Variables(trigger.variables | reaction.variables))


class BoundReaction(Pattern):
    """A counteraction must be performed every time and only when a speciﬁc location is entered."""

    def __init__(self, trigger: LTL, reaction: LTL):
        pattern_formula = "G( (({t}) -> ({r})) & (({r}) -> ({t})))".format(t=trigger.formula, r=reaction.formula)

        super().__init__(pattern_formula, Variables(trigger.variables | reaction.variables))


class BoundDelay(Pattern):
    """A counteraction must be performed, in the next time instant,
    every time and only when a speciﬁc location is entered."""

    def __init__(self, trigger: LTL, reaction: LTL):
        pattern_formula = "G( (({t}) -> X({r})) & (X({r}) -> ({t})))".format(t=trigger.formula, r=reaction.formula)

        super().__init__(pattern_formula, Variables(trigger.variables | reaction.variables))



class Wait(TriggerPattern):
    """Applies when a counteraction must be performed every time and only when a specific location is entered"""

    def __init__(self, where: LTL, until: LTL):
        pattern_formula = "(({w}) U ({u}))".format(w=where.formula, u=until.formula)

        super().__init__(pattern_formula, where.variables | until.variables)
