from uuid import uuid4
import math
from random import randrange

import pygame

from src.Brain import NeuralNetwork
from src.logger import logger
from src.game_setup import BLUE, screen
from src.config import WORLD_HEIGHT, WORLD_WIDTH, BIRTH_INTERVAL


class Blob(object):
    blobs = []

    def __init__(self, x, y, health=100, rotation=0, age=0, oid=uuid4(), brain=None):
        self.x = x
        self.y = y
        self.age = age
        self.last_bred_age = 0
        self.health = health
        self.rotation = rotation
        if brain is None:
            self.brain = NeuralNetwork(2, 4, 2)
        else:
            self.brain = brain

        Blob.blobs.append(self)
        self.oid = oid

        self.rotation_angle = (2*(math.pi))/18
        self.forward_movement = 2
        self.color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))

    def evaluate(self):
        self.health += -0.1

        logger.info('Blob id: %s \n with brain: %s', self.oid, self.brain.__dict__)

        if self.health >= 0:
            self.age += 1
            self.decide_action()
            self.draw()

        else:
            for i, blob in enumerate(Blob.blobs):
                if blob.oid == self.oid:
                    del Blob.blobs[i]
                    logger.info('Blob %s died', self.oid)
                    break
        return

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5)
        return

    def decide_action(self):
        rot_out, forward_out = self.brain.feed_forward([self.rotation, self.health])

        #rotate against the watch
        if rot_out <= 0.333:
            if self.rotation >= math.pi:
                self.rotation = -math.pi + self.rotation_angle
            else:
                self.rotation += self.rotation_angle

        #rotate with the watch
        if rot_out >= 0.666:
            if self.rotation <= -math.pi:
                self.rotation = math.pi - self.rotation_angle
            else:
                self.rotation += -self.rotation_angle

        # If movement True
        if forward_out >= 0.5:
            self.x += int(math.cos(self.rotation) * self.forward_movement)
            self.y += int(math.sin(self.rotation) * self.forward_movement)

        if self.x > WORLD_WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = WORLD_WIDTH

        if self.y > WORLD_HEIGHT:
            self.y = 0
        if self.y < 0:
            self.y = WORLD_HEIGHT

        return

    def breed(self):
        if self.age - self.last_bred_age > BIRTH_INTERVAL:
            self.last_bred_age = self.age

            child = Blob(
                randrange(0, WORLD_WIDTH),
                randrange(0, WORLD_HEIGHT),
                brain=NeuralNetwork(2, 4, 2)
            )


        return