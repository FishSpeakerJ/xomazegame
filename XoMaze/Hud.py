import pygame

class Hud:
	def __init__( self, game):
		self.game = game
		self.surface = game.hudSurface
		# Create a font
		self.font = pygame.font.Font(None, 60)

	def update( self ):
		# Render the text
		if self.game.isGameRunning:
			text = self.font.render(self.game.gameClock.getTimeString(), True, 
			                        (255, 255, 255), (0, 0, 0))
			# Create a rectangle
			textRect = text.get_rect()
	
			# Center the rectangle
			textRect.centerx = self.surface.get_rect().centerx
			textRect.centery = self.surface.get_rect().centery
	
			# Blit the text
			self.surface.blit(text, textRect)
			pygame.display.update( self.surface.get_rect() )
	#		self.game.addDirtyRect( self.surface.get_rect() )
	
		else:
			pass
