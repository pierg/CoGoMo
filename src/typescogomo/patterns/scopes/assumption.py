# from typing import Set, Union
#
# from checks.tools import Or, Implies, Not, And
# from typescogomo.formula import LTL, InconsistentException
# from typescogomo.variables import Variables
#
#
# class LTL(LTL):
#
#     def __init__(self,
#                  formula: str = None,
#                  variables: Variables = None,
#                  cnf: Set['LTL'] = None,
#                  kind: str = None,
#                  skip_checks=True):
#
#         if kind is None:
#             kind = "assumed"
#
#         super().__init__(formula=formula, variables=variables, cnf=cnf, kind=kind, skip_checks=skip_checks)
#
#
#     def __iand__(self, other: 'LTL'):
#         """self &= other
#         Modifies self with the conjunction with other"""
#         if not isinstance(other, LTL):
#             return AttributeError
#
#         if self.formula == "TRUE":
#             self.__formula = other.formula
#             self.__variables = other.variables
#             self.__cnf = other.cnf
#             return self
#
#         if other.formula == "TRUE":
#             return self
#         if other.formula == "FALSE":
#             self.__formula = "FALSE"
#             self.__cnf |= other.cnf
#             return self
#
#         self.__formula = And([self.formula, other.formula])
#         self.__variables = Variables(self.variables | other.variables)
#         self.__cnf |= other.cnf
#
#         if not self.is_satisfiable():
#             raise InconsistentException(self, other)
#         return self
#
#
#
#     def __and__(self, other: 'LTL') -> Union['LTL', 'LTL']:
#         """self & other
#         Returns a new LTL that is the conjunction of self with other"""
#         if isinstance(other, LTL):
#             return LTL(cnf={self, other})
#         else:
#             return LTL(cnf={self, other})
#
#     def __or__(self, other: 'LTL') -> Union['LTL', 'LTL']:
#         """self | other
#         Returns a new LTL that is the disjunction of self with other"""
#         if isinstance(other, LTL):
#             return LTL(
#                 formula=Or([self.formula, other.formula]),
#                 variables=Variables(self.variables | other.variables)
#             )
#         else:
#             return LTL(
#                 formula=Or([self.formula, other.formula]),
#                 variables=Variables(self.variables | other.variables)
#             )
#
#     def __invert__(self) -> 'LTL':
#         """~ self
#         Returns a new LTL that is the negation of self"""
#         return LTL(
#             formula=Not(self.formula),
#             variables=self.variables
#         )
#
#     def __rshift__(self, other: 'LTL') -> Union['LTL', 'LTL']:
#         """>> self
#         Returns a new LTL that is the result of self -> other (implies)"""
#         if isinstance(other, LTL):
#             return LTL(
#                 formula=Implies(self.formula, other.formula),
#                 variables=Variables(self.variables | other.variables)
#             )
#         else:
#             return LTL(
#                 formula=Implies(self.formula, other.formula),
#                 variables=Variables(self.variables | other.variables)
#             )
#
#
# class Expectation(LTL):
#
#     def __init__(self,
#                  formula: str = None,
#                  variables: Variables = None,
#                  cnf: Set['Expectation'] = None):
#         super().__init__(formula, variables, cnf, kind="expectation")
#
#
# class Domain(LTL):
#
#     def __init__(self,
#                  formula: str = None,
#                  variables: Variables = None,
#                  cnf: Set['Domain'] = None):
#         super().__init__(formula, variables, cnf, kind="domain")
#
# # class Context(Assumption):
# #
# #     def __init__(self, scope: 'LTL' = None, formula: str = None, variables: Variables = None):
# #         if scope is not None:
# #             super().__init__(scope.formula, scope.variables, kind="context")
# #         else:
# #             super().__init__(formula, variables, kind="context")
# #
