import pygame
#import olpcgames ##note, disable this when testing on a non-xo computer.
from XoMaze import XoMaze


def main():
	pygame.init()
	# Start Pygame displays...
	game = XoMaze( )
	while True:
		# Pygame event loop.
		# Update the screen
		if not game.update():
			break
	print "Good Game!"
	return
	
if __name__=="__main__":
	main()