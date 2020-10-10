from collections import defaultdict


def print_cgt_CROME(self, level=0):
    """Override the print behavior"""
    ret = "\t" * level + "GOAL    :\t" + repr(self.name) + "\n"
    ret += "\t" * level + "SCENARIO:\t" + str(self.context.formula()) + "\n"
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
            ret += "\t" * level + "  \t\t[" + a.kind + "]\t\t\t" + a.formula() + "\n"

        ret += "\t" * level + "  GUARANTEES:\n"
        for g in contract.guarantees.cnf:
            if g.kind == "constraints":
                ret += "\t" * level + "  \t\t[" + g.kind + "]\t\t" + g.formula() + "\n"
            elif g.kind == "scope":
                ret += "\t" * level + "  \t\t[" + g.kind + "]\t\t\t\t" + g.formula() + "\n"
            else:
                ret += "\t" * level + "  \t\t[" + g.kind + "]\t\t\t" + g.formula() + "\n"

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
    ret += "\t" * level + "ID:\t\t" + repr(self.id) + "\n"
    ret += "\t" * level + "CONTEXT:\t" + str(self.context) + "\n"
    ret += "\t" * level + "A:\t" + str(self.specification.assumptions) + "\n"
    ret += "\t" * level + "G:\t" + str(self.specification.guarantees) + "\n"

    # ret += "\t" * level + str(self.specification)

    ret += "\n"
    if self.children is not None:

        for link, goals in self.children.items():

            ret += "\t" * level + "\t" + link.name + "\n"
            level += 1
            for child in goals:
                try:
                    ret += child.__str__(level + 1)
                except:
                    print("ERROR IN PRINT")

    return ret

    #
    # for n, contract in enumerate(self.specification.conjoined_by):
    #     if n > 0:
    #         ret += "\t" * level + "\t/\\ \n"
    #
    #     a_assumed = contract.assumptions.get_kind("")
    #     a_context = contract.assumptions.get_kind("context")
    #     a_context_gridworld = contract.assumptions.get_kind("context_gridworld")
    #
    #     if a_assumed is not None:
    #         ret += "\t" * level + "  A:\t\t" + ' & '.join(map(str, a_assumed)) + "\n"
    #     else:
    #         ret += "\t" * level + "  A:\t\t" + "" + "\n"
    #
    #     if a_context is not None:
    #         ret += "\t" * level + " \tCTX:\t" + ', '.join(map(str, a_context)) + "\n"
    #
    #     if a_context_gridworld is not None:
    #         ret += "\t" * level + " \tCGR:\t" + ', '.join(map(str, a_context_gridworld)) + "\n"
    #
    #     g_objective = contract.guarantees.get_kind("pattern")
    #     g_objective.extend(contract.guarantees.get_kind("scope"))
    #
    #     a_gridworld = contract.guarantees.get_kind("gridworld")
    #     a_constraints = contract.guarantees.get_kind("constraints")
    #
    #     ret += "\t" * level + "  G:\t\t" + ' & '.join(map(str, g_objective)) + "\n"
    #     # ret += "\t" * level + "  Gs:\t\t" + contract.guarantees.formula() + "\n"
    #
    #     if a_gridworld is not None:
    #         ret += "\t" * level + " \tGRD:\t" + ', '.join(map(str, a_gridworld)) + "\n"
    #
    #     if a_constraints is not None:
    #         ret += "\t" * level + " \tSYS:\t" + ', '.join(map(str, a_constraints)) + "\n"
