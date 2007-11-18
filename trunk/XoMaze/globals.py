import pygame

# custom events
CLOCKTICK = pygame.USEREVENT + 1

# Milliseconds we will sleep each frame if there are no events,
# this will update the clock every second
clockSleepTime = 50

# global variables
hudHeight = 50
bottomMargin = 20

# maze sizes
difficultyLevelToMazeSize = {
 1:( 10, 10 ),
 2:( 30, 20 ),
 3:( 50, 30 ),
 4:( 80, 50 ),
} 

emulatorKeys = {
	pygame.K_KP8 : [ 0, 0, ],
	pygame.K_KP6 : [ 0, 1, ],
	pygame.K_KP2 : [ 0, 2, ],
	pygame.K_KP4 : [ 0, 3, ],
	pygame.K_TAB : [ 0, 4, ],

	pygame.K_w : [ 1, 0, ],
	pygame.K_d : [ 1, 1, ],
	pygame.K_s : [ 1, 2, ],
	pygame.K_a : [ 1, 3, ],
	pygame.K_q : [ 1, 4, ],
	
	pygame.K_UP : [ 2, 0, ],
	pygame.K_RIGHT : [ 2, 1, ],
	pygame.K_DOWN : [ 2, 2, ],
	pygame.K_LEFT : [ 2, 3, ],
	pygame.K_RSHIFT : [ 2, 4, ],
	
	pygame.K_KP9 : [ 3, 0, ],
	pygame.K_KP1 : [ 3, 1, ],
	pygame.K_KP3 : [ 3, 2, ],
	pygame.K_KP7 : [ 3, 3, ],
	pygame.K_BACKSPACE : [ 3, 4, ],
	
	
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

	pygame.K_KP8 : [ 3, 0, ],
	pygame.K_KP6 : [ 3, 1, ],
	pygame.K_KP2 : [ 3, 2, ],
	pygame.K_KP4 : [ 3, 3, ],
	pygame.K_KP7 : [ 3, 4, ],
}
# Player variables
playerSpeedConstant = 4.5  # playerSpeed = sqrt( totalCellsInMaze )/playerSpeedConstant
playerColors = [
	((255.0, 0.0, 0.0), (0.0, 255.0, 0.0)),
	((0.0, 0.0, 255.0), ( 55.0, 0.0, 0.0)),
	((255.0, 255.0, 0.0), (0.0, 255.0, 255.0)),
	((0.0, 255.0, 0.0), (255.0, 0.0, 255.0)),
]