from collections import namedtuple

Action = namedtuple('Action', [
    # ccw or cw
    'rotation',
    # True or False
    'movement'
])
