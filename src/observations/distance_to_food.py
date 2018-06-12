import math

from src.config import VISION_ANGLE
from src.named_tuples import Point, Vector, Food


def derive_vision_coordinates(v_1: Vector, v_2: Vector, pos: Point) -> Point:
    p_1 = Point(v_1.a + pos.x, v_1.b + pos.y)
    p_2 = Point(v_2.a + pos.x, v_2.b + pos.y)

    return p_1, p_2


def derive_vectors(angle: float) -> any:
    angle_1 = angle + VISION_ANGLE
    vector_1 = Vector(math.cos(angle_1) * 100, math.sin(angle_1) * 100)

    angle_2 = angle - VISION_ANGLE
    vector_2 = Vector(math.cos(angle_2) * 100, math.sin(angle_2) * 100)

    return angle_1, vector_1, angle_2, vector_2


def compute_dist_to_food(angle: int, position: Point, grid) -> float:
    """

    :param angle:
    :param position:
    :param grid:
    :return:
    """

    # Derive vectors and angles
    a_1, v_1, a_2, v_2 = derive_vectors(angle)

    # Derive vector of the vision cone
    p_1, p_2 = derive_vision_coordinates(v_1, v_2, position)

    # Calculate the area where food might be within the vision cone of the position
    dist: int = int(math.hypot(position.x - p_1.x, position.y - p_1.y))

    # query the grid for nearby food TODO: implement world size limitiation
    potential_area = __flatten_grid(
        grid[position.x: position.x + dist][position.y: position.y + dist] +
        grid[position.x: position.x - dist][position.y: position.y + dist] +
        grid[position.x: position.x + dist][position.y: position.y - dist] +
        grid[position.x: position.x - dist][position.y: position.y - dist]
    )

    for entity in potential_area:
        if isinstance(entity, Food):
            if __point_in_triangle(p_1, p_2, position, entity.position):
                return math.hypot(position.x - entity.position.x, position.y - entity.position.y)

    # TODO: implement
    return -1.0


def __determinant(v_1: Point, v_2: Point) -> any:
    return v_1.x*v_2.y - v_1.y*v_2.x


def __check_side(a: Point, b: Point, c: Point, p: Point):

    ab = Point(b.x - a.x, b.y - a.y)
    ap = Point(p.x - a.x, p.y - a.y)
    ac = Point(c.x - a.x, c.y - a.y)

    d_1 = __determinant(ab, ap)
    d_2 = __determinant(ab, ac)

    if (d_1 > 0 and d_2 > 0) or (d_1 < 0 and d_2 < 0):
        return True
    else:
        return False


def __point_in_triangle(a: Point, b: Point, c: Point, p: Point):
    if __check_side(a, b, c, p):
        if __check_side(b, c, a, p):
            if __check_side(c, a, b, p):
                return True
    else:
        return False


def __flatten_grid(potential_area):
    flat: list = []
    for x in potential_area:
        for y in x:
            for z in y:
                flat.append(z)
    return flat
