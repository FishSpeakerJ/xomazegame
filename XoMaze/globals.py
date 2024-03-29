import pygame

# custom events
CLOCKTICK = pygame.USEREVENT + 1

# Milliseconds we will sleep each frame if there are no events,
# this will update the clock every second
clockSleepTime = 15

# global variables
hudHeight = 50
bottomMargin = 20

# maze sizes
difficultyLevelToMazeSize = {
 1:( 12, 8 ),
 2:( 24, 16 ),
 3:( 30, 20 ),
 4:( 45, 30 ),
} 

emulatorKeys = {
	pygame.K_KP8 : [ 0, 0, ],
	pygame.K_KP6 : [ 0, 1, ],
	pygame.K_KP2 : [ 0, 2, ],
	pygame.K_KP4 : [ 0, 3, ],

	pygame.K_w : [ 1, 0, ],
	pygame.K_d : [ 1, 1, ],
	pygame.K_s : [ 1, 2, ],
	pygame.K_a : [ 1, 3, ],
	
	pygame.K_UP : [ 2, 0, ],
	pygame.K_RIGHT : [ 2, 1, ],
	pygame.K_DOWN : [ 2, 2, ],
	pygame.K_LEFT : [ 2, 3, ],
	
	pygame.K_KP9 : [ 3, 0, ],
	pygame.K_KP1 : [ 3, 1, ],
	pygame.K_KP3 : [ 3, 2, ],
	pygame.K_KP7 : [ 3, 3, ]
}

keyboardKeys = {
	pygame.K_w : [ 0, 0, ],
	pygame.K_d : [ 0, 1, ],
	pygame.K_s : [ 0, 2, ],
	pygame.K_a : [ 0, 3, ],
	
	pygame.K_o : [ 1, 0, ], # up
	pygame.K_SEMICOLON : [ 1, 1, ],
	pygame.K_l : [ 1, 2, ],
	pygame.K_k : [ 1, 3, ],
	
	pygame.K_UP : [ 2, 0, ],
	pygame.K_RIGHT : [ 2, 1, ],
	pygame.K_DOWN : [ 2, 2, ],
	pygame.K_LEFT : [ 2, 3, ],

	pygame.K_KP8 : [ 3, 0, ],
	pygame.K_KP6 : [ 3, 1, ],
	pygame.K_KP2 : [ 3, 2, ], #down
	pygame.K_KP5 : [ 3, 2, ], #down
	pygame.K_KP4 : [ 3, 3, ],
}
# Player variables
playerSpeedFactor = 0.18  # playerSpeed = sqrt( totalCellsInMaze )*playerSpeedFactor
playerSpeedVisitedFactor = 1.5
#playerSpeedFactor = 0.05  # playerSpeed = sqrt( totalCellsInMaze )*playerSpeedFactor
#playerSpeedVisitedFactor = 10.0
playerColors = [
	((0xFF,0xCE,0x00),(0x00,0x33,0xCC)),
	((0xFF,0xFF,0x9F),(0x66,0x00,0x99)),
	((0xFF,0x85,0x00),(0x00,0x99,0x00)),
	((0x80,0x8F,0xFF),(0xFF,0x00,0x00)),
]