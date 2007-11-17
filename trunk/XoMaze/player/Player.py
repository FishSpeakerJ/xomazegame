"""
The player class!

Handles player stuff... not sure what yet...

"""

from globals import *

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
		self.offset = 1.0 / ( self.game.numberOfPlayers + 4.0 ) * ( self.id + 1 )
		self.headAttached = False
		self.directionToStringDirection = {
			0 : "north",
			1 : "east",
			2 : "south",
			3 : "west",
		}

	def move( self, direction ):
		'''
		Move yourself in the maze
			0 - Up
			1 - Right
			2 - Down
			3 - Left
		'''
		if direction == 0:
			potentialPosition = [ self.position[0], self.position[1] + playerYIncrement ]
			if self.oldDirection == 1 or self.oldDirection == 3:
				potentialPosition[0] = int( potentialPosition[0] ) + 0.5
		elif direction == 1:
			potentialPosition = [ self.position[0] + playerXIncrement, self.position[1] ] 
			if self.oldDirection == 0 or self.oldDirection == 2:
				potentialPosition[0] = int( potentialPosition[0] ) + 0.5
		elif direction == 2:
			potentialPosition = [ self.position[0], self.position[1] - playerYIncrement ] 
			if self.oldDirection == 1 or self.oldDirection == 3:
				potentialPosition[0] = int( potentialPosition[0] ) + 0.5
		else:
			potentialPosition = [ self.position[0] - playerXIncrement, self.position[1] ] 
			if self.oldDirection == 0 or self.oldDirection == 2:
				potentialPosition[0] = int( potentialPosition[0] ) + 0.5
		if self.id == 0:
			print "Player 0 move"
			print "position = ( %f, %f ) " % ( self.position[0], self.position[1] )
			print "direction = %d" % direction
			print "oldDirection = %d" % self.oldDirection
			print "potentialPosition = ( %f, %f )" % ( potentialPosition[0], potentialPosition[1] )
			print "current cell %s " % self.game.maze.getCellXY( *self.getDiscreetPosition( self.position ) )
			print "potential cell %s " % self.game.maze.getCellXY( *self.getDiscreetPosition( potentialPosition ) )
			
		self.oldDirection = direction
		
		# If my new discreet position is the same as my old one, update position
		# and return, no need to check other walls
		if self.getDiscreetPosition( potentialPosition ) == self.getDiscreetPosition( self.position ):
			self.position = potentialPosition
			return
		
		potentialCell = self.game.maze.getCellXY( *self.getDiscreetPosition( potentialPosition ) )
		directionObject = getattr( potentialCell, self.directionToStringDirection[ direction ] )
		if currentCell == self.headCell:
			self.game.playerManager.foundHead( self.id )
			self.headAttached = True
			
		if currentCell == self.endCell:
			if self.headAttached:
				self.playerManager.finished( self.id )

		if directionObject.isWalled:
			# We hit a wall, if there is sound, play it... if not, do nothing.
			if self.game.hasSound:
				self.game.soundNamesToSounds[ "hitWall" ].play()
			return
		# We're free and clear
		self.path.append( potentialCell )
		self.position = potentialPosition
		
	def reset( self ):
		'''
		Resets the player to the bottom of the maze, offset based on his id
		'''
		self.oldDirection = -1
		self.headAttached = False
		
		x = int( self.game.maze.getXCellCount() / 2.0 )
		x = int( x - float(self.game.numberOfPlayers / 2.0 ) ) + self.id*1.0 + self.offset
		self.position = ( x, 0.5 )
		self.beginCell = self.game.maze.getCellXY( *self.getDiscreetPosition( self.position ) ) 
		self.headCell = self.game.maze.getRandomCell()
		self.endCell = self.game.maze.getCellXY( *self.getDiscreetPosition( ( self.position[0], self.position[1] + self.game.maze.getYCellCount() - 1 ) ) )
		self.path = [ self.game.maze.getCellXY( *self.getDiscreetPosition( self.position ) ) ]

	def getPath( self ):
		return self.path

	def getPosition( self ):
		return self.position
		
	def getDiscreetPosition( self, position ):
		return ( int( position[0] ), int( position[1] ) )

	def getStrokeColor( self ):
		return self.colors[0]

	def getFillColor( self ):
		return self.colors[1]

	def signal( self ):
		'''
		Wave and change strong path to where you are
		'''
		pass

