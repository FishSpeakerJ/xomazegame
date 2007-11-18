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
import time

try:
	# if we're running on an evironment euivalent to the XO laptop
	import olpcgames
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
		self.initScreen( int( width ), int( height ) ) 
		self.initVariables()
		self.initPlayerManager()
		self.initSounds()
		self.pressedKeys = []
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

		self.fogOfWarSurface = pygame.Surface( (boardWidth, boardHeight) )

	def initVariables( self ):
		self.numberOfPlayers = 4
		self.lastTime = time.time()
		
		if emulatorMode:
			# These are the directional keys on the laptop's joystick
			self.keysToDirections = globals.emulatorKeys
		else:
			# These are... wasd
			self.keysToDirections = globals.keyboardKeys
			
		self.fogOfWarPlayerIDsToPointsToDraw = {}
		self.fogOfWarPlayerIDsToLastPoints = {}
		for i in range( self.numberOfPlayers ):
			self.fogOfWarPlayerIDsToPointsToDraw[i] = []
			self.fogOfWarPlayerIDsToLastPoints[i] = None
		self.fogOfWarEnabled = True
		self.fogOfWarKeyColor = (0, 255, 0)
		self.fogOfWarRadius = 60
		self.fogOfWarSurface.set_colorkey( self.fogOfWarKeyColor )
		self.fogOfWarImage = self.loadImage( "cloud.png" )

		# DEBUG:
#		self.fogOfWarPlayerIDsToPointsToDraw[0] = [(100, 100), (200, 100), (300, 300), (500, 600), (600, 500)]

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
			#"hitWall" : None,
		}
		
		for soundName in self.soundNamesToSounds.keys():
			fullname = os.path.join( 'data/sounds', soundName + ".ogg" )
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
		t = time.time()
		dt = t - self.lastTime
		self.lastTime = t
		
		# check to see if game is over
		
		
		# Event Handling (controls)
		# sleep if there is no event
		updateVisuals = True # Don't we always want to update visuals?!
		event = pygame.event.wait()

		keepGoing = self.processMessages( event)
		for event in pygame.event.get():
			keepGoing = self.processMessages( event )
			if keepGoing == False:
				return False
		
		# update player movement
		for key in self.pressedKeys:
			self.playerManager.playerIdsToPlayers[ self.keysToDirections[key][0] ].move( self.keysToDirections[key][1], dt )
				
		# if game timer is running, update stuff
		if updateVisuals and self.gameClock.isRunning():
			# Update the maze!
			self.maze.paint( self.boardSurface )

			# Draw fog of war into it's own surface
#			dirtyRects = []
			for id in self.playerManager.playerIdsToPlayers:
				pointsToDraw = self.fogOfWarPlayerIDsToPointsToDraw[id]
				if len( pointsToDraw ) > 0:
					lastPoint = self.fogOfWarPlayerIDsToLastPoints[id]
					for point in pointsToDraw:
						pygame.draw.circle( self.fogOfWarSurface, self.fogOfWarKeyColor, point, self.fogOfWarRadius )
#						dirtyRects.append( pygame.Rect( point[0] - self.fogOfWarRadius, point[1] - self.fogOfWarRadius, 2*self.fogOfWarRadius, 2*self.fogOfWarRadius ) )
						if lastPoint is not None:
							pygame.draw.line( self.fogOfWarSurface, self.fogOfWarKeyColor, lastPoint, point, self.fogOfWarRadius )
						lastPoint = point
					self.fogOfWarPlayerIDsToLastPoints[id] = lastPoint
					self.fogOfWarPlayerIDsToPointsToDraw[id] = []

#			if len( dirtyRects ) > 1:
#				dirtyRect = dirtyRects[0].unionall( dirtyRects[1:] )
#			elif len( dirtyRects ) == 1:
#				dirtyRect = dirtyRects[0]
#			else:
#				dirtyRect = None

			# Blit fog of war onto board
