import pygame

# custom events
CLOCKTICK = pygame.USEREVENT + 1

# Player variables
PLAYERXINCREMENT = 0.1
PLAYERYINCREMENT = 0.1
PLAYERCOLORS = [
	( ( 255.0, 0.0, 0.0 ), ( 0.0, 255.0, 0.0 ) ),
	( ( 0.0, 0.0, 255.0 ), ( 255.0, 0.0, 0.0 ) ),
	( ( 255.0, 255.0, 0.0 ), ( 0.0, 255.0, 255.0 ) ),
	( ( 0.0, 255.0, 0.0 ), ( 255.0, 0.0, 255.0 ) ),
]