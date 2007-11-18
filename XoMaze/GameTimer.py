import pygame
import globals
import time
import datetime

class GameTimer:
	def __init__( self ):
		# start game time
		self.startTime = 0
		self.stoppedTime = 0
		self.isRunning = False

	def start( self ):
		self.startTime = pygame.time.get_ticks()
		self.stoppedTime = self.startTime
		self.isRunning = True

	def stop( self ):
		if self.isRunning:
			self.stoppedTime = pygame.time.get_ticks()
			self.isRunning = False

	def reset( self ):
		self.startTime = 0
		self.stoppedTime = 0

	def getTime( self ):
		if self.isRunning:
			return pygame.time.get_ticks() - self.startTime
		else:
			return self.stoppedTime - self.startTime

	def getTimeString( self ):
		if self.isRunning:
			delta = datetime.timedelta( milliseconds=(pygame.time.get_ticks() - self.startTime) )
		else:
			delta = datetime.timedelta( milliseconds=(self.stoppedTime - self.startTime) )
		return time.strftime( "%M:%S", time.gmtime( delta.seconds ) )
