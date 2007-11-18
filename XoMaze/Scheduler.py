
import time

class Scheduler:
	def __init__( self, xoMaze ):
		self.xoMaze = xoMaze
		self.lastTime = time.time()
		self.intervals = []
		
	def doInterval( self, duration, func, waitBefore=0.0 ):
		print "doInterval"
		self.intervals.append( (duration, func, duration, waitBefore) )

	def update( self ):
		t = time.time()
		dt = t - self.lastTime
		self.lastTime = t
		
		newIntervals = []
		for interval in self.intervals:
			duration, func, timeLeft, waitBefore = interval
			print waitBefore

			if waitBefore > 0.0:
				waitBefore -= dt
				if waitBefore <= 0.0:
					func( 0.0 )

			if waitBefore <= 0.0:
				timeLeft -= dt
				if timeLeft <= 0.0:
					func( 1.0 )
					return
				else:
					func( (duration - timeLeft)/duration )
			newIntervals.append( (duration, func, timeLeft, waitBefore) )
		self.intervals = newIntervals


