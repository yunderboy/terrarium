from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

Agent = namedtuple('Agent', ['hp', 'angle', 'position', 'color'])

Food = namedtuple('Food', ['position'])

Vector = namedtuple('Vector', ['a', 'b'])

Observation = namedtuple('Observation', ['dist_to_food', 'hp', 'agent_angle'])

GameStep = namedtuple('GameStep', ['done', 'info'])