import pygame
import globals
import time
import datetime

class GameTimer:
	def __init__( self ):
		# start game time
		self.startTime = 0
		self.isRunning = False

	def start( self ):
		self.startTime = pygame.time.get_ticks()
		self.isRunning = True
		
	def stop( self ):
		self.isRunning = False

	def getTime( self ):
		return pygame.time.get_ticks() - self.startTime
		
	def getTimeString( self ):
		delta = datetime.timedelta( milliseconds=(pygame.time.get_ticks() - self.startTime) )
		return time.strftime("%M:%S",time.gmtime(delta.seconds))