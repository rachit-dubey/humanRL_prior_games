__author__ = 'Rachit Dubey'
import pygame
import sys
from pygame.constants import K_a, K_d, K_SPACE, K_w, K_s, QUIT, KEYDOWN
from .board import Board
#from ..base import base
#from ple.games import base
from ple.games.base.pygamewrapper import PyGameWrapper
import numpy as np
import os


class originalgame_blank_stochastic(PyGameWrapper):

	def __init__(self):
		"""
		Parameters
		----------
		None

		"""
		self.height = 150 #modify height accordingly based on how long the game level is, orignal was 230*230
		self.width = 230
		self.status = 2
		actions = {
			"left": K_a,
			"right": K_d,
			"jump": K_SPACE,
			"up": K_w,
			"down": K_s
		}

		PyGameWrapper.__init__(
			self, self.width, self.height, actions=actions)

		self.rewards = {
			"positive": 0, 
			"win": 1,
			"negative": 0, 
			"tick": 0
		}
		self.allowed_fps = 30
		self._dir = os.path.dirname(os.path.abspath(__file__))

		self.IMAGES = {
			"right": pygame.image.load(os.path.join(self._dir, 'assets/right.png')),
			"right2": pygame.image.load(os.path.join(self._dir, 'assets/right2.png')),
			"left": pygame.image.load(os.path.join(self._dir, 'assets/left.png')),
			"left2": pygame.image.load(os.path.join(self._dir, 'assets/left2.png')),
			"still": pygame.image.load(os.path.join(self._dir, 'assets/still.png'))
		}

	def init(self):
	
		# Create a new instance of the Board class
		self.newGame = Board(
			self.width,
			self.height,
			self.rewards,
			self._dir)

		# Assign groups from the Board instance that was created
		self.playerGroup = self.newGame.playerGroup

		self.numactions = 0
	def getScore(self):
		return self.newGame.score

	def game_over(self):
		if(self.numactions > 2000 or self.newGame.lives <=0): #max episode length is 2000 steps. 
			self.numactions = 0
			return 1
		else:
			return 0

	def position(self): #function to simply return position of Player
		return self.newGame.Players[0].getPosition()

	def step(self, dt):

		self.numactions = self.numactions+1 #check number of actions taken by agent so far
		self.newGame.score += self.rewards["tick"]
		# This is where the actual game is run
		# Get the appropriate groups
		self.wallGroup = self.newGame.wallGroup #wall and ladder added to step function as these are also recreated
		self.ladderGroup = self.newGame.ladderGroup
		self.enemyGroup = self.newGame.enemyGroup
		self.enemyGroup2 = self.newGame.enemyGroup2
		# To check collisions below, we move the player downwards then check
		# and move him back to his original location
		self.newGame.Players[0].updateY(2)
		self.laddersCollidedBelow = self.newGame.Players[
			0].checkCollision(self.ladderGroup)
		self.wallsCollidedBelow = self.newGame.Players[
			0].checkCollision(self.wallGroup)
		self.newGame.Players[0].updateY(-2)

		# To check for collisions above, we move the player up then check and
		# then move him back down
		self.newGame.Players[0].updateY(-2)
		self.wallsCollidedAbove = self.newGame.Players[
			0].checkCollision(self.wallGroup)
		self.newGame.Players[0].updateY(2)

		# Sets the onLadder state of the player
		self.newGame.ladderCheck(
			self.laddersCollidedBelow,
			self.wallsCollidedBelow,
			self.wallsCollidedAbove)

		for event in pygame.event.get():
			# Exit to desktop
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				# Get the ladders collided with the player
				self.laddersCollidedExact = self.newGame.Players[
					0].checkCollision(self.ladderGroup)
				if (event.key == self.actions["jump"] and self.newGame.Players[0].onLadder == 0) or (
						event.key == self.actions["up"] and self.laddersCollidedExact):
					# Set the player to move up
					self.direction = 2
					if self.newGame.Players[
							0].isJumping == 0 and self.wallsCollidedBelow:
						# We can make the player jump and set his
						# currentJumpSpeed
						self.newGame.Players[0].isJumping = 1
						self.newGame.Players[0].currentJumpSpeed = 7

				if event.key == self.actions["right"]:
					if self.newGame.direction != 4:
						self.newGame.direction = 4
						self.newGame.cycles = -1  # Reset cycles
					self.newGame.cycles = (self.newGame.cycles + 1) % 4
					if self.newGame.cycles < 2:
						# Display the first image for half the cycles
						self.newGame.Players[0].updateWH(self.IMAGES["right"], "H",
														 self.newGame.Players[0].getSpeed(), 15, 15)
					else:
						# Display the second image for half the cycles
						self.newGame.Players[0].updateWH(self.IMAGES["right2"], "H",
														 self.newGame.Players[0].getSpeed(), 15, 15)
					wallsCollidedExact = self.newGame.Players[
						0].checkCollision(self.wallGroup)
					if wallsCollidedExact:
						# If we have collided a wall, move the player back to
						# where he was in the last state
						self.newGame.Players[0].updateWH(self.IMAGES["right"], "H",
														 -self.newGame.Players[0].getSpeed(), 15, 15)

				if event.key == self.actions["left"]:
					if self.newGame.direction != 3:
						self.newGame.direction = 3
						self.newGame.cycles = -1  # Reset cycles
					self.newGame.cycles = (self.newGame.cycles + 1) % 4
					if self.newGame.cycles < 2:
						# Display the first image for half the cycles
						self.newGame.Players[0].updateWH(self.IMAGES["left"], "H",
														 -self.newGame.Players[0].getSpeed(), 15, 15)
					else:
						# Display the second image for half the cycles
						self.newGame.Players[0].updateWH(self.IMAGES["left2"], "H",
														 -self.newGame.Players[0].getSpeed(), 15, 15)
					wallsCollidedExact = self.newGame.Players[
						0].checkCollision(self.wallGroup)
					if wallsCollidedExact:
						# If we have collided a wall, move the player back to
						# where he was in the last state
						self.newGame.Players[0].updateWH(self.IMAGES["left"], "H",
														 self.newGame.Players[0].getSpeed(), 15, 15)

				# If we are on a ladder, then we can move up
				if event.key == self.actions[
                        "up"] and self.newGame.Players[0].onLadder:
					self.newGame.Players[0].updateWH(self.IMAGES["still"], "V",
													 -self.newGame.Players[0].getSpeed() / 2, 15, 15)
					if len(self.newGame.Players[0].checkCollision(self.ladderGroup)) == 0 or len(
							self.newGame.Players[0].checkCollision(self.wallGroup)) != 0:
						self.newGame.Players[0].updateWH(self.IMAGES["still"], "V",
														 self.newGame.Players[0].getSpeed() / 2, 15, 15)

				# If we are on a ladder, then we can move down
				if event.key == self.actions[
                        "down"] and self.newGame.Players[0].onLadder:
					self.newGame.Players[0].updateWH(self.IMAGES["still"], "V",
													 self.newGame.Players[0].getSpeed() / 2, 15, 15)

		# Update the player's position and process his jump if he is jumping
		self.newGame.Players[0].continuousUpdate(
			self.wallGroup, self.ladderGroup)

		for enemy in self.enemyGroup:
			enemy.moveEnemy()

		# Redraws all our instances onto the screen
		self.newGame.redrawScreen(self.screen, self.width, self.height)

		#enemy encounter
		enemysCollected = pygame.sprite.spritecollide(
			self.newGame.Players[0], self.enemyGroup, True)
		enemysCollected2 = pygame.sprite.spritecollide(
			self.newGame.Players[0], self.enemyGroup2, True)
		self.newGame.enemyCheck2(enemysCollected2)
		self.newGame.enemyCheck(enemysCollected)

		# Check if you have reached the princess
		self.status = self.newGame.checkVictory(self.status)
if __name__ == "__main__":
	pygame.init()
	# Instantiate the Game class and run the game
	game = originalgame_blank_stochastic()
	game.screen = pygame.display.set_mode(game.getScreenDims(), 0, 32)
	game.clock = pygame.time.Clock()
	game.rng = np.random.RandomState(24)
	game.init()
	
	while True:
		dt = game.clock.tick_busy_loop(30)
		game.step(dt)
		#print(game.game_over())
		pygame.display.update()
