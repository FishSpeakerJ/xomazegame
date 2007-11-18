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
from Scheduler import Scheduler

try:
	# if we're running on an evironment euivalent to the XO laptop
	import olpcgames
	emulatorMode = True
	graphicsPrefix = "xo"
	width=1200.0
	height=825.0

except ImportError:
	# otherwise, assume a smaller resolution
	emulatorMode = False
	graphicsPrefix = "desktop"
	width=1024.0
	height=750.0

class XoMaze:
	def __init__(self):
		self.initScreen( int( width ), int( height ) ) 
		self.initVariables()
		self.initPlayerManager()
		self.initSounds()
		self.mazeComplexityLevel = 2
		pygame.init()
		pygame.font.init()
		pygame.event.set_blocked( pygame.MOUSEMOTION )
		pygame.event.set_blocked( pygame.VIDEORESIZE )
		pygame.event.set_blocked( pygame.VIDEOEXPOSE )
		pygame.event.set_blocked( pygame.ACTIVEEVENT )

		self.scheduler = Scheduler( self )

		pygame.time.set_timer( globals.CLOCKTICK, globals.clockSleepTime )

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
		self.showTitleScreen()
		# show title screen
		

	def showTitleScreen( self ):
		# clear to right color
		self.screen.fill( (72, 70, 70) )

		# show title
		self.titleImage = self.loadImage( "title.png" )		
		# Create a rectangle
		imageRect = self.titleImage.get_rect()
		# Center the rectangle
		imageRect.centerx = self.screen.get_rect().centerx
		imageRect.centery = self.titleImage.get_height() + 10
		self.screen.blit( self.titleImage, imageRect )

		# show spacebar press anim
		
		
		# show directions		
		self.directionsImage = self.loadImage( "%s_startDirections.png" % graphicsPrefix, (0, 255, 0) )		
		if self.screen.get_width() < self.directionsImage.get_width() + 20:
			self.directionsImage = pygame.transform.scale(self.directionsImage, (self.directionsImage.get_width()*0.8, self.directionsImage.get_height()*0.8))
		# Create a rectangle
		imageRect = self.directionsImage.get_rect()		
		# Center the rectangle
		imageRect.centerx = self.screen.get_rect().centerx
		imageRect.centery = self.screen.get_height() - self.directionsImage.get_height()/2.0 - 20		
		self.screen.blit( self.directionsImage, imageRect )
		
		
		
		
	def initVariables( self ):
		self.isGameRunning = False
		
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
		self.fogOfWarStartRadius = 600.0
		self.fogOfWarGameOverRadius = 800.0
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
		self.soundNamesToSounds = { "gameOver" : None, "frogOfWar" : None, "trumpet" : None, "start" : None }
		for i in range( 4 ):
			self.soundNamesToSounds[ "signalEnd%d" % i ] = None
			self.soundNamesToSounds[ "signalFound%d" % i ] = None
			self.soundNamesToSounds[ "signalHead%d" % i ] = None
			self.soundNamesToSounds[ "corkPop%d" % i ] = None
		
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
		t = time.time()
		dt = t - self.lastTime
		self.lastTime = t

		self.scheduler.update()
		
		# check to see if game is over
		
		
		# Event Handling (controls)
		# sleep if there is no event
		event = pygame.event.wait()

		keepGoing = True
		for event in pygame.event.get():
			keepGoing = self.processMessages( event )
			if keepGoing == False:
				return False

		# update player movement
		if self.gameClock.isRunning:
			pressedKeys = pygame.key.get_pressed()
			for key in self.keysToDirections.keys():
				# check if key is pressed
				if pressedKeys[key] == True:					
					self.playerManager.playerIdsToPlayers[ self.keysToDirections[key][0] ].move( self.keysToDirections[key][1], dt )

		# Update the maze!
		if self.isGameRunning:
			self.maze.paint( self.boardSurface )
	
			# Draw fog of war into it's own surface
			for id in self.playerManager.playerIdsToPlayers:
				pointsToDraw = self.fogOfWarPlayerIDsToPointsToDraw[id]
				if len( pointsToDraw ) > 0:
					lastPoint = self.fogOfWarPlayerIDsToLastPoints[id]
					for point in pointsToDraw:
						pygame.draw.circle( self.fogOfWarSurface, self.fogOfWarKeyColor, point, self.fogOfWarRadius )
						if lastPoint is not None:
							pygame.draw.line( self.fogOfWarSurface, self.fogOfWarKeyColor, lastPoint, point, self.fogOfWarRadius )
						lastPoint = point
					self.fogOfWarPlayerIDsToLastPoints[id] = lastPoint
					self.fogOfWarPlayerIDsToPointsToDraw[id] = []
	
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
		elif event.type == KEYDOWN: # (I assume we want key down, not up)
			if event.key == K_ESCAPE:
				# TODO: Show a confirmation dialog maybe?
				return False			
			if event.key == K_n and (pygame.key.get_pressed()[K_RCTRL] or pygame.key.get_pressed()[K_LCTRL]):
				self.startNewGame(*globals.difficultyLevelToMazeSize[self.mazeComplexityLevel])
			elif event.key == K_f and (pygame.key.get_pressed()[K_RCTRL] or pygame.key.get_pressed()[K_LCTRL]):
				self.fogOfWarEnabled = not self.fogOfWarEnabled
			elif event.key == K_x and (pygame.key.get_pressed()[K_RCTRL] or pygame.key.get_pressed()[K_LCTRL]):
				self.gameOver()
			elif event.key == K_1:
				self.mazeComplexityLevel = 1
			elif event.key == K_2:
				self.mazeComplexityLevel = 2
			elif event.key == K_3:
				self.mazeComplexityLevel = 3
			elif event.key == K_4:
				self.mazeComplexityLevel = 4

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
		# make sure gameClock is stopped and reset
		self.gameClock.stop()
		self.gameClock.reset()
		
		# clear EVERYTHING
		self.boardSurface.fill( (1.0, 1.0, 1.0) )
		#self.hud.reset()
		# create the new maze
		self.maze.initialize(xCellNum,yCellNum)
		# setup each player
		self.playerManager.reset()

		self.maze.constructRandom()
		self.maze.paint( self.boardSurface )

		# Unfog entrance and exit
		self.fogOfWarPlayerIDsToPointsToDraw = {}
		self.fogOfWarPlayerIDsToLastPoints = {}
		for id in self.playerManager.playerIdsToPlayers:
			self.fogOfWarPlayerIDsToPointsToDraw[id] = []
			self.fogOfWarPlayerIDsToLastPoints[id] = None
		self._fogOfWarStartPoints = None
		self.fogOfWarSurface.fill( self.fogOfWarKeyColor )
		fogDuration = 2.0
		headsDuration = 1.5
		self.scheduler.doInterval( fogDuration, self.enterFogOfWar, waitBefore=0.0 )
		self.scheduler.doInterval( headsDuration, self.maze.handleHeadsRollingAnimation, waitBefore=fogDuration )
		self.scheduler.doLater( fogDuration + headsDuration, self.gameClock.start )
		if self.hasSound:
			self.scheduler.doLater( fogDuration + headsDuration, self.soundNamesToSounds[ "start" ].play )

		self.isGameRunning = True

	def enterFogOfWar( self, t ):
		if self._fogOfWarStartPoints is None:
			self._fogOfWarStartPoints = []
			for id in self.playerManager.playerIdsToPlayers:
				player = self.playerManager.playerIdsToPlayers[id]
				x, y = player.position
				gx = int( self.maze.mapX( x ) )
				gy = int( self.maze.mapY( y ) )
				self._fogOfWarStartPoints.append( (gx, gy) )
	
			for endCell in self.playerManager.endCells:
				endX, endY = self.maze.mapCell( endCell, 0.5 )
				self._fogOfWarStartPoints.append( (int( endX ), int( endY )) )
		
		self.fogOfWarSurface.blit( self.fogOfWarImage, (0.0, 0.0) )
		radius = self.fogOfWarStartRadius + t*(self.fogOfWarRadius - self.fogOfWarStartRadius)
		for point in self._fogOfWarStartPoints:
			pygame.draw.circle( self.fogOfWarSurface, self.fogOfWarKeyColor, point, int( radius ) )
	
	def exitFogOfWar( self, t ):
		radius = 1 + t*(self.fogOfWarGameOverRadius - 1)
		w, h = self.fogOfWarSurface.get_width(), self.fogOfWarSurface.get_height()
		pygame.draw.circle( self.fogOfWarSurface, self.fogOfWarKeyColor, (w/2, h/2), int( radius ) )

	def gameOver( self ):
		'''
		Everyone quit or everyone finished
		'''
		if self.hasSound:
			#self.soundNamesToSounds[ "gameOver" ].play()
			self.soundNamesToSounds[ "trumpet" ].play()
#		self.isGameRunning = False
		self.scheduler.doInterval( 2.0, self.exitFogOfWar )
		self.playerManager.doCelebrate = True
		self.playerManager.celebrate()
		self.gameClock.stop()

	def loadImage( self, name, colorkey=None ):
		fullname = os.path.join( "data", name )
		image = pygame.image.load( fullname )
		image = image.convert()
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at( (0, 0) )
			image.set_colorkey( colorkey )
		return image

