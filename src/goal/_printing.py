from specification.formula import FormulaOutput


def __str__(self, level=0):
    """Override the print behavior"""
    ret = "\t" * level + "GOAL:    \t" + repr(self.name) + "\n"
    ret += "\t" * level + "CONTEXT:\t" + str(self.context) + "\n"
    ret += "\t" * level + "ASSUMPTIONS:\n"
    ret += self.specification.assumptions.pretty_print(FormulaOutput.DNF) + "\n"
    ret += "\t" * level + "GUARANTEES:\n"
    ret += self.specification.guarantees.pretty_print(FormulaOutput.CNF) + "\n"
    return ret

