from uuid import uuid4
import math
from random import randrange, random
import pickle

import pygame
import numpy as np

from src.Brain import NeuralNetwork
from src.logger import logger
from src.game_setup import screen, GREEN
from src.config import WORLD_HEIGHT, WORLD_WIDTH, BIRTH_INTERVAL, HEALTH_PER_AGE, MAX_BLOBS
from src.Food import Food


class Blob(object):
    blobs = []
    best_blob = {'brain': None, 'age': 0, 'mutation_rate': None}

    def __init__(self, x, y, health=100, rotation=1*math.pi, age=0, mutation_rate=None):
        self.x = x
        self.y = y
        self.age = age
        self.last_bred_age = 0
        self.health = health
        self.rotation = rotation
        self.brain = NeuralNetwork(3, 4, 2)
        self.oid = uuid4()
        self.color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
        self.radius = 5
        self.can_breed = False

        if mutation_rate is not None:
            self.mutation_rate = mutation_rate
        else:
            self.mutation_rate = np.random.randn()

        # Movement constants
        self.rotation_angle = 0.0055555555556*(math.pi)
        self.forward_movement = 2

        # Vision angle (in radians)
        self.vision = 0.2 * math.pi

        # Append to blob registry
        Blob.blobs.append(self)

    def evaluate(self):
        self.health += -HEALTH_PER_AGE

        if self.health >= 0:
            self.age += 1
            self.breed()
            self.decide_action()
            '''if self.age > Blob.best_blob['age']:
                Blob.best_blob['age'] = self.age
                Blob.best_blob['brain'] = self.brain
                Blob.best_blob['mutation_rate'] = self.mutation_rate
                # This should be done in another thread as disk writes is very slow
                with open('best_blob.pkl', 'wb') as output:
                    pickle.dump(Blob.best_blob, output, pickle.HIGHEST_PROTOCOL)
                logger.info('Top age: %s', self.age)
'''
            self.draw()

        # Kill the blob if it's too low on HP
        else:
            for i, blob in enumerate(Blob.blobs):
                if blob.oid == self.oid:
                    del Blob.blobs[i]
                    logger.info('Blob %s died', self.oid)
                    break
        return

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        return

    def decide_action(self):
        rot_out, forward_out = self.brain.feed_forward([self.rotation/10, self.health/100, self.sense_food()/100])

        # Rotate counter clockwise
        if rot_out <= 0.333:
            if self.rotation >= math.pi:
                self.rotation = -math.pi + self.rotation_angle
            else:
                self.rotation += self.rotation_angle

        # Rotate clockwise
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
        if self.age - self.last_bred_age > BIRTH_INTERVAL and len(Blob.blobs) < MAX_BLOBS and self.can_breed == True:
            self.last_bred_age = self.age
            child = Blob(randrange(1, WORLD_WIDTH), randrange(1, WORLD_HEIGHT))
            child.color = self.color
            child.brain = self.brain

            # Apply mutations in the brain weights
            child.brain.wi = [[i+self.mutation_rate for i in child.brain.wi[0]], [i+self.mutation_rate for i in child.brain.wi[1]], [i+self.mutation_rate for i in child.brain.wi[2]], [i+self.mutation_rate for i in child.brain.wi[3]]]
            child.brain.wo = [[i+self.mutation_rate for i in child.brain.wo[0]], [i+self.mutation_rate for i in child.brain.wo[1]], [i+self.mutation_rate for i in child.brain.wo[2]], [i+self.mutation_rate for i in child.brain.wo[3]]]

            logger.info('Blob %s \n has bred blob \n %s', self.oid, child.oid)

        return

    def sense_food(self):

        angle_1 = self.rotation + self.vision
        vector_1 = (math.cos(angle_1) * 100, math.sin(angle_1) * 100)

        angle_2 = self.rotation - self.vision
        vector_2 = (math.cos(angle_2) * 100, math.sin(angle_2) * 100)

        # Derive vector points
        p_1 = (vector_1[0] + self.x, vector_1[1] + self.y)
        p_2 = (vector_2[0] + self.x, vector_2[1] + self.y)

        pygame.draw.line(screen, self.color, (self.x, self.y), (p_1[0], p_1[1]))
        pygame.draw.line(screen, self.color, (self.x, self.y), (p_2[0], p_2[1]))

        logger.info('x: %s \n y: %s', self.x, self.y)

        for i, food in enumerate(Food.food):
            if self.y == food.y and self.x == food.x:
                if self.health < 100:
                    self.health += 50
                elif self.health + 50 > 100:
                    self.health = 100
                else:
                    self.health += 50

                del Food.food[i]
                self.can_breed = True

            if (self.x <= food.x <= p_1[0] or self.x >= food.x >= p_1[0] or self.x <= food.x <= p_2[0] or self.x >= food.x >= p_2[0]):
                # Derive linear functions for vectors
                a_1 = (p_1[1]-self.y)/(p_1[0]-self.x)
                b_1 = p_1[1] - a_1 * p_1[0]
                y_1 = lambda x: a_1*x+b_1

                a_2 = (p_2[1]-self.y)/(p_2[0]-self.x)
                b_2 = p_2[1] - a_2 * p_2[0] # b = y_2 - a * x_2
                y_2 = lambda x: a_2*x+b_2

                if y_1(food.x) <= food.x <= y_2(food.x):
                    pygame.draw.line(screen, GREEN, (self.x, self.y), (food.x, food.y))
                    # returns the euclaudian distance between the blob and the first food that's within it's vision cone
                    return math.hypot(food.x-self.x, food.y-self.y)

        return 0.0
