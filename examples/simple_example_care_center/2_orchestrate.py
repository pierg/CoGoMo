import os
import pickle

from examples.simple_example_care_center import folder_name
from goal.cgg import Node, Link
from goal.cgg.exceptions import CGGException
from specification import FormulaOutput
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.atom.pattern.robotics.trigger.triggers import InstantaneousReaction, BoundReaction, Wait, \
    GlobalAvoidance, BoundDelay
from tools.persistence import Persistence
from worlds.illustrative_example import IllustrativeExample

"""Illustrative Example:
GOALS to model:
during context day => start from r1, patrol r1, r2 
during context night => start from r3, patrol r3, r4 
always => if see a person, greet
"""

"""Load CGG"""
cgg = Persistence.load_cgg(folder_name)

cgg.orchestrate(n_steps=50, t_min_context=4)

print(cgg)
