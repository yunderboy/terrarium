from random import randrange

from src.config import ENVIRONMENT_Y, ENVIRONMENT_X
from src.named_tuples import Point


def random_color() -> tuple:
    return tuple((randrange(0, 255), randrange(0, 255), randrange(0, 255)))


def random_point(max_x: int=ENVIRONMENT_X, max_y: int=ENVIRONMENT_Y) -> Point:
    return Point(randrange(0, max_x), randrange(0, max_y))


def insert_entity(entity, coordinate: Point, grid: tuple) -> tuple:
    grid = list(grid)
    grid[coordinate.x] = list(grid[coordinate.x])
    grid[coordinate.x][coordinate.y] = list(grid[coordinate.x][coordinate.y])

    grid[coordinate.x][coordinate.y].append(entity)

    grid[coordinate.x][coordinate.y] = tuple(grid[coordinate.x][coordinate.y])
    grid[coordinate.x] = tuple(grid[coordinate.x])
    grid = tuple(grid)
    return grid


def delete_entity(coordinate: Point, z, grid: tuple) -> tuple:
    grid = list(grid)
    grid[coordinate.x] = list(grid[coordinate.x])
    grid[coordinate.x][coordinate.y] = list(grid[coordinate.x][coordinate.y])

    del grid[coordinate.x][coordinate.y][z]

    grid[coordinate.x][coordinate.y] = tuple(grid[coordinate.x][coordinate.y])
    grid[coordinate.x] = tuple(grid[coordinate.x])
    grid = tuple(grid)
    return grid