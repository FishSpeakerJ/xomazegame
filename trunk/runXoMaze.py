import pygame
#import olpcgames ##note, disable this when testing on a non-xo computer.
from XoMaze import XoMaze

def main():
    pygame.init()
    # Start Pygame displays...
    Game = XoMaze( 1200, 855 )
    while True:
        # Pygame event loop.
        # Update the screen
		pygame.display.update()
		
if __name__=="__main__":
    main()