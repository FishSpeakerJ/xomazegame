import time
import os
import string
import random

# PyGame Constants
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

def main():
	WINSIZE = 1200,825
	pygame.init()
	screen = pygame.display.set_mode(WINSIZE,0,8)
	pygame.display.set_caption('Hello World (in Thai)')
	
	screen.fill(THECOLORS["black"])
	
	image, rect = load_image('emblem0.png', -1)
	image2, rect = load_image('emblem1.png', -1)
	imagepos = image.get_rect(centerx=screen.get_width()/2, centery=screen.get_height()/2)
	screen.blit(image, imagepos)
	images = (image, image2)

	if pygame.font:
		font = pygame.font.Font(None, 36)
		text = font.render("h w", 1, (200, 200, 200))
		textpos = text.get_rect(centerx=screen.get_width()/2)
		screen.blit(text, textpos)

	hello_sound = load_sound('hello.ogg')
	hello_sound.play()
	
	import time
	lastTime = time.time()
	i = 0
	# The Main Event Loop
	done = False
	while not done:
		t = time.time()
		if t - lastTime > 1.0:
			lastTime = t
			i = (i + 1) % 2
		screen.fill(THECOLORS["black"])
		screen.blit(images[i], imagepos)
		hello_sound.play()

		if pygame.font:
			font = pygame.font.Font(None, 36)
			text = font.render("Hello World (in Thai)", 1, (200, 200, 200))
			textpos = text.get_rect(centerx=screen.get_width()/2)
			screen.blit(text, textpos)

		# Drawing finished this iteration?  Update the screen
		pygame.display.update()
		    
		# Event Handling:
		events = pygame.event.get( )
		for e in events:
			if( e.type == QUIT ):
				done = True
				break
			elif (e.type == KEYDOWN):
				if( e.key == K_ESCAPE ):
					done = True
					break
				if( e.key == K_f ):
					pygame.display.toggle_fullscreen()
	
	print "Exiting!"
	
	return

if __name__=="__main__":
    main()
