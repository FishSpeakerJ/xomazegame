import pygame

class XoMaze:
    def __init__(self, width=1200,height=825):
        self.initScreen( width, height )                
        
    def initScreen( self, width, height ):
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('XoMaze')