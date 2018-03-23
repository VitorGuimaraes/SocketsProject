import string
import time
import pygame as pg
from pygame.locals import *

pg.font.init()
font = pg.font.Font("nyala.ttf", 18)
update_msg_box = pg.image.load("updateMsgBox.png")

def get_key():
	event = pg.event.poll()
	if event.type == KEYDOWN:
		return event.key


def display_box(screen, pos_x, pos_y, message):
	screen.blit(update_msg_box, (0, 0))
	if len(message) != 0:
		screen.blit(font.render(message, 1, (0, 0, 0)), (pos_x, pos_y))
	pg.display.update()

def ask(screen, pos_x, pos_y):
	current_string = []
	# display_box(screen, pos_x, pos_y, string.join(current_string,""))
	
	while True:
		inkey = get_key()
		if inkey != None:
			if inkey == K_BACKSPACE:
				current_string = current_string[0:-1]
			
			elif inkey == K_RETURN:
				break

			elif inkey <= 127:
				if len(current_string) < 28:
					current_string.append(chr(inkey))

		msg = string.join(current_string, "")
		display_box(screen, pos_x, pos_y, msg)

		print current_string
		
	return string.join(current_string, "")