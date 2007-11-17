import pygame

# custom events
CLOCKTICK = pygame.USEREVENT + 1

# Player variables
PLAYERXINCREMENT = 0.5
PLAYERYINCREMENT = 0.5
PLAYERCOLORS = [
	( ( 255.0, 0.0, 0.0 ), ( 0.0, 255.0, 0.0 ) ),
	( ( 0.0, 0.0, 255.0 ), ( 255.0, 0.0, 0.0 ) ),
	( ( 255.0, 255.0, 0.0 ), ( 0.0, 255.0, 255.0 ) ),
	( ( 0.0, 255.0, 0.0 ), ( 255.0, 0.0, 255.0 ) ),
]