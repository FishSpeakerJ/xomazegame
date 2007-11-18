"""
PlayerManager

Handles all the players!

"""
from Player import Player
from globals import *

class PlayerManager:
	def __init__( self, game ):
		self.game = game
		self.playerIdsToPlayers = {}
		self.doCelebrate = False
		
		for i in range( self.game.numberOfPlayers ):
			self.playerIdsToPlayers[ i ] = Player( self.game, i )
	
	def reset( self ):
		self.playersWhoHaveHeads = []
		self.endCells = []
		self.alreadySaidUhOhs = []
		self.doCelebrate = False
		for player in self.playerIdsToPlayers.values():
			player.reset()
	
	def playUhOh( self, id ):
		if id in self.alreadySaidUhOhs:
			return
		self.alreadySaidUhOhs.append( id )
		if self.game.hasSound:
			self.game.soundNamesToSounds[ "corkPop%d" % id ].play()

	def registerEnd( self, endCell ):
		self.endCells.append( endCell )

	def checkForEnd( self, endCell, idChecking ):
		if endCell in self.endCells:
			for player in self.playerIdsToPlayers.values():
				if player.id == idChecking:
					continue
				if endCell == self.game.maze.getCellXY( *player.getDiscretePosition( player.position ) ):
					return False
			return True
		else:
			return False

	def checkForSnapDelays( self ):
		for player in self.playerIdsToPlayers.values():
			player.checkSnapDelay()

	def checkForHeads( self ):
		for player in self.playerIdsToPlayers.values():
			player.checkForHead()
	
	def unattachHeads( self ):
		for player in self.playerIdsToPlayers.values():
			player.headAttached = False
	
	def celebrate( self ):
		for player in self.playerIdsToPlayers.values():
			player.celebrate()
		if self.doCelebrate:
			self.game.scheduler.doLater( 0.3, self.celebrate )
		
	def foundHead( self, id ):
		self.playersWhoHaveHeads.append( self.playerIdsToPlayers[ id ] )
	
	def finished( self, id ):
		for player in self.playerIdsToPlayers.values():
			if not player.isFinished():
				return
		print "GAMEOSVER"
		self.game.gameOver()
