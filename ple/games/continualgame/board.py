__author__ = 'Rachit Dubey'
import pygame
import math
import sys
import os
import numpy as np
from .person import Person
from .onBoard import OnBoard
from .enemy import enemy
from .player import Player
from random import randint

#This game doesn't have any default location of princess or robot sprite - they can be anywhere depending on the map being used (their location are directly read from the map - 20 for princess, 21 for robot)

class Board(object):
    '''
    This class defines our gameboard.
    A gameboard contains everthing related to our game on it like our characters, walls, ladders, enemies etc
    The generation of the level also happens in this class.
    '''

    def __init__(self, width, height, rewards, _dir):
        self.__width = width
        self.__actHeight = height
        self.__height = self.__actHeight + 10
        self.score = 0
        self.rewards = rewards
        self.cycles = 0  # For the characters animation
        self.direction = 0
        self._dir = _dir
        
        #self.playerPosition = (120, 190)
        
        self.IMAGES = {
            "still": pygame.image.load(os.path.join(_dir, 'assets/still.png')).convert_alpha(),
            "princess": pygame.image.load(os.path.join(_dir, 'assets/princess.png')).convert_alpha(),
            "enemy1": pygame.image.load(os.path.join(_dir, 'assets/enemy1.png')).convert_alpha(),
            "enemy2": pygame.image.load(os.path.join(_dir, 'assets/fire.png')).convert_alpha(),
            "wood_block": pygame.image.load(os.path.join(_dir, 'assets/wood_block.png')).convert_alpha(),
            "wood_block2": pygame.image.load(os.path.join(_dir, 'assets/wood_block2.png')).convert_alpha(),
            "wood_block3": pygame.image.load(os.path.join(_dir, 'assets/wood_block3.png')).convert_alpha(),
            "wood_block4": pygame.image.load(os.path.join(_dir, 'assets/wood_block4.png')).convert_alpha(),
            "wood_block5": pygame.image.load(os.path.join(_dir, 'assets/wood_block5.png')).convert_alpha(),
            "boundary": pygame.image.load(os.path.join(_dir, 'assets/boundary.png')).convert_alpha(),            
            "ladder": pygame.image.load(os.path.join(_dir, 'assets/ladder.png')).convert_alpha()
        }

        self.white = (255, 255, 255)

        '''
        The map is essentially an array of 30x80 in which we store what each block on our map is.
        1 represents a wall, 2 for a ladder and 3 for a enemy.
        '''
        self.map = []
        # These are the arrays in which we store our instances of different
        # classes
        self.Players = []
        self.Allies = []
        self.enemys = []
        self.enemys2 = []
        self.Walls = []
        self.Ladders = []
        self.Boards = []

        # Resets the above groups and initializes the game for us
        self.resetGroups()

        # Initialize the instance groups which we use to display our instances
        # on the screen
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.ladderGroup = pygame.sprite.RenderPlain(self.Ladders)
        self.enemyGroup = pygame.sprite.RenderPlain(self.enemys)
        self.enemyGroup2 = pygame.sprite.RenderPlain(self.enemys2)
        self.allyGroup = pygame.sprite.RenderPlain(self.Allies)

    def resetGroups(self):
        self.score = 0
        self.lives = 1
        self.map = []  # We will create the map again when we reset the game
        self.Players = [] #initial position of the player
        self.Allies = [] 
        self.enemys = []
        self.enemys2 = []
        self.Walls = []
        self.Ladders = []
        self.initializeGame()  # This initializes the game and generates our map
        self.createGroups()  # This creates the instance groups

    def resetGroups2(self):
        for wall in self.Walls: #need to kill wall and ladder sprites when we load a new map
                    wall.kill()
        for ladder in self.Ladders:
                     ladder.kill()
        self.map = []  # We will create the map again when we reset the game
        self.Players = []
        self.Allies = []
        self.enemys = []
        self.enemys2 = []
        self.Walls = []
        self.Ladders = []   
        self.initializeGame()  # This initializes the game and generates our map 
        self.createGroups()

    def populateMap(self):
        j = randint(1,120)
        s = 'curriculum_maps_3/'+str(j)+".txt"
        print(s)
        self.map = np.loadtxt(s, dtype='i', delimiter=',') #load new map everytime        
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 1:
                    # Add a wall at that position
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["wood_block"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))
                elif self.map[x][y] == 21:
                    #add player at that location
                    self.Players.append(
                        Player(
                            self.IMAGES["still"], 
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2), 
                            15, 15))
                    self.playerPosition = (y * 15 + 15 / 2, x * 15 + 15 / 2) #also set player position
                elif self.map[x][y] == 20:
                    #add princess at that location
                    self.Allies.append(
                        Person(
                            self.IMAGES["princess"], 
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2), 
                            18, 23))
                elif self.map[x][y] == 2:
                    # Add a ladder at that position
                    self.Ladders.append(
                        OnBoard(
                            self.IMAGES["ladder"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))
                elif self.map[x][y] == 11:
                    # Add the enemy to our enemy list
                    self.enemys.append(
                        enemy(
                            self.IMAGES["enemy1"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2),
                             self._dir))
                elif self.map[x][y] == 12:
                    # Add the enemy to our enemy list
                    self.enemys2.append(
                        enemy(
                            self.IMAGES["enemy2"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2),
                             self._dir))
                # Add a wall at that position
                elif self.map[x][y] == 4:
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["wood_block2"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))                 
                elif self.map[x][y] == 5:
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["wood_block3"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))
                elif self.map[x][y] == 6:
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["wood_block4"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2))) 
                elif self.map[x][y] == 7:
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["wood_block5"],
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2))) 
                elif self.map[x][y] == 9:
                    self.Walls.append(
                        OnBoard(
                            self.IMAGES["boundary"], #9 is to create boundary walls so that player doesn't cross over the game
                            (y * 15 + 15 / 2,
                             x * 15 + 15 / 2)))

    # Check if the player is on a ladder or not
    def ladderCheck(self, laddersCollidedBelow,
                    wallsCollidedBelow, wallsCollidedAbove):
        if laddersCollidedBelow and len(wallsCollidedBelow) == 0:
            for ladder in laddersCollidedBelow:
                if ladder.getPosition()[1] >= self.Players[0].getPosition()[1]:
                    self.Players[0].onLadder = 1
                    self.Players[0].isJumping = 0
                    # Move the player down if he collides a wall above
                    if wallsCollidedAbove:
                        self.Players[0].updateY(3)
        else:
            self.Players[0].onLadder = 0

    # Check for enemys collided and add the appropriate score
    def enemyCheck(self, enemysCollected):
        for enemy in enemysCollected:
            if(self.Players[0].getPosition()[1]+7 < enemy.getPosition()[1]):
                 enemy.kill()
            else:
                 #self.Players[0].setPosition(self.playerPosition) #player dies when reaches enemy 
                 self.lives = 0
                 status = 0
                 # Update the enemy group since we modified the enemy list
                 self.resetGroups2()
    
    
    def enemyCheck2(self,enemysCollected2):
        for enemys2 in enemysCollected2:
            #self.Players[0].setPosition(self.playerPosition) #player dies when reaches enemy 
            self.lives = 0            
            #intialize game again to load a new map
            self.resetGroups2()
    
    # Check if the player wins
    def checkVictory(self,status):
        # If you touch the princess you
        # win!
        if self.Players[0].checkCollision(self.allyGroup):

            self.score += self.rewards["win"]
            self.lives = 0		
            status = 1
            #self.Players[0].setPosition(self.playerPosition)
            self.resetGroups2()
        return status

    # Redraws the entire game screen for us
    def redrawScreen(self, screen, width, height):
        screen.fill((40, 20, 0))  # Fill it with black
        # Draw all our groups on the background
        self.ladderGroup.draw(screen)
        self.playerGroup.draw(screen)
        self.enemyGroup2.draw(screen)
        self.enemyGroup.draw(screen)
        self.wallGroup.draw(screen)
        self.allyGroup.draw(screen)

    # Update all the groups from their corresponding lists
    def createGroups(self):
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.ladderGroup = pygame.sprite.RenderPlain(self.Ladders)
        self.enemyGroup = pygame.sprite.RenderPlain(self.enemys)
        self.enemyGroup2 = pygame.sprite.RenderPlain(self.enemys2)
        self.allyGroup = pygame.sprite.RenderPlain(self.Allies)

    
    def initializeGame(self):
        self.populateMap()
        self.createGroups()
