from uuid import uuid4
from random import randrange

import pygame

from src.config import WORLD_HEIGHT, WORLD_WIDTH
from src.game_setup import screen, GREEN


class Food(object):
    food = []

    def __init__(self, x=randrange(0, WORLD_WIDTH), y=randrange(0, WORLD_HEIGHT), oid=uuid4()):
        self.x = x
        self.y = y
        self.oid = oid

        Food.food.append(self)

    def evaluate(self):
        self.draw()
        return

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 4)
        return
