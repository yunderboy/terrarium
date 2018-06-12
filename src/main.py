from typing import Tuple
import time

from src.environment import environment
from src.config import MAX_AGENTS
from src.actions import Action
from src.observations import Observation
from src.logger import logger

if __name__ == '__main__':

    rand_actions = tuple([Action(rotation='ccw', movement=True) for i in range(MAX_AGENTS)])

    world = environment(2000 * 22)
    next(world)
    for i in range(2000*2):
        time.sleep(1)
        observations: Tuple[Observation, ...] = world.send(rand_actions)
        logger.info('Observations: \n %s', observations.__str__())
