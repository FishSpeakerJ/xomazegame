"""
The player class!

Handles player stuff... not sure what yet...

"""


class Player:
	def __init__( self, game, id ):
		self.game = game
		self.id = id
		self.initVariables()
		self.initVisuals()
		
	def initVariables( self ):
		self.position = ( 0.0, 0.0 )
		self.directionToStringDirection = {
			0 : "up",
			1 : "right",
			2 : "down",
			3 : "left",
		}

	def initVisuals( self ):
		'''
		Have to get colors from somewhere...
		'''

	def move( self, direction ):
		'''
		Move yourself in the maze
			0 - Up
			1 - Right
			2 - Down
			3 - Left
		'''		
		print "Player %d is moving %s (%d)" % ( self.id, self.directionToStringDirection[ direction ], direction )
		print self.position
		
	def reset( self ):
		'''
		Resets the player to the bottom of the maze, offset based on his id
		'''
		x = self.game.maze.getColumnCount / 2.0
		print x
		self.position = ( x - float(self.game.numberOfPlayers) + self.id*1.0, 0.0 )

	def getPosition( self ):
		return self.position

	def signal( self ):
		'''
		Wave and change strong path to where you are
		'''
		pass