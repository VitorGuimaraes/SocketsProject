# -*-coding: utf-8-*-
import pygame as pg 
from pygame.locals import *
import time

#Retorna o índice de acordo com as coordenadas x, y
def return_index(pos_x, pos_y):
	i = 0
	for y in range(38, 548, 51): 
		for x in range(38, 548, 51): 
			if x == pos_x and y == pos_y:
				return i
			else:
				i += 1

class Hero():
	def __init__(self, t, x, y):
		self.x = x
		self.y = y
		self.t = t
		self.L = 1  #está vivo ou morto

	def set_pos_x(self, x):
		self.x = x

	def set_pos_y(self, y):
		self.y = y

	def set_t(self, t):
		self.t = t

	def set_is_alive(self, liveStat):
		self.L = liveStat

	def get_tipo(self):
		return self.t

	def get_pos_x(self):
		return self.x

	def get_pos_y(self):
		return self.y

	def get_is_alive(self):
		return self.L

	def walk(self, event, x_ant, y_ant, map_objB):
		if event.key == pg.K_LEFT:
			self.x -= 51

		elif event.key == pg.K_RIGHT:
			self.x += 51
		
		elif event.key == pg.K_UP:
			self.y -= 51
			
		elif event.key == pg.K_DOWN:
			self.y += 51

		#Não pode passar dos limites do tabuleiro
		if self.x < 38 or self.x > 497 or self.y < 38 or self.y > 497:
			self.x = x_ant
			self.y = y_ant

		#Não pode andar nos lagos
		if (self.x > 89 and self.x < 242 or self.x > 293 and self.x < 446) and (self.y > 191 and self.y < 344):
				self.x = x_ant
				self.y = y_ant

		#Variável auxiliar para verificar se a casa já contém uma peça do jogador
		index = return_index(self.x, self.y) #Retorna None, 1 ou 2 

		if self.t != 2: #Se não for soldado
			if (((self.x < x_ant or self.x > x_ant) and (self.y < y_ant or self.y > y_ant)) or 
				  self.x < x_ant-51 or self.x > x_ant+51 or self.y < y_ant-51 or self.y > y_ant+51 or
				  map_objB[index] == 1): 
				self.x = x_ant
				self.y = y_ant

		elif self.t == 2: #Se for soldado
			if (((self.y < y_ant-51 or self.y > y_ant+51) and (self.x < x_ant or self.x > x_ant)) or
			    ((self.y < y_ant or self.y > y_ant) and (self.x < x_ant-51 or self.x > x_ant+51)) or
				  self.x < x_ant-102 or self.x > x_ant+102 or self.y < y_ant-102 or self.y > y_ant+102 or
				  map_objB[index] == 1):
				self.x = x_ant
				self.y = y_ant

		#Não permite o jogador selecionar uma peça e deixá-la na mesma posição
		#Cuidado, pq se a peça tiver cercada e o jogador escolher ela, vai entrar em loop infinito
		#Fazer função no main para verificar se esta cercada. Se estiver, nao pode selecionar a peça