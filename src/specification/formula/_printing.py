from specification.formula import FormulaOutput


def __str__(self):
    return self.formula()[0]


def pretty_print(self, formulatype: FormulaOutput = FormulaOutput.CNF):
    return self.formula(formulatype)[0]
