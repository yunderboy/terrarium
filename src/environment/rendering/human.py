import pygame
from src.helpers import WHITE, GREEN
from src.observations import derive_vision_coordinates, derive_vectors
from src.config import ENVIRONMENT_Y, ENVIRONMENT_X


def initial_render():
    pygame.init()
    pygame.display.set_caption('Terrarium')

    screen = pygame.display.set_mode((ENVIRONMENT_X, ENVIRONMENT_Y))
    screen.fill(WHITE)
    pygame.display.update()
    return screen


def render_step(screen, food, agents, ) -> None:
    screen.fill(WHITE)

    for f in food:
        pygame.draw.circle(screen, GREEN, (f.position.x, f.position.y), 2)

    if agents is not None:
        for agent in agents:
            pygame.draw.circle(screen, agent.color, (agent.position.x, agent.position.y), 5)
            _, v_1, _, v_2 = derive_vectors(agent.angle)

            p_1, p_2 = derive_vision_coordinates(v_1, v_2, agent.position)
            pygame.draw.line(screen, agent.color, agent.position, p_1)
            pygame.draw.line(screen, agent.color, agent.position, p_2)

    ev = pygame.event.get()

    for event in ev:

        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()

    return None
