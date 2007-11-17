"""
The player class!

Handles player stuff... not sure what yet...

"""

import globals

class Player:
	def __init__( self, game, id ):
		self.game = game
		self.id = id
		self.initVariables()
		self.initVisuals()

	def initVariables( self ):
		self.colors = PLAYERCOLORS[ self.id ]
		self.position = ( 0.0, 0.0 )
		self.directionToStringDirection = {
			0 : "north",
			1 : "east",
			2 : "south",
			3 : "west",
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
		if direction == 0:
			potentialPosition = ( self.position[0], self.position[1] + PLAYERYINCREMENT ) 
		elif direction == 1:
			potentialPosition = ( self.position[0] + PLAYERXINCREMENT, self.position[1] ) 
		elif direction == 2:
			potentialPosition = ( self.position[0], self.position[1] - PLAYERYINCREMENT ) 
		else:
			potentialPosition = ( self.position[0] - PLAYERXINCREMENT, self.position[1] ) 

		if self.getDiscreetPosition( potentialPosition ) == self.getDiscreetPosition( self.position ):
			self.position = potentialPosition
			return
		potentialCell = self.game.maze.getCell( *self.getDiscreetPosition( potentialPosition ) )
		directionObject = getattr( potentialCell, self.directionToStringDirection[ direction ] )
		if directionObject.isWalled():
			# We hit a wall, if there is sound, play it... if not, do nothing.
			if self.game.hasSound:
				self.game.soundNamesToSounds[ "hitWall" ].play()
			return
		# We're free and clear
		self.position = potentialPosition
		
	def reset( self ):
		'''
		Resets the player to the bottom of the maze, offset based on his id
		'''
		x = self.game.maze.getColumnCount() / 2.0
		self.position = ( x - float(self.game.numberOfPlayers) + self.id*1.0, 0.0 )

	def getPosition( self ):
		return self.position
		
	def getDiscreetPosition( self, position ):
		return ( int( position[0] ), int( position[1] ) )

	def signal( self ):
		'''
		Wave and change strong path to where you are
		'''
		pass