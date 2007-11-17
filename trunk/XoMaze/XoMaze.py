import pygame
import sys
#from olpcgames import eventwrap
from Maze import Maze, Cell

class XoMaze:
    def __init__(self, width=1200,height=825):
        self.initScreen( width, height ) 
        self.maze = Maze()
        pygame.init()
        #eventwrap.install()
        
    def initScreen( self, width, height ):
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('XoMaze')
    
    def update( self ):
    	'''
    	 This is the main game loop.
    	 
    	'''
    	pygame.display.update()
    	self.maze.paint( self.screen, 0, 0, 1000, 700 )
    	for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				sys.exit()
        
