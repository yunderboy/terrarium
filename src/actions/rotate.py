import math

from src.config import ROTATION_SPEED


def rotate(angle: float, direction: str, rotation_speed: float = ROTATION_SPEED) -> float:
    """

    :param angle: The current angle of the agent
    :param direction: Options: ccw (counterclockwise) or cw (clockwise)
    :param rotation_speed: The amount of which to increment the angle on rotation
    :return:
    """
    new_angle: float = 0.0

    # Rotate counter clockwise
    if direction == 'ccw':
        if angle >= math.pi:
            angle = -math.pi + rotation_speed
        else:
            angle += rotation_speed

    # Rotate clockwise
    if direction == 'cw':
        if angle <= -math.pi:
            angle = math.pi - rotation_speed
        else:
            angle += -rotation_speed

    return angle
