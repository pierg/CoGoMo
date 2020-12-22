from goal import Goal
from specification.atom.pattern.basic import Init
from specification.atom.pattern.robotics.coremovement.coverage import Visit
from worlds.simple_gridworld import SimpleGridWorld

"""Simple Gridworld Evironment with 5 cells"""
gridworld = SimpleGridWorld()

"""Pointing to existing locations in the typeset"""
a = gridworld.typeset["go_a"]
d = gridworld.typeset["go_d"]

"""Defining goal"""
goal_reach_d = Goal(name="reach_d",
                    description="reach location d, starting from a",
                    specification=Init(a) & Visit(d))

print(str(goal_reach_d))
print(goal_reach_d.specification.guarantees.formula())

print("end")
