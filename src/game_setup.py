import pygame

from src.config import WORLD_WIDTH, WORLD_HEIGHT

WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)


pygame.init()
screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
pygame.display.set_caption('Terrarium')