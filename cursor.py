# -*-coding: utf-8-*-
import pygame as pg 
from pygame import mixer
from pygame.locals import *

mixer.init() #Inicia o mixer do pygame
move_cursor = pg.mixer.Sound("sounds/cursor_move.ogg")

cursor = pg.image.load("misc/cursor.png")
select = pg.image.load("misc/select.png")

class Cursor():
	def __init__(self):
		self.pos_x     = 242
		self.pos_y     = 242
		self.isPressed = 0

	def set_pos_x(self, pos_x):
		self.pos_x = pos_x

	def set_pos_y(self, pos_y):
		self.pos_y = pos_y

	def set_pressed(self, isPressed):
		self.isPressed = isPressed

	def get_pos_x(self):
		return self.pos_x

	def get_pos_y(self):
		return self.pos_y

	def draw(self, screen):
		if self.isPressed == 0:
			screen.blit(cursor, (self.pos_x, self.pos_y))
		elif self.isPressed == 1:
			screen.blit(select, (self.pos_x, self.pos_y))

	def move(self, event):
		if event.key == pg.K_LEFT:
			move_cursor.play()
			if (self.pos_x == 242 or self.pos_x == 446) and (self.pos_y == 242 or self.pos_y == 293):
				pass
			else:
				self.pos_x -= 51 
			
			if self.pos_x < 38:
				self.pos_x = 497

		elif event.key == pg.K_RIGHT:
			move_cursor.play()
			if (self.pos_x == 89 or self.pos_x == 293) and (self.pos_y == 242 or self.pos_y == 293):
				pass
			else:
				self.pos_x += 51  
			if self.pos_x > 497:
				self.pos_x = 38

		elif event.key == pg.K_UP:
			move_cursor.play()
			if (self.pos_x == 140 or self.pos_x == 191 or self.pos_x == 344 or self.pos_x == 395) and (self.pos_y == 344):
				pass
			else:
				self.pos_y -= 51
			if self.pos_y < 38:
				self.pos_y = 497

		elif event.key == pg.K_DOWN:
			move_cursor.play()
			if (self.pos_x == 140 or self.pos_x == 191 or self.pos_x == 344 or self.pos_x == 395) and (self.pos_y == 191):
				pass
			else:
				self.pos_y += 51
			if self.pos_y > 497:
				self.pos_y = 38