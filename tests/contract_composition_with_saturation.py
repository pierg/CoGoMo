from contract import Contract
from contract.operations import compose_contracts
from formula.patterns.robotic_patterns import *
from world.simple_mutex_booleans.types.sensors import *
from world.simple_mutex_booleans.types.actions import *

"""Define Typeset"""


class ObjectDetected(BooleanSensor):

    def __init__(self, name: str = "object_detected"):
        super().__init__(name)


class GraspObject(BooleanAction):

    def __init__(self, name: str = "grasp_object"):
        super().__init__(name)


class GraspBox(GraspObject):

    def __init__(self, name: str = "grasp_box"):
        super().__init__(name)


class CarryBox(BooleanAction):

    def __init__(self, name: str = "carry_box"):
        super().__init__(name)


"""Instantiate variables"""

object_detected = ObjectDetected().assign_true()
grasp_object = GraspObject().assign_true()
grasp_box = GraspBox().assign_true()
carry_box = CarryBox().assign_true()

"""Every contracts assigns a **copy** of A and G, so each contract has its saturated G"""
contract_1 = Contract(
    assumptions=object_detected,
    guarantees=grasp_object
)

contract_2 = Contract(
    assumptions=grasp_object,
    guarantees=carry_box
)

#
# """Without Simplification"""
# contract_12 = compose_contracts({contract_1, contract_2})

"""With Simplification"""
contract_12 = compose_contracts({contract_1, contract_2})
print(contract_12)
