import math

from src.named_tuples import Point
from src.config import ENVIRONMENT_X, ENVIRONMENT_Y, MOVEMENT_SPEED


def move(current_pos: Point, angle: int) -> Point:

    x = current_pos.x + int(math.cos(angle) * 5 * MOVEMENT_SPEED)
    y = current_pos.y + int(math.sin(angle) * 5 * MOVEMENT_SPEED)

    if x >= ENVIRONMENT_X:
        x = 0
    if x < 0:
        x = ENVIRONMENT_X - 1

    if y >= ENVIRONMENT_Y:
        y = 0
    if current_pos.y <= 0:
        y = ENVIRONMENT_Y - 1

    return Point(x, y)
