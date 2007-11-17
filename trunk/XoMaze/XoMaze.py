import pygame
from pygame.locals import *
import sys
#from olpcgames import eventwrap
from Maze import Maze
from Maze import Cell
from player.PlayerManager import PlayerManager


# Use this variable to determine if we're running in the emulator or not
emulatorMode = False

class XoMaze:
	def __init__(self, width=1200,height=825):
		self.initScreen( width, height ) 
		self.maze = Maze()
		self.players = {}
		pygame.init()
		pygame.event.set_blocked( pygame.MOUSEMOTION )
		#eventwrap.install()

	def processMessages( self, event ):
		# Gotta have this if we want to exit nicely
			if event.type == QUIT:
				return False
			elif event.type == KEYDOWN: # (I assume we want key down, not up)
				if event.key == K_ESCAPE:
					# TODO: Show a confirmation dialog maybe?
					return False
				
				# Handle any directional input
				for key, value in self.keysToDirections.items():
					if event.key == getattr( pygame.locals, key ):
						# Let's assume player ID 0 is me, the main player.
						self.playerManager.playerIdsToPlayers[ 0 ].move( value )

	def initScreen( self, width, height ):
		"""Set the window Size"""
		self.width = width
		self.height = height
		"""Create the Screen"""
		self.screen = pygame.display.set_mode( (self.width, self.height) )
		pygame.display.set_caption("XoMaze")
		
		
	def startNewGame( self ):
		# create the new maze
		# setup each player
		# start game time
		pass
		
	def __init__(self, width=1200,height=825):
		self.initScreen( width, height )
		self.initVariables()
		self.initPlayerManager()
		self.maze = Maze()
		pygame.init()
		#eventwrap.install()

	def initScreen( self, width, height ):
		"""Set the window Size"""
		self.width = width
		self.height = height
		"""Create the Screen"""
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('XoMaze')

	def initVariables( self ):
		self.numberOfPlayers = 1
		
		if emulatorMode:
			# These are the directional keys on the laptop's joystick
			self.keysToDirections = {
				"K_KP8" : 0,
				"K_KP6" : 1,
				"K_KP2" : 2,
				"K_KP4" : 3,
			}
		else:
			# These are... wasd
			self.keysToDirections = {
				"K_w" : 0,
				"K_d" : 1,
				"K_s" : 2,
				"K_a" : 3,
			}

	def initPlayerManager( self ):
		self.playerManager = PlayerManager( self )

	def update( self ):
		'''
		This is the main game loop.
		
		'''
		# Do some stuff!
		self.maze.paint( self.screen, 0, 0, 1000, 700 )
		
		# Render that sucker
		pygame.display.update()
		
		# Event Handling (controls)
		# sleep if there is no event
		firstNewEvent = pygame.event.wait()
		self.processMessages( firstNewEvent)		
		for event in pygame.event.get():
			self.processMessages( event )
					
		# Keep looping!
		return True
