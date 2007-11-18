
import time

class Scheduler:
	def __init__( self, xoMaze ):
		self.xoMaze = xoMaze
		self.lastTime = time.time()
		self.intervals = []
		self.doLaters = []
		
	def doInterval( self, duration, func, waitBefore=0.0 ):
		self.intervals.append( (duration, func, duration, waitBefore) )

	def doLater( self, wait, func ):
		self.doLaters.append( (wait, func) )

	def update( self ):
		t = time.time()
		dt = t - self.lastTime
		self.lastTime = t

		newDoLaters = []
		for wait, func in self.doLaters:
			wait -= dt
			if wait <= 0.0:
				func()
			else:
				newDoLaters.append( (wait, func) )
		self.doLaters = newDoLaters

		newIntervals = []
		for duration, func, timeLeft, waitBefore in self.intervals:
			if waitBefore > 0.0:
				waitBefore -= dt
				if waitBefore <= 0.0:
					func( 0.0 )

			kill = False
			if waitBefore <= 0.0:
				timeLeft -= dt
				if timeLeft <= 0.0:
					func( 1.0 )
					kill = True
				else:
					func( (duration - timeLeft)/duration )
			if not kill:
				newIntervals.append( (duration, func, timeLeft, waitBefore) )
		self.intervals = newIntervals


