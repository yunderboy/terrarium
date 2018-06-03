from uuid import uuid4
from random import randrange

import pygame

from src.config import WORLD_HEIGHT, WORLD_WIDTH
from src.game_setup import screen, GREEN
from src.logger import logger


class Food(object):
    food = []

    def __init__(self):
        self.x = randrange(0, WORLD_WIDTH)
        self.y = randrange(0, WORLD_HEIGHT)
        self.oid = uuid4()

        Food.food.append(self)

    def evaluate(self):
        self.draw()
        return

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 4)
        return
