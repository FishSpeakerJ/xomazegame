import pygame
from pygame.locals import *
import sys
import os
from Maze import Maze
from Maze import Cell
from GameTimer import GameTimer
import globals
from player.PlayerManager import PlayerManager

try:
	from olpcgames import eventwrap
	emulatorMode = True
except ImportError:
	# Use this variable to determine if we're running in the emulator or not
	emulatorMode = False

class XoMaze:
	def __init__(self, width=1200,height=825):
		self.initScreen( width, height ) 
		self.initVariables()
		self.initPlayerManager()
		self.initSounds()
		pygame.init()
		pygame.event.set_blocked( pygame.MOUSEMOTION )
		#eventwrap.install()
		
	def initScreen( self, width, height ):
		"""Set the window Size"""
		# determine space available for board & hud
		boardWidth = width
		boardHeight = height*0.9
		hudWidth = width
		hudHeight = height - boardHeight
		
		"""Create the Screen"""
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('XoMaze')
		self.board = self.screen.subsurface( pygame.Rect( 0, hudHeight, boardWidth, boardHeight ))
		self.hud = self.screen.subsurface( pygame.Rect( 0,0,hudWidth, hudHeight ))
		self.initHud()
		self.maze = Maze( self )
		self.gameClock = GameTimer()


	def initVariables( self ):
		self.numberOfPlayers = 4
		
		if emulatorMode:
			# These are the directional keys on the laptop's joystick
			self.keysToDirections = {
				"K_KP8" : [ 0, 0, ],
				"K_KP6" : [ 0, 1, ],
				"K_KP2" : [ 0, 2, ],
				"K_KP4" : [ 0, 3, ],
			}
		else:
			# These are... wasd
			self.keysToDirections = {
				"K_w" : [ 0, 0, ],
				"K_d" : [ 0, 1, ],
				"K_s" : [ 0, 2, ],
				"K_a" : [ 0, 3, ],
				"K_UP" : [ 1, 0, ],
				"K_RIGHT" : [ 1, 1, ],
				"K_DOWN" : [ 1, 2, ],
				"K_LEFT" : [ 1, 3, ],
			}

	def initHud( self ):
		pass

	def initPlayerManager( self ):
		self.playerManager = PlayerManager( self )
		
	def initSounds( self ):
		if not pygame.mixer or not pygame.mixer.get_init():
			print "Sound can't initialize!"
			self.hasSound = False
			return
		else:
			self.hasSound = True
	
		# Add any sounds you want here!!
		self.soundNamesToSounds = {
			"hitWall" : None,
		}
		
		for soundName in self.soundNamesToSounds.keys():
			fullname = os.path.join( 'data\sounds', soundName + ".ogg" )
			try:
			    sound = pygame.mixer.Sound( fullname )
			except pygame.error, message:
			    print 'Cannot load sound:', fullname
			    raise SystemExit, message
			self.soundNamesToSounds[ soundName ] = sound

	def update( self ):
		'''
		This is the main game loop.
		
		'''
		# check to see if game is over
		
		
		# Event Handling (controls)
		# sleep if there is no event
		firstNewEvent = pygame.event.wait()
		keepGoing = self.processMessages( firstNewEvent)		
		for event in pygame.event.get():
			self.processMessages( event )
		
		# Do update the maze!
		self.maze.paint( self.board )		
		# Render that sucker
		pygame.display.update()
					
		# Keep looping!
		return keepGoing
		
	def processMessages( self, event ):
		# Gotta have this if we want to exit nicely
		if event.type == QUIT:
			return False
		elif event.type == globals.CLOCKTICK:
			self.gameClock.update()
#				print self.gameClock.getTime()
		elif event.type == KEYDOWN: # (I assume we want key down, not up)
			if event.key == K_ESCAPE:
				# TODO: Show a confirmation dialog maybe?
				return False
			
			# Handle any directional input
			for key, value in self.keysToDirections.items():
				if event.key == getattr( pygame.locals, key ):
					# Let's assume player ID 0 is me, the main player.
					self.playerManager.playerIdsToPlayers[ value[0] ].move( value[1] )
					
			if event.key == K_SPACE:
				# checkif this is relevant
				self.startNewGame()
		return True
		
	def startNewGame( self ):
		# clear EVERYTHING
		self.board.fill( (1.0, 1.0, 1.0) )
		#self.hud.reset()
		# create the new maze
		self.maze.constructRandom()
		# setup each player
		self.playerManager.reset()
		self.gameClock.start()

	def gameOver( self ):
		'''
		Everyone quit or everyone finished
		'''
		pass
		
