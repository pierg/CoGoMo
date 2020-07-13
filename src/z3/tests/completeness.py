#!/usr/bin/env python
"""Test Library module provides a test suite for LTL contract verifier"""

import os
import sys

from src_z3.parser import parse
from src_z3.cgtgoal import *

from src_z3.operations import *

sys.path.append(os.path.join(os.getcwd(), os.path.pardir))


def case2():
    goals = parse('../input_files/test_completeness.txt')

    try:
        refine_goal(goals['communicate_with_platoon_leader_abstracted'],
                    goals['communicate_with_platoon_leader_refined'])
    except Exception:
        print("Refinement not complete, Fixing..")

        refine_goal(goals['communicate_with_platoon_leader_abstracted_complete'],
                    goals['communicate_with_platoon_leader_refined_complete'])

        print(goals['communicate_with_platoon_leader_abstracted_complete'])
        print(goals['communicate_with_platoon_leader_refined_complete'])



if __name__ == "__main__":

    goals = parse('../input_files/decomposition.txt')

    communicate_with_platoon_leader_refined = compose_goals([
        goals['enstablish_connection'],
        goals['retrieve_information']], "communicate_with_platoon_leader_refined")

    try:

        refine_goal(goals['communicate_with_platoon_leader'],
                    communicate_with_platoon_leader_refined)

        print(goals['communicate_with_platoon_leader'])

    except Exception:
        print("Exception occurred")
        print("Fixing the assumptions..")

        # communicate_with_platoon_leader_refined = compose_goals([
        #     goals['enstablish_connection_fixed'],
        #     goals['retrieve_information']], "communicate_with_platoon_leader_refined")

        refine_goal(goals['communicate_with_platoon_leader_fixed'],
                    communicate_with_platoon_leader_refined)

        print(goals['communicate_with_platoon_leader_fixed'])




