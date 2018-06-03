from random import randrange

from src.Blob import Blob
from src.Food import Food
from src.config import WORLD_HEIGHT, WORLD_WIDTH, MAX_BLOBS, MAX_FOOD
from src.logger import logger


def spawn_blobs(amount=MAX_BLOBS):
    logger.info('Spawned %s blobs', amount)

    for i in range(amount):
        Blob(
            randrange(0, WORLD_WIDTH),
            randrange(0, WORLD_HEIGHT)
        )
    return


def spawn_food(amount=1):
    logger.info('Spawned %s food', amount)

    for i in range(amount):
        Food()

    return