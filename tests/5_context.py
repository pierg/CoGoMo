from contract import Contract
from goal.cgg import Node
from goal.cgg.exceptions import CGGException
from specification.atom.pattern.basic import Init, G, F
from specification.atom.pattern.robotics.coremovement.surveillance import Patrolling
from type.subtypes.sensors import BooleanSensor
from worlds.simple_gridworld import SimpleGridWorld

"""Let us instantiate a world"""
sw = SimpleGridWorld()
""""
    A   B   
      X
    C   D
"""
t = sw.typeset
#
# """Definition of a goals"""
# try:
#
#     n1 = Node(name="patrol_a_b_init_a",
#               description="Patrolling of locations a and b beginning from a",
#               specification=Patrolling([t["a"], t["b"]]) & Init(t["a"]))
#
#     n2 = Node(name="patrol_c_d_init_c",
#               description="Patrolling of locations c and d beginning from c",
#               specification=Patrolling([t["c"], t["d"]]) & Init(t["c"]))
#
#     cgg = Node.composition({n1, n2})
#
# except CGGException as e:
#
#     try:
#
#         n1 = Node(name="patrol_a_b_init_a_and_b",
#                   description="Patrolling of locations a and b beginning from a",
#                   specification=Patrolling([t["a"], t["b"]]) & Init(t["a"]))
#
#         n2 = Node(name="patrol_c_d",
#                   description="Patrolling of locations c and d beginning from c",
#                   specification=Patrolling([t["c"], t["d"]]) & Init(t["c"]))
#
#         """In order to use all elements of the world (e.g. 'X', which is not present in the specification)
#         we could instanciate the Nodes with the World"""
#
#         n1 = Node(name="patrol_a_b_init_a",
#                   description="Patrolling of locations a and b beginning from a",
#                   specification=Patrolling([t["a"], t["b"]]) & Init(t["a"]),
#                   world=sw)
#
#         n2 = Node(name="patrol_c_d_init_c",
#                   description="Patrolling of locations c and d beginning from c",
#                   specification=Patrolling([t["c"], t["d"]]) & Init(t["c"]),
#                   world=sw)
#
#         cgg = Node.conjunction({n1, n2})
#
#     except CGGException as e:
#         print(
#             "Goals n1 and n2 cannot be neither composed nor conjoined since one demands starting "
#             "from a and another starting from c and they share the same 'true' assumption")
#
"""CASE 1: Adding a mutually exclusive condition as assumption"""


class Day(BooleanSensor):

    def __init__(self, name: str = "day"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "time"


class Night(BooleanSensor):

    def __init__(self, name: str = "night"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "time"


day = Day().to_atom()
night = Night().to_atom()

patrol_ab = Patrolling([t["a"], t["b"]]) & Init(t["a"])
patrol_cd = Patrolling([t["c"], t["d"]]) & Init(t["c"])
#
# try:
#
#     n1 = Node(name="patrol_a_b_init_a",
#               description="Patrolling of locations a and b beginning from a",
#               specification=Contract(assumptions=day, guarantees=patrol_ab),
#               world=sw)
#
#     n2 = Node(name="patrol_c_d_init_c",
#               description="Patrolling of locations c and d beginning from c",
#               specification=Contract(assumptions=night, guarantees=patrol_cd),
#               world=sw)
#
#     cgg = Node.conjunction({n1, n2})
#
#     cgg.session_name = "case_1"
#
#     cgg.translate_all_to_buchi()
#     cgg.realize_all()
#     cgg.save()
#
#     print(cgg)
#
#     print("The CGG is realizable but it does not reflect the behaviour "
#           "'always during the night do patrol_a_b_init_a, and always during the day do patrol_c_d_init_c'")
#
#
# except CGGException as e:
#     raise e
#
# """CASE 2: Adding Globally in the assumptions"""
#
# try:
#
#     n1 = Node(name="patrol_a_b_init_a",
#               description="Patrolling of locations a and b beginning from a",
#               specification=Contract(assumptions=G(day), guarantees=patrol_ab),
#               world=sw)
#
#     n2 = Node(name="patrol_c_d_init_c",
#               description="Patrolling of locations c and d beginning from c",
#               specification=Contract(assumptions=G(night), guarantees=patrol_cd),
#               world=sw)
#
#     cgg = Node.conjunction({n1, n2})
#
#     cgg.session_name = "case_2"
#
#     cgg.translate_all_to_buchi()
#     cgg.realize_all()
#     cgg.save()
#
#     print(cgg)
#
#     print("The CGG is realizable but it does not reflect the behaviour "
#           "'always during the night do patrol_a_b_init_a, and always during the day do patrol_c_d_init_c'"
#           " since once is day/night then it has always to be day/night => no switch possible")
#
#
# except CGGException as e:
#     raise e
#
# """CASE 3: Making guarantees G(condition -> something)"""
#
# try:
#
#     n1 = Node(name="patrol_a_b_init_a",
#               description="Patrolling of locations a and b beginning from a",
#               specification=Contract(guarantees=G(day >> patrol_ab)),
#               world=sw)
#
#     n2 = Node(name="patrol_c_d_init_c",
#               description="Patrolling of locations c and d beginning from c",
#               specification=Contract(guarantees=G(night >> patrol_cd)),
#               world=sw)
#
#     cgg = Node.conjunction({n1, n2})
#
#     cgg.session_name = "case_3"
#
#     cgg.translate_all_to_buchi()
#     cgg.realize_all()
#     cgg.save()
#
#     print(cgg)
#
#
# except CGGException as e:
#
#     print("Cannot conjoin since we impose that in both cases 'a' and 'c' "
#           "have to be the initial locations, and they are mutex locations")


"""CASE 3 bis: Making guarantees G(condition -> something)"""

try:

    n1 = Node(name="patrol_a_b_init_a",
              description="Patrolling of locations a and b beginning from a",
              specification=Contract(guarantees=G(day >> patrol_ab)),
              world=sw)

    """We redefine 'patrol_cd' with 'eventually c' rather than 'initially c'"""
    patrol_cd = Patrolling([t["c"], t["d"]]) & F(t["c"])

    n2 = Node(name="patrol_c_d_init_c",
              description="Patrolling of locations c and d beginning from c",
              specification=Contract(guarantees=G(night >> patrol_cd)),
              world=sw)

    cgg = Node.conjunction({n1, n2})

    cgg.session_name = "case_3"

    cgg.translate_all_to_buchi()
    cgg.realize_all()
    cgg.save()

    print(cgg)

    print("The CGG is realizable but it does not reflect the behaviour "
          "'always during the night do patrol_a_b_init_a, and always during the day do patrol_c_d_init_c'"
          " since once is day/night then it has always to be day/night => no switch possible")


except CGGException as e:
    raise e