__author__ = 'Batchu Vishal'
import pygame
import os
from .onBoard import OnBoard


class enemy(OnBoard):
    """
    This class defines all our enemys.
    """

    def __init__(self, raw_image, position, _dir):
        OnBoard.__init__(self, raw_image, position)
        self.__enemyAnimState = 0  # Initialize animation state to 0
        self.IMAGES = {
            "enemy1": pygame.transform.scale(pygame.image.load(os.path.join(_dir, 'assets/enemy1.png')), (15, 15)).convert_alpha(),
            "enemy2": pygame.transform.scale(pygame.image.load(os.path.join(_dir, 'assets/enemy1.png')), (15, 15)).convert_alpha(),
            "enemy3": pygame.transform.scale(pygame.image.load(os.path.join(_dir, 'assets/enemy1.png')), (15, 15)).convert_alpha(),
            "enemy4": pygame.transform.scale(pygame.image.load(os.path.join(_dir, 'assets/enemy1.png')), (15, 15)).convert_alpha(),
            "enemy5": pygame.transform.scale(pygame.image.load(os.path.join(_dir, 'assets/enemy1.png')), (15, 15)).convert_alpha()
        }

    # Update the image of the enemy
    def updateImage(self, raw_image):
        self.image = raw_image

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
