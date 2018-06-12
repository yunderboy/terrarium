from src.environment.rendering import human
from src.config import RENDER_MODE

screen = None

# Perform initial rendering
if RENDER_MODE == 'human':
    screen = human.initial_render()


def render_step(food, agents, render_mode=RENDER_MODE):
    if render_mode == 'human':
        human.render_step(screen, food, agents)

    return
