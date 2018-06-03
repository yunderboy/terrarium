from uuid import uuid4
import math
from random import randrange

import pygame

from src.Brain import NeuralNetwork
from src.logger import logger
from src.game_setup import BLUE, screen
from src.config import WORLD_HEIGHT, WORLD_WIDTH, BIRTH_INTERVAL
from src.Food import Food


class Blob(object):
    blobs = []

    def __init__(self, x, y, health=100, rotation=1*math.pi, age=0):
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

        # Movement constants
        self.rotation_angle = (2*(math.pi))/18
        self.forward_movement = 2

        # Vision angle (in radians)
        self.vision = 0.2 * math.pi

        # Append to blob registry
        Blob.blobs.append(self)

    def evaluate(self):
        self.health += -0.1

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
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        return

    def decide_action(self):
        rot_out, forward_out = self.brain.feed_forward([self.rotation, self.health, self.sense_food()])

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


    def gene_mutation(self):


        return


    def breed(self):
        if self.age - self.last_bred_age > BIRTH_INTERVAL:
            self.last_bred_age = self.age
            child = Blob(randrange(0, WORLD_WIDTH), randrange(0, WORLD_HEIGHT))
            child.brain = self.brain
            for i in enumerate(child.brain.wi):
                for j in enumerate(child.brain.wi[i]):
                    child.brain.wi[i[j]] = child.brain.wi[i[j]]


        return

    def sense_food(self):

        left_angle = self.rotation + self.vision
        left_vector = (math.cos(left_angle)*100, math.sin(left_angle)*100)

        right_angle = self.rotation - self.vision
        right_vector = (math.cos(right_angle)*100, math.sin(right_angle)*100)

        # Derive vector points
        p_1 = (left_vector[0] + self.x, left_vector[1] + self.y)
        p_2 = (right_vector[0] + self.x, right_vector[1] + self.y)

        pygame.draw.line(screen, self.color, (self.x, self.y), (p_1[0], p_1[1]))
        pygame.draw.line(screen, self.color, (self.x, self.y), (p_2[0], p_2[1]))

        for i, food in enumerate(Food.food):
            if self.y == food.y and self.x == food.x:
                if self.health < 100:
                    self.health += 50
                elif self.health + 50 > 100:
                    self.health = 100
                else:
                    self.health += 50

                del Food.food[i]
                logger.info('Blob %s ate food %s, \n amount of food left: %s', self.oid, food.oid, len(Food.food))

            if self.y <= food.y <= self.y + left_vector[1]:

                # Derive linear functions for vectors
                a_1 = (p_1[1]-self.y)/(p_1[0]-self.x)
                b_1 = p_1[1] - a_1 * p_1[0]
                x_1 = lambda y: (y-b_1)/a_1

                a_2 = (p_2[1]-self.y)/(p_2[0]-self.x)
                b_2 = p_2[1] - a_2 * p_2[0] # b = y_2 - a * x_2
                x_2 = lambda y: (y-b_2)/a_2

                if x_1(food.y) <= food.x <= x_2(food.y):
                    #logger.info('x 1: %s', x_1(food.y))
                    #logger.info('x 2: %s', x_2(food.y))
                    #logger.info('Blob %s \n found food %s', (self.x, self.y), (food.x, food.y))
                    return 1.0
        return 0.0
