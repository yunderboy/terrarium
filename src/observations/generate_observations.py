from src.observations import Observation
from src.named_tuples import Agent
from src.observations import compute_dist_to_food


def generate_observations(agent: Agent, grid) -> Observation:
    dist: int = compute_dist_to_food(agent.angle, agent.position, grid)
    return Observation(dist, agent.hp, agent.angle)
