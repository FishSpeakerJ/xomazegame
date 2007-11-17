import pygame
import globals

class GameTimer:
	def __init__( self ):
		# start game time
		self.totalTime = 0

	def start( self ):
		self.totalTime = 0
		pygame.time.set_timer(globals.CLOCKTICK, 1)
		
	def resume( self ):
		pygame.time.set_timer(globals.CLOCKTICK, 1)
		
	def pause( self ):
		pygame.time.set_timer(0)
	
	def getTime( self ):
		return self.totalTime
		
	def update( self ):
		self.totalTime += 1
		
	def updateVisual( self ):
		''' draw some stuff '''
		pass
		