#			if dirtyRect is not None:
#				self.boardSurface.blit( self.fogOfWarSurface, (0, 0), dirtyRect )
#			else:
#				self.boardSurface.blit( self.fogOfWarSurface, (0, 0) )
			if self.fogOfWarEnabled:
				self.boardSurface.blit( self.fogOfWarSurface, (0, 0) )

			# Render that sucker
			pygame.display.update()						
		self.hud.update()
		# Keep looping!
		return keepGoing
		
	def processMessages( self, event ):
		# Gotta have this if we want to exit nicely
		if event.type == QUIT:
			return False
#		elif event.type == globals.CLOCKTICK:
#			self.gameClock.update()
###				print self.gameClock.getTime()
		elif event.type == KEYUP:
			# Handle any directional input
			if event.key in self.pressedKeys:
				self.pressedKeys.remove( event.key )
		elif event.type == KEYDOWN: # (I assume we want key down, not up)
			if event.key == K_ESCAPE:
				# TODO: Show a confirmation dialog maybe?
				return False			
			# Handle any directional input
			if event.key in self.keysToDirections.keys() and self.gameClock.isRunning():
				self.pressedKeys.append( event.key )
			if event.key == K_SPACE:
				# checkif this is relevant
				self.startNewGame(*globals.difficultyLevelToMazeSize[1])
			elif event.key == K_1:
				# checkif this is relevant
				self.startNewGame(*globals.difficultyLevelToMazeSize[1])
			elif event.key == K_2:
				# checkif this is relevant
				self.startNewGame(*globals.difficultyLevelToMazeSize[2])
			elif event.key == K_3:
				# checkif this is relevant
				self.startNewGame(*globals.difficultyLevelToMazeSize[3])
			elif event.key == K_f:
				self.fogOfWarEnabled = not self.fogOfWarEnabled
				
		return True

	def onPlayerPositionChange( self, playerID, position ):
		# mark points to be updated for fog of war
		try:
			x, y = position
			newX = self.maze.mapX( x )
			newY = self.maze.mapY( y )
			self.fogOfWarPlayerIDsToPointsToDraw[playerID].append( (newX, newY) )
		except:
			print "can't update fog of war for player position", position
			import traceback
			traceback.print_exc()

	def startNewGame( self, xCellNum, yCellNum ):
		# clear EVERYTHING
		self.boardSurface.fill( (1.0, 1.0, 1.0) )
#		self.fogOfWarSurface.fill( (0.0, 0.0, 0.0) )
		self.fogOfWarSurface.blit( self.fogOfWarImage, (0.0, 0.0) )
		#self.hud.reset()
		# create the new maze
		self.maze.initialize(xCellNum,yCellNum)
		# setup each player
		self.playerManager.reset()

		self.maze.constructRandom()

		# Unfog entrance and exit
		self.fogOfWarPlayerIDsToPointsToDraw = {}
		self.fogOfWarPlayerIDsToLastPoints = {}
		for id in self.playerManager.playerIdsToPlayers:
			player = self.playerManager.playerIdsToPlayers[id]
			x, y = player.position
			gx = self.maze.mapX( x )
			gy = self.maze.mapY( y )
			pygame.draw.circle( self.fogOfWarSurface, self.fogOfWarKeyColor, (gx, gy), self.fogOfWarRadius )

			endX, endY = self.maze.mapCell( player.endCell, 0.5 )
			pygame.draw.circle( self.fogOfWarSurface, self.fogOfWarKeyColor, (endX, endY), self.fogOfWarRadius )

			self.fogOfWarPlayerIDsToPointsToDraw[id] = []
			self.fogOfWarPlayerIDsToLastPoints[id] = None
		
		self.gameClock.start()

	def gameOver( self ):
		'''
		Everyone quit or everyone finished
		'''
		pass

	def loadImage( self, name, colorkey=None ):
		fullname = os.path.join( "data", name )
		image = pygame.image.load( fullname )
		image = image.convert()
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at( (0, 0) )
			image.set_colorkey( colorkey )
		return image

