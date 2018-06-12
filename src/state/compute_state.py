from typing import Tuple

from src.named_tuples import Agent, Food
from src.config import HEALTH_PER_STEP
from src.actions import rotate, move, Action


def compute_state(agents: Tuple[Agent, ...], actions: Tuple[Action, ...], grid: Tuple[Tuple, ...]):
    new_state = []
    # TODO: implement as map() for concurrency
    for i, agent in enumerate(agents):
        new_state.append(eval_agent(agent, actions[i], grid[agent.position.x][agent.position.y]))
    return new_state


def eval_agent(agent: Agent, action: Action, z_pos: list) -> Agent:
    # Decrement agent HP (and optionally kill it)
    agent: Agent = agent._replace(hp=agent.hp-HEALTH_PER_STEP)

    if agent.hp < 0:
        # TODO: implement
        pass

    # Check whether the agent is located on the same position as food
    for i, entity in enumerate(z_pos):
        if isinstance(entity, Food):
            z_pos = list(z_pos)     # Convert the z tuple to a list
            del z_pos[i]            # Delete the food from the z list

            # Increment the agents hp
            if agent.hp+50 >= 100:
                agent = agent._replace(hp=100)
            else:
                agent = agent._replace(hp=agent.hp+50)
            break

    # Evaluate the actions send by the agent
    if action.movement is not False:
        agent: Agent = agent._replace(position=move(agent.position, agent.angle))
    if action.rotation is not False:
        agent: Agent = agent._replace(angle=rotate(agent.angle, action.rotation))

    return agent, z_pos
