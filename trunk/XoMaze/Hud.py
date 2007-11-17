import pygame

class Hud:
	def __init__( self, game):
		self.game = game
		self.surface = game.hudSurface
		# Create a font
		font = pygame.font.Font(None, 17)
		
	def update( self ):
		# Render the text
		text = font.render(self.gameClock.getTimeString(), True, 
						(255, 255, 255), (159, 182, 205))

		# Create a rectangle
		textRect = text.get_rect()

		# Center the rectangle
		textRect.centerx = self.surface.get_rect().centerx
		textRect.centery = self.surface.get_rect().centery

		# Blit the text
		self.surface.blit(text, textRect)
		# update the subparts
		pygame.display.update( self.surface.get_rect() )