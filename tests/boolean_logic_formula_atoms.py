from specification.formula import FormulaOutput
from specification.atom import Atom
from specification.formula import Formula
from type import MutexType
from type.subtypes.locations import ReachLocation
from typeset import Typeset


class MutexLocation(MutexType):
    pass


class GoA(ReachLocation, MutexLocation):

    def __init__(self, name: str = "a"):
        super().__init__(name, adjacent_to={"GoX", "GoB"})


class GoB(ReachLocation, MutexLocation):

    def __init__(self, name: str = "b"):
        super().__init__(name, adjacent_to={"GoX", "GoA"})


class GoC(ReachLocation, MutexLocation):

    def __init__(self, name: str = "c"):
        super().__init__(name, adjacent_to={"GoX", "GoD"})


class GoD(ReachLocation, MutexLocation):

    def __init__(self, name: str = "d"):
        super().__init__(name, adjacent_to={"GoX", "GoC"})


a = GoA()
b = GoB()
c = GoC()
d = GoD()

a = Atom((a.name, Typeset({a})))
b = Atom((b.name, Typeset({b})))

c = Atom((c.name, Typeset({c})))
d = Atom((d.name, Typeset({d})))

#
# one = a & b
# print(one)
#

one = a & b

print("\none")
print(one.formula(FormulaOutput.CNF)[0])
print(one.formula(FormulaOutput.DNF)[0])

one = ~ one

print("\nNOT one")
print(one.formula(FormulaOutput.CNF)[0])
print(one.formula(FormulaOutput.DNF)[0])

one = ~ one

print("\nNOT NOT one")
print(one.formula(FormulaOutput.CNF)[0])
print(one.formula(FormulaOutput.DNF)[0])


two = c | d

three = one & one & two
four = one | two

print("\ntwo")
print(two.formula(FormulaOutput.CNF)[0])
print(two.formula(FormulaOutput.DNF)[0])


print("\nthree")
print(three.formula(FormulaOutput.CNF)[0])
print(three.formula(FormulaOutput.DNF)[0])

three = ~three

print("\nNOT three")
print(three.formula(FormulaOutput.CNF)[0])
print(three.formula(FormulaOutput.DNF)[0])

three = ~three

print("\nNOT NOT three")
print(three.formula(FormulaOutput.CNF)[0])
print(three.formula(FormulaOutput.DNF)[0])

print("\nfour")
print(four.formula(FormulaOutput.CNF)[0])
print(four.formula(FormulaOutput.DNF)[0])


five = three & four
six = three | four

print("\nfive")
print(five.formula(FormulaOutput.CNF)[0])
print(five.formula(FormulaOutput.DNF)[0])

print("\nsix")
print(six.formula(FormulaOutput.CNF)[0])
print(six.formula(FormulaOutput.DNF)[0])


seven = five >> six

print("\nseven")
print(seven.formula(FormulaOutput.CNF)[0])
print(seven.formula(FormulaOutput.DNF)[0])
