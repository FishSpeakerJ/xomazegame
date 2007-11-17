"""
PlayerManager

Handles all the players!

"""
from Player import Player
 
class PlayerManager:
	def __init__( self, game ):
		self.game = game
		self.playerIdsToPlayers = {}
		
		for i in range( self.game.numberOfPlayers ):
			self.playerIdsToPlayers[ i ] = Player( self.game, i )
	
	def reset( self ):
		self.playersWhoHaveHeads = []
		for player in self.playerIdsToPlayers.values():
			player.reset()

	def foundHead( self, id ):
		print "Player %d found their head!" % id
		self.playersWhoHaveHeads.append( self.playerIdsToPlayers[ id ] )
	
	def finished( self, id ):
		print "Player %d finished!!" % id
		for player in self.playerIdsToPlayers.values():
			if not player.isFinished():
				return
		self.game.gameOver()
