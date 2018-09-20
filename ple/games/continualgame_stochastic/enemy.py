__author__ = 'Batchu Vishal'
import pygame
import os
from .onBoard import OnBoard
import random
from random import randint

class enemy(OnBoard):
    """
    This class defines all our enemys.
    """

    def __init__(self, raw_image, position, _dir):
        OnBoard.__init__(self, raw_image, position)
        self.__coinAnimState = 0  # Initialize animation state to 0
        self.position = position
        self.IMAGES = {
            "enemy1": pygame.transform.scale(pygame.image.load(os.path.join(_dir, 'assets/enemy1.png')), (15, 15)).convert_alpha(),
            "enemy2": pygame.transform.scale(pygame.image.load(os.path.join(_dir, 'assets/enemy1.png')), (15, 15)).convert_alpha(),
            "enemy3": pygame.transform.scale(pygame.image.load(os.path.join(_dir, 'assets/enemy1.png')), (15, 15)).convert_alpha(),
            "enemy4": pygame.transform.scale(pygame.image.load(os.path.join(_dir, 'assets/enemy1.png')), (15, 15)).convert_alpha(),
            "enemy5": pygame.transform.scale(pygame.image.load(os.path.join(_dir, 'assets/enemy1.png')), (15, 15)).convert_alpha()
        }
        self.speed = 0.7#randint(1,1) #speed of enemy
        self.direction = 0 #direction of enemy
        self.c = 0 #counter to move enemy c number of times in each direction
        self.n = 40#randint(20,20) #how many times to move enemy in each direction

    # Update the image of the enemy
    def updateImage(self, raw_image):
        self.image = raw_image

    def moveEnemy(self):

        if self.direction == 0:
            
            if self.c<self.n:
                self.updateWH(self.IMAGES["enemy1"], "H", self.speed, 45, 45)
                self.c = self.c+1
            else:
                self.c = 0
                self.direction = 1 #random.choice([1,2])
        elif self.direction == 1:
            if self.c<self.n:
                self.updateWH(self.IMAGES["enemy1"], "H", -self.speed, 45, 45)
                self.c = self.c+1
            else:
                self.c = 0
                self.direction = 0 #random.choice([0,2])
        elif self.direction == 2:
            self.updateY(-self.speed)
            self.updateY(self.speed)
            #self.updateWH(self.IMAGES["coin1"], "V", self.speed, 45, 45)
            self.direction = random.choice([0,1])


    # Animate the enemy
    def animateenemy(self):
        self.__enemyAnimState = (self.__enemyAnimState + 1) % 25
        if self.__enemyAnimState / 5 == 0:
            self.updateImage(self.IMAGES["enemy1"])
        if self.__enemyAnimState / 5 == 1:
            self.updateImage(self.IMAGES["enemy2"])
        if self.__enemyAnimState / 5 == 2:
            self.updateImage(self.IMAGES["enemy3"])
        if self.__enemyAnimState / 5 == 3:
            self.updateImage(self.IMAGES["enemy4"])
        if self.__enemyAnimState / 5 == 4:
            self.updateImage(self.IMAGES["enemy5"])

    def updateWH(self, raw_image, direction, value, width, height):
        if direction == "H":
            self.position = (self.position[0] + value, self.position[1])
        if direction == "V":
            self.position = (self.position[0], self.position[1] + value)
        self.image = raw_image
        # Update the image to the specified width and height
        #self.image = pygame.transform.scale(self.image, (width, height))
        self.rect.center = self.position

    def updateY(self, value):
        self.position = (self.position[0], self.position[1] + value)
        self.rect.center = self.position