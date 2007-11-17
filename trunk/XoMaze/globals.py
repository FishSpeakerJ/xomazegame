import pygame

# custom events
CLOCKTICK = pygame.USEREVENT + 1

# global variables
hudHeight = 50
bottomMargin = 20

# maze sizes
difficultyLevelToMazeSize = {
 1:( 20,20),
 2:( 50, 30 ),
 3:( 70, 50 )
}

emulatorKeys = {
	"K_KP8" : [ 0, 0, ],
	"K_KP6" : [ 0, 1, ],
	"K_KP2" : [ 0, 2, ],
	"K_KP4" : [ 0, 3, ],
}

keyboardKeys = {
	"K_w" : [ 0, 0, ],
	"K_d" : [ 0, 1, ],
	"K_s" : [ 0, 2, ],
	"K_a" : [ 0, 3, ],
	
	"K_g" : [ 1, 0, ], # up
	"K_h" : [ 1, 0, ], # up
	"K_n" : [ 1, 1, ],
	"K_b" : [ 1, 2, ],
	"K_v" : [ 1, 3, ],
	
	"K_UP" : [ 2, 0, ],
	"K_RIGHT" : [ 2, 1, ],
	"K_DOWN" : [ 2, 2, ],
	"K_LEFT" : [ 2, 3, ],
	
	"K_8" : [ 3, 0, ],
	"K_6" : [ 3, 1, ],
	"K_2" : [ 3, 2, ],
	"K_4" : [ 3, 3, ],

	"K_KP8" : [ 3, 0, ],
	"K_KP6" : [ 3, 1, ],
	"K_KP2" : [ 3, 2, ],
	"K_KP4" : [ 3, 3, ],

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