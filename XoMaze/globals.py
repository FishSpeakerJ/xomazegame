import pygame

# custom events
CLOCKTICK = pygame.USEREVENT + 1

# global variables
hudHeight = 50
bottomMargin = 20

# maze sizes
difficultyLevelToMazeSize = {
 1:( 10,10),
 2:( 30, 20 ),
 3:( 50, 30 )
}

emulatorKeys = {
	"K_KP8" : [ 0, 0, ],
	"K_KP6" : [ 0, 1, ],
	"K_KP2" : [ 0, 2, ],
	"K_KP4" : [ 0, 3, ],
	"K_KP7" : [ 0, 4, ],
}

keyboardKeys = {
	pygame.K_w : [ 0, 0, ],
	pygame.K_d : [ 0, 1, ],
	pygame.K_s : [ 0, 2, ],
	pygame.K_a : [ 0, 3, ],
	pygame.K_q : [ 0, 4, ],
	
	pygame.K_g : [ 1, 0, ], # up
	pygame.K_h : [ 1, 0, ], # up
	pygame.K_n : [ 1, 1, ],
	pygame.K_b : [ 1, 2, ],
	pygame.K_v : [ 1, 3, ],
	pygame.K_f : [ 1, 4, ],
	
	pygame.K_UP : [ 2, 0, ],
	pygame.K_RIGHT : [ 2, 1, ],
	pygame.K_DOWN : [ 2, 2, ],
	pygame.K_LEFT : [ 2, 3, ],
	pygame.K_RSHIFT : [ 2, 4, ],
	
	pygame.K_8 : [ 3, 0, ],
	pygame.K_6 : [ 3, 1, ],
	pygame.K_2 : [ 3, 2, ],
	pygame.K_4 : [ 3, 3, ],
	pygame.K_7 : [ 3, 4, ],

	pygame.K_KP8 : [ 3, 0, ],
	pygame.K_KP6 : [ 3, 1, ],
	pygame.K_KP2 : [ 3, 2, ],
	pygame.K_KP4 : [ 3, 3, ],
	pygame.K_KP7 : [ 3, 4, ],
}
# Player variables
playerXIncrement = 0.11
playerYIncrement = 0.11
playerColors = [
	( ( 255.0, 0.0, 0.0 ), ( 0.0, 255.0, 0.0 ) ),
	( ( 0.0, 0.0, 255.0 ), ( 255.0, 0.0, 0.0 ) ),
	( ( 255.0, 255.0, 0.0 ), ( 0.0, 255.0, 255.0 ) ),
	( ( 0.0, 255.0, 0.0 ), ( 255.0, 0.0, 255.0 ) ),
]