"""
The player class!

Handles player stuff... not sure what yet...

"""

from globals import *

import math

class Player:
	def __init__( self, game, id ):
		self.game = game
		self.id = id
		self.initVariables()

	def initVariables( self ):
		self.colors = playerColors[ self.id ]
		self.position = ( 0.0, 0.0 )
		self.oldDirection = -1
		self.path = []
		self.offset = 1.0 / ( self.game.numberOfPlayers + 3.0 ) * ( self.id + 2 )
		self.headAttached = True
		self.signaling = False
		self.directionToStringDirection = {
			0 : "north",
			1 : "east",
			2 : "south",
			3 : "west",
		}

	def move( self, direction, dt=0.05 ):
		'''
		Move yourself in the maze
			0 - North
			1 - East
			2 - South
			3 - West
			4 - Signal
		'''
		if direction == 4:
			self.signaling = True
			return
		# If I don't want to move because I've just been snapped... return
		if self.snapDelayed:
			return

		oldCell = self.game.maze.getCellXY( *self.getDiscretePosition( self.position ) )

		playerSpeed = math.sqrt( self.game.maze._rowCount*self.game.maze._columnCount )*playerSpeedConstant
		if oldCell.beenVisited:
			playerSpeed *= playerSpeedVisitedFactor
		delta = playerSpeed*dt
		delta = min( delta, 0.49 )

		if direction == 0:  # North
			directionVector = (0.0, 1.0)
		elif direction == 1:  # East
			directionVector = (1.0, 0.0)
		elif direction == 2:  # South
			directionVector = (0.0, -1.0)
		else:  # West
			directionVector = (-1.0, 0.0)
		
		potentialPosition = [self.position[0] + delta*directionVector[0], self.position[1] + delta*directionVector[1]]
		
		if False and self.id == 2:
			print "Player 0 move"
			print "  dt:", dt
			print "  delta:", delta
			print "  position = ( %f, %f ) " % ( self.position[0], self.position[1] )
			print "  direction = %d" % direction
			print "  oldDirection = %d" % self.oldDirection
			print "  potentialPosition = ( %f, %f )" % ( potentialPosition[0], potentialPosition[1] )
			currentCell = self.game.maze.getCellXY( *self.getDiscretePosition( self.position ) )
			potentialCell = self.game.maze.getCellXY( *self.getDiscretePosition( potentialPosition ) )
			
			print "  current cell %s " % currentCell
			print "  potential cell %s " % potentialCell
		self.oldDirection = direction
		
		# Check for walls if I'm past the center of the cell (in the direction of travel)
		directionObject = getattr( oldCell, self.directionToStringDirection[direction] )
		if directionObject.isWalled:
			if (direction == 0) and (math.modf( potentialPosition[1] )[0] > 0.5):  # North
				potentialPosition[1] = int( potentialPosition[1] ) + 0.5
			elif (direction == 1) and (math.modf( potentialPosition[0] )[0] > 0.5):  # East
				potentialPosition[0] = int( potentialPosition[0] ) + 0.5
			elif (direction == 2) and (math.modf( potentialPosition[1] )[0] < 0.5):  # South
				potentialPosition[1] = int( potentialPosition[1] ) + 0.5
			elif (direction == 3) and (math.modf( potentialPosition[0] )[0] < 0.5):  # West
				potentialPosition[0] = int( potentialPosition[0] ) + 0.5
		else:
			if directionVector[0] == 0.0:
				potentialPosition[0] = int( potentialPosition[0] ) + 0.5
			else:
				potentialPosition[1] = int( potentialPosition[1] ) + 0.5


		self.position = potentialPosition
		self.game.onPlayerPositionChange( self.id, self.position )

		# Do updates for new cell
		currentCell = self.game.maze.getCellXY( *self.getDiscretePosition( self.position ) )
		if currentCell != oldCell:
			self.path.append( oldCell )
			currentCell.beenVisited = True
	
			if currentCell == self.headCell and not self.headAttached:
				self.game.playerManager.foundHead( self.id )
				self.headAttached = True
				if self.game.hasSound:
					self.game.soundNamesToSounds[ "signalHead%d" % self.id ].play()
				currentCell.isContainingHead = False
			
			# We've got a head... it isn't mine, let's check back later!
			if currentCell.isContainingHead:
				pygame.time.set_timer( CHECKHEADS, 250 )

			if self.game.playerManager.checkForEnd( currentCell ):
				if self.headAttached:
					self.game.playerManager.finished( self.id )
					if self.game.hasSound:
						self.game.soundNamesToSounds[ "signalEnd%d" % self.id ].play()
					self.position = ( currentCell.column + 0.5, currentCell.row + 0.5 )
					pygame.time.set_timer( DELAYSNAP, 500 )
					self.snapDelayed = True
					self.game.onPlayerPositionChange( self.id, self.position )
	
	def checkSnapDelay( self ):
		self.snapDelayed = False

	def checkForHead( self ):
		currentCell = self.game.maze.getCellXY( *self.getDiscretePosition( self.position ) )
		if currentCell.isContainingHead:
			if self.signaling:
				self.signaling = False
			else:
				self.signaling = True
				if self.game.hasSound:
					self.game.soundNamesToSounds[ "signalFound%d" % self.id ].play()
		else:
			self.signaling = False
		pygame.time.set_timer( CHECKHEADS, 300 )

	def celebrate( self ):
		if not self.isFinished():
			return
		if self.signaling:
			self.signaling = False
		else:
			self.signaling = True
		pygame.time.set_timer( CELEBRATE, 300 )
		
	def reset( self ):
		'''
		Resets the player to the bottom of the maze, offset based on his id
		'''
		self.oldDirection = -1
		self.headAttached = True
		self.signaling = False
		self.snapDelayed = False
		x = int( self.game.maze.getXCellCount() / 2.0 )
		x = int( x - float(self.game.numberOfPlayers / 2.0 ) ) + self.id*1.0 + self.offset
		self.position = ( x, 0.5 )
		self.beginCell = self.game.maze.getCellXY( *self.getDiscretePosition( self.position ) ) 
		self.headCell = self.game.maze.getRandomUnusedCell()
		self.headCell.isContainingHead = True
		self.game.playerManager.registerEnd( self.game.maze.getCellXY( *self.getDiscretePosition( ( self.position[0], self.position[1] + self.game.maze.getYCellCount() - 1 ) ) ) )
		self.path = [ self.game.maze.getCellXY( *self.getDiscretePosition( self.position ) ) ]

	def getPath( self ):
		return self.path

	def isFinished( self ):
		if self.game.playerManager.checkForEnd( self.game.maze.getCellXY( *self.getDiscretePosition( self.position ) ) ) and self.headAttached:
			return True
		else:
			return False

	def getPosition( self ):
		return self.position
		
	def getDiscretePosition( self, position ):
		return ( int( position[0] ), int( position[1] ) )

	def getStrokeColor( self ):
		return self.colors[0]

	def getFillColor( self ):
		return self.colors[1]

	def isSignaling( self ):
		'''
		Wave and change strong path to where you are
		'''
		return self.signaling

