import pygame
import globals

class GameTimer:
	def __init__( self ):
		# start game time
		self.totalTime = 0

	def start( self ):
		self.totalTime = 1
		pygame.time.set_timer(globals.CLOCKTICK, globals.clockSleepTime )
		
	def resume( self ):
		pygame.time.set_timer(globals.CLOCKTICK, globals.clockSleepTime )
		
	def pause( self ):
		pygame.time.set_timer(0)
	
	def isRunning( self ):
		return bool(self.totalTime)
		
	def getTime( self ):
		return self.totalTime
		
	def update( self ):
		self.totalTime += 1000
	
	def getTimeString( self ):
		return "%i:%i" % ( this.totalTime/1000, 60*this.totalTime%1000) 
		