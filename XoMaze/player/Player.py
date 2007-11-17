"""
The player class!

Handles player stuff... not sure what yet...

"""


class Player:
	def __init__( self, game, id ):
		self.game = game
		self.id = id

	def move( self, direction ):
		print "Player %d is moving %d" % ( self.id, direction )

