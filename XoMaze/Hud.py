import pygame

class Hud:
	def __init__( self, game):
		self.game = game
		self.surface = game.hudSurface
		# Create a font
		self.font = pygame.font.Font(None, 30)
		
	def update( self ):
		# Render the text
		text = self.font.render(self.game.gameClock.getTimeString(), True, 
						(255, 255, 255), (0, 0, 0))

		# Create a rectangle
		textRect = text.get_rect()

		# Center the rectangle
		textRect.centerx = self.surface.get_rect().centerx
		textRect.centery = self.surface.get_rect().centery

		# Blit the text
		self.surface.blit(text, textRect)
		# update the subparts
		pygame.display.update( self.surface.get_rect() )