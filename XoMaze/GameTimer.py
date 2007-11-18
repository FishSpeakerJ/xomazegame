import pygame
import globals
import time
import datetime

class GameTimer:
	def __init__( self ):
		# start game time
		self.startTime = 0

	def start( self ):
		self.startTime = pygame.time.get_ticks()
		pygame.time.set_timer(globals.CLOCKTICK, globals.clockSleepTime )
		
	def isRunning( self ):
		return bool(self.startTime)
		
	def getTime( self ):
		return pygame.time.get_ticks() - self.startTime
		
	def getTimeString( self ):
		delta = datetime.timedelta( milliseconds=(pygame.time.get_ticks() - self.startTime) )
		return time.strftime("%H:%M:%S",time.gmtime(delta.seconds))
		
#		.strftime("%M:%S")