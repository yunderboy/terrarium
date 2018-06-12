import math
import random
from typing import Tuple

from src.config import ENVIRONMENT_X, ENVIRONMENT_Y, MAX_FOOD, MAX_AGENTS, SEED
from src.helpers import random_color, random_point, insert_entity
from src.named_tuples import Agent, Food
from src.state import compute_state
from src.environment.rendering import render_step
from src.observations import generate_observations, Observation


def environment(max_world_age, max_agents=MAX_AGENTS):
    # Set the seed
    random.seed(SEED)

    world_age: int = 0
    world_age += 1

    # Create the grid
    grid = tuple([tuple([tuple([]) for _ in range(ENVIRONMENT_Y)]) for _ in range(ENVIRONMENT_X)])

    food = []

    # Initialize agents
    agents = tuple([
        Agent(hp=100, angle=1 * math.pi, position=random_point(), color=random_color()) for _ in range(max_agents)
    ])

    # Spawn initial food
    for i in range(MAX_FOOD):
        f = Food(position=random_point())
        food.append(f)
        grid = insert_entity(f, f.position, grid)

    # Generator environment loop
    while world_age < max_world_age:
        actions = yield

        if world_age > 0:
            # Spawn food
            if len(food) < MAX_FOOD:
                f = Food(position=random_point())
                food.append(f)
                grid = insert_entity(f, f.position, grid)

            # Compute new environment state
            new_state: tuple = compute_state(agents, actions, grid)

            # Apply state to the environment
            for state in new_state:
                agent: Agent = state[0]
                grid = insert_entity(agent, agent.position, grid)

            # Apply state to the agents
            agents = tuple([state[0] for state in new_state])

            # Generate observations
            observations: Tuple[Observation, ...] = tuple(map(lambda agent: generate_observations(agent, grid), agents))

            yield observations

        # Render graphics if rendering mode is set to human
        render_step(food, agents)
