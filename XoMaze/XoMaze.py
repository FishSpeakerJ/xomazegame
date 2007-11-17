import pygame
from pygame.locals import *
import sys
import os
from Maze import Maze
from Maze import Cell
from Hud import Hud
from GameTimer import GameTimer
import globals
from player.PlayerManager import PlayerManager

try:
	# if we're running on an evironment euivalent to the XO laptop
	from olpcgames import eventwrap
	emulatorMode = True
	width=1200.0
	height=825.0

except ImportError:
	# otherwise, assume a smaller resolution
	emulatorMode = False
	width=1024.0
	height=750.0

class XoMaze:
	def __init__(self):
		self.initScreen( width, height ) 
		self.initVariables()
		self.initPlayerManager()
		self.initSounds()
		self.pressedKeys = {}
		pygame.init()
		pygame.font.init()
		pygame.event.set_blocked( pygame.MOUSEMOTION )
		pygame.event.set_blocked( pygame.VIDEORESIZE )
		pygame.event.set_blocked( pygame.VIDEOEXPOSE )
		pygame.event.set_blocked( pygame.ACTIVEEVENT )
				
		#eventwrap.install()
		
	def initScreen( self, width, height ):
		"""Set the window Size"""
		# determine space available for board & hud
		boardWidth = width
		boardHeight = height-globals.hudHeight-globals.bottomMargin
		hudWidth = width
		hudHeight = globals.hudHeight
		
		"""Create the Screen"""
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('XoMaze')
		self.boardSurface = self.screen.subsurface( pygame.Rect( 0, hudHeight, boardWidth, boardHeight ))
		self.hudSurface = self.screen.subsurface( pygame.Rect( 0,0,hudWidth, hudHeight ))
		self.gameClock = GameTimer()
		self.hud = Hud( self )
		self.maze = Maze( self )


	def initVariables( self ):
		self.numberOfPlayers = 4
		
		if emulatorMode:
			# These are the directional keys on the laptop's joystick
			self.keysToDirections = globals.emulatorKeys
		else:
			# These are... wasd
			self.keysToDirections = globals.keyboardKeys

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
		updateVisuals = False
		event = pygame.event.wait()
		if event.type != globals.CLOCKTICK:
			updateVisuals = True
		keepGoing = self.processMessages( event)
		for event in pygame.event.get():
			keepGoing = self.processMessages( event )
			if keepGoing == False:
				return False
			if event.type != globals.CLOCKTICK:
				updateVisuals = True
		
		# update player movement
		for key, lastUpdateTime in self.pressedKeys.items():
			if lastUpdateTime != 0:
				self.playerManager.playerIdsToPlayers[ self.keysToDirections[key][0] ].move( self.keysToDirections[key][1], self.gameClock.getTime() - lastUpdateTime )
				self.pressedKeys[key] = self.gameClock.getTime()
				
		# if game timer is running, update stuff
		if updateVisuals and self.gameClock.isRunning():	
			# Do update the maze!
			self.maze.paint( self.boardSurface )		
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
		elif event.type == KEYUP: # (I assume we want key down, not up)
			# Handle any directional input
			if event.key in self.keysToDirections.keys():
				if event.key in self.pressedKeys:
					self.pressedKeys[event.key] = 0										
		elif event.type == KEYDOWN: # (I assume we want key down, not up)
			if event.key == K_ESCAPE:
				# TODO: Show a confirmation dialog maybe?
				return False			
			# Handle any directional input
			if event.key in self.keysToDirections.keys():
				self.pressedKeys[event.key] = self.gameClock.getTime()					
			if event.key == K_SPACE:
				# checkif this is relevant
				self.startNewGame(*globals.difficultyLevelToMazeSize[1])
			elif event.key == K_F1:
				# checkif this is relevant
				self.startNewGame(*globals.difficultyLevelToMazeSize[1])
			elif event.key == K_F2:
				# checkif this is relevant
				self.startNewGame(*globals.difficultyLevelToMazeSize[2])
			elif event.key == K_F3:
				# checkif this is relevant
				self.startNewGame(*globals.difficultyLevelToMazeSize[3])
						
				
				
				
		return True
		
	def startNewGame( self, xCellNum, yCellNum ):
		# clear EVERYTHING
		self.boardSurface.fill( (1.0, 1.0, 1.0) )
		#self.hud.reset()
		# create the new maze
		self.maze.initialize(xCellNum,yCellNum)
		# setup each player
		self.playerManager.reset()
		self.gameClock.start()

	def gameOver( self ):
		'''
		Everyone quit or everyone finished
		'''
		pass
		

