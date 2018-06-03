import time

import pygame

from src.config import WORLD_HEIGHT, WORLD_WIDTH, MAX_BLOBS, MAX_FOOD
from src.game_setup import WHITE
from src.god_functions.spawn_entities import spawn_blobs, spawn_food
from src.Blob import Blob
from src.Food import Food
from src.logger import logger


def main():
    world_age = 0

    screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
    screen.fill(WHITE)
    pygame.display.update()

    while True:
        #time.sleep(0.005)
        screen.fill(WHITE)

        world_age += 1

        if len(Blob.blobs) < MAX_BLOBS:
            spawn_blobs(amount=1)

        if len(Food.food) < MAX_FOOD:
            spawn_food()

        # Evaluate food
        for food in Food.food:
            food.evaluate()

        # Evaluate blobs
        for blob in Blob.blobs:
            blob.evaluate()

        ev = pygame.event.get()

        for event in ev:

            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()


if __name__ == '__main__':
    main()
