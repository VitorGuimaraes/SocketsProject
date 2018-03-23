# -*-coding: utf-8-*-
#System imports:
import random
import time
from threading import Thread
from select import select
import string
#Third party imports:
import pygame as pg 
from pygame.locals import *
#Local imports:
from cursor import Cursor
from client import SocketClient
from hero import Hero
from managepackage import ManagePackage

pg.init()						#Inicializa o pygame
pg.font.init()
sock = SocketClient()			#Instancia um objeto Socket Cliente
PacketManager = ManagePackage()	#Cria um gerenciador de pacotes json

SCREEN_SIZE = (900, 700) #Dimensões da tela
BACKGROUND_COLOR = (255, 255, 255)
CAPTION = "Stratego!"
font = pg.font.Font("nyala.ttf", 18)

map_x = [] #Armazena as posições x do mapa
map_y = [] #Armazena as posições y do mapa

#Gera o mapa atribuindo as coordenadas do tabuleiro nas listas map_x e map_y
def mapGen():
	i = 0
	for y in range(38, 548, 51): 
		for x in range(38, 548, 51): 
			map_x.insert(i, x)
			map_y.insert(i, y)
			i += 1
mapGen() 

#Retorna o índice de acordo com as coordenadas x, y
def return_index(pos_x, pos_y):
	i = 0
	for y in range(38, 548, 51): 
		for x in range(38, 548, 51): 
			if x == pos_x and y == pos_y:
				return i
			else:
				i += 1

#Retorna as coordenadas de acordo com o índice
def return_x_y(index):
	i = 0
	for y in range(38, 548, 51): 
		for x in range(38, 548, 51):
			if index == i:
				return (x, y)
			else:
				i += 1

#Retorna as cordenadas inversas de uma coordenada comum
def invert_x_y(pos_x, pos_y):
	index = return_index(pos_x, pos_y)
	i = 0
	for y in reversed(range(38, 548, 51)): 
		for x in reversed(range(38, 548, 51)):
			if index == i:
				return (x, y)
			else:
				i += 1
############################################################################
start 		   = pg.image.load("misc/start.png") 
update_board   = pg.image.load("misc/updateBoard.png")
hidden   	   = pg.image.load("misc/hidden.png")
update_chat    = pg.image.load("misc/updateChat.png")
update_msg_box = pg.image.load("misc/updateMsgBox.png")
restart_img    = pg.image.load("misc/restart.png")
surrender_img  = pg.image.load("misc/surrender.png")
popup_cursor   = pg.image.load("misc/popup_cursor.png")
cursor_confirm = pg.mixer.Sound("sounds/cursor_confirm.ogg")
############################################################################
sprites = ["Heros/mina.png", "Heros/espiao.png", "Heros/soldado.png", "Heros/cabo.png", "Heros/sargento.png",
"Heros/subtenente.png", "Heros/tenente.png", "Heros/capitao.png", "Heros/major.png", "Heros/coronel.png",
"Heros/general.png", "Heros/prisioneiro.png"]

classe = []
def load_sprites():
	i = 0
	for path in sprites:
		classe.insert(i, pg.image.load(path))
		i += 1

def create_army(army):
	for i in range(0, 8):
		army.insert(i, Hero(2, 38, 38)) #cria soldados
	for i in range(8, 13):
		army.insert(i, Hero(3, 38, 38)) #cria cabos
	for i in range(13, 17):
		army.insert(i, Hero(4, 38, 38)) #cria sargentos
	for i in range(17, 21):
		army.insert(i, Hero(5, 38, 38)) #cria subtenentes
	for i in range(21, 25):	
		army.insert(i, Hero(6, 38, 38)) #cria tenentes
	for i in range(25, 28):
		army.insert(i, Hero(7, 38, 38)) #cria capitães
	for i in range(28, 30):
		army.insert(i, Hero(8, 38, 38)) #cria majores
	army.insert(30, Hero(9, 38, 38))    #cria coronéis
	army.insert(31, Hero(10, 38, 38))   #cria generais
	army.insert(32, Hero(1, 38, 38)) 	#cria espiões
	for i in range(33, 39):
		army.insert(i, Hero(0, 38, 38)) #cria minas
	army.insert(39, Hero(11, 38, 38))   #cria prisioneiros

#Lista para randomizar as posições das peças no início do jogo
rdPos = random.sample(xrange(60, 100), 40)
#Define a posição inicial das peças do jogador1
def give_pos(obj):
	cont = 0
	for i in range(0, 40):
		obj[cont].set_pos_x(map_x[rdPos[i]])
		obj[cont].set_pos_y(map_y[rdPos[i]])
		cont += 1

#Insere os objetos nas listas de controle
def insert_obj(army, player):
	global map_obj
	global map_objB

	for i in range(0, 40):
		index = return_index(army[i].get_pos_x(), army[i].get_pos_y())

		if army[i].get_is_alive() == 1:
			map_obj[index]  = army[i]
			map_objB[index] = player

		elif army[i].get_is_alive() == 0:
			map_obj[index]  = 0
			map_objB[index] = 0

def draw_player(screen, army, player):
	for i in range(0, 40):
		index = return_index(army[i].get_pos_x(), army[i].get_pos_y())

		if army[i].get_is_alive() == 1:
			if player == 1:
				screen.blit(classe[army[i].get_tipo()], (army[i].get_pos_x(), army[i].get_pos_y())) 
			elif player == 2:
				screen.blit(hidden, (army[i].get_pos_x(), army[i].get_pos_y())) 

#Codifica pacotes json e envia pro servidor
def pack_and_send():
	global player_army
	packet = PacketManager.pack_json(player_army)
	sock.send(packet)

#Recebe pacotes json e decodifica 
def receive_pack():
	packet = sock.receive()
	dictionary = PacketManager.unpack_json(packet)
	return dictionary

def update_enemy_army(dictionaries):
	global enemy_army
	global map_objB
	i = 0
	for dictionary in dictionaries:
		#A posição antiga do inimigo nas listas de controle é setada para 0
		old_x = enemy_army[i].get_pos_x()
		old_y = enemy_army[i].get_pos_y()

		old_index = return_index(old_x, old_y)
		map_objB[old_index] = 0

		enemy_army_data = list(dictionary.values())
		new_x, new_y = invert_x_y(enemy_army_data[1], enemy_army_data[0])
		enemy_army[i].set_pos_x(new_x) 
		enemy_army[i].set_pos_y(new_y) 
		enemy_army[i].set_is_alive(enemy_army_data[3]) 
		enemy_army[i].set_t(enemy_army_data[2])
		i += 1

def update_my_army(army, map_obj, map_objB):
	j = 0
	for i in range(0, 100):
		if map_objB[i] == 1: #Se é um soldado do jogador1
			army[j] = map_obj[i]
			j += 1

def combat(my_soldier, my_soldier_old_house, enemy_soldier, map_obj, map_objB, win_game):
	enemy_strenght = enemy_soldier.get_tipo()
	my_strenght = my_soldier.get_tipo()
	#Casos de vitória
	if ((my_strenght > enemy_strenght and enemy_strenght != 0) or #Se meu_soldado é mais forte e o inimigo não é uma mina
		(my_strenght == 3 and enemy_strenght == 0) or #Se meu_soldado é cabo e o inimigo é mina
		(my_strenght == 1 and enemy_strenght == 10)): #Se meu_soldado é espião e o inimigo é general
		enemy_soldier.set_is_alive(0)		    #Inimigo é eliminado
		return True								#Venceu o combate
	#Casos de derrota
	elif ((my_strenght < enemy_strenght) or              #Se meu_soldado é mais fraco do que o inimigo
		  (my_strenght != 3 and enemy_strenght == 0) or  #Se meu soldado não é cabo e o inimigo é mina
		  (my_strenght == enemy_strenght)):			     #Se meu_soldado é igual ao soldado inimigo
		if enemy_strenght != 11:		#Se o inimigo não for o prisioneiro
			my_soldier.set_is_alive(0)	#meu_soldado é eliminado
			map_obj[my_soldier_old_house]  = 0		#Remove meu_soldado das listas de controle
			map_objB[my_soldier_old_house] = 0		#Remove meu_soldado das listas de controle

			#Se meu_soldado não é cabo e o inimigo é uma mina || soldados são da mesma classe
			if (my_strenght != 3 and enemy_strenght == 0) or (my_strenght == enemy_strenght):	
				enemy_soldier.set_is_alive(0) #Inimigo é eliminado
				index = return_index(enemy_soldier.get_pos_x(), enemy_soldier.get_pos_y())
				map_obj[index]  = 0		#Remove inimigo das listas de controle
				map_objB[index] = 0		#Remove inimigo das listas de controle
			return False					#Perdeu o combate

		elif enemy_strenght == 11:	#Se o inimigo for o prisioneiro
			win_game = True #chamar função de vitória

def ask_surrender_or_restart(event):
	if event.key == K_F12: 		   #Se a tecla pressionada for F12
		sock.send(".;~[/su")	   #Envia o pedido de desistência para o servidor

	elif event.key == K_F11:	   #Se a tecla pressionada for F11
		sock.send(".;~[/re") 	   #Envia o pedido de reinício para o servidor

def accept_restart_or_surrender():
	global enemy_wants_restart
	global enemy_wants_surrender
	
	if enemy_wants_restart:
		answer = ".;~[/accres"
		img = restart_img
	elif enemy_wants_surrender:
		answer = ".;~[/accsu"
		img = surrender_img

	if enemy_wants_restart or enemy_wants_surrender:
		pos_x = 280
		choose = False
		while not choose: 
			screen.blit(img, (255, 227))
			screen.blit(popup_cursor, (pos_x, 227))
			pg.display.update()

			for event in pg.event.get():
				if event.type == KEYDOWN:
					if event.key == K_LEFT:
						pos_x = 280

					elif event.key == K_RIGHT:
						pos_x = 460

					elif event.key == K_LCTRL:
						cursor_confirm.play()
						enemy_wants_surrender = False
						enemy_wants_restart = False 
							
						if pos_x == 280:
							sock.send(answer)
							if answer == ".;~[/accres":
								pass
						
						choose = True

				elif event.type == QUIT: #Clicar no x da janela fecha o jogo
					sock.send(".;~[/out")#Informa o servidor de que o jogo foi fechado
					return

def receive_packet():
	global vez
	global enemy_wants_surrender
	global enemy_wants_restart
	global pack
	global chat_queue

	while True:
		msg = sock.receive()
		if msg == ".;~[/vez":
			sock.send(".;~[/vez recebida")		#Informa ao servidor que recebeu a vez
			pack = receive_pack()
			sock.send(".;~[/objetos recebidos")	#Informa ao servidor que recebeu as peças do inimigo
			vez  = True
			
		elif msg[:5] != ".;~[/": #é uma mensagem do chat
			chat_queue.append(msg)			   #Armazena a mensagem no array de mensagens
			show_chat_window()

		elif msg == ".;~[/re":				   #Recebe pedido de reinício de jogo
			enemy_wants_restart = True

		elif msg == ".;~[/su":				   #Recebe pedido de desistência
			enemy_wants_surrender = True

		elif msg == ".;~[/accres":			   #Pedido de restart aceito(não implementado)
			pass
			
		elif msg == ".;~[/accsu":			   #Pedido de desistência (não implementado)
			pass

def write_in_chat(event, screen):
	global current_string
	global chat 
	global chat_queue

	if event.key == K_BACKSPACE:
		current_string = current_string[0:-1]	  #A tecla backspace apaga uma letra.

	elif event.key == K_RETURN:		         	  #Tecla para enviar mensagem no chat (Enter)
		sock.send(chat)					 	 	  #Envia a mensagem para o outro jogador
		chat_queue.append(chat)				 	  #Insere nova mensagem no array do chat
		current_string = []					 	  #Esvazia o buffer da mensagem digitada
		show_chat_window()						  #Atualiza o chat

	elif event.key <= 255:						  #Aceita letras no padrão ASCII
		if len(current_string) < 28:		 	  #Limita a caixa de digitação em 28 caracteres
			current_string.append(chr(event.key)) #Armazena cada tecla digitada para formar a mensagem. Ex: (["o"], ["l"], "[a]")

	chat = string.join(current_string, "")		  #Junta as letras digitadas em uma string só. Ex: ("ola")
	screen.blit(update_msg_box, (0, 0))			  #Desenha a caixa de entrada de texto
	screen.blit(font.render(chat, 1, (255, 255, 255)), (610, 535)) #Desenha a palavra digitada
	pg.display.update()											   #Renderiza a tela

def show_chat_window():
	global chat_queue
	
	if len(chat_queue) == 27: #Se a caixa de mensagens estiver cheia
		chat_queue.pop(0)	  #Remove a primeira mensagem da lista
	
	pos_y = 55
	screen.blit(update_chat, (0, 0))
	for msg in chat_queue:
		screen.blit(font.render(msg, 1, (0, 0, 0)), (590, pos_y))
		pos_y += 18

	pg.display.update()

def main():
	global screen

	screen = pg.display.set_mode(SCREEN_SIZE)		#Tamanho da janela
	screen.fill(BACKGROUND_COLOR)				    #Cor de fundo
	pg.display.set_caption(CAPTION)					#Título da janela
	
	#Variáveis globais que precisam ser alteradas pelas funções fora do main
	global vez	
	global enemy_wants_surrender
	global enemy_wants_restart
	global pack
	global chat
	global chat_queue
	global current_string
	global player_army
	global enemy_army 
	global map_obj
	global map_objB

	vez 	    	        = False 	#Vez do jogador
	enemy_wants_surrender   = False	#Inimigo pediu para desistir
	enemy_wants_restart     = False  	#Inimigo pediu para reiniciar
	pack = "empty"				#Armazena o pacote do exército inimigo

	cursor 	    = Cursor() 		#Objeto cursor
	move_cursor = True			#Define que o jogador pode mover o cursor
	
	player_army = []			#Array que armazena o exército do jogador
	enemy_army  = []			#Array que armazena o exército do inimigo
	map_obj     = [0]*100       #Armazena os objetos do mapa (Player 1)
	map_objB    = [0]*100       #Informa se a posição no mapa está ocupada e se é do jogador ou do inimigo 

	action	    = False			#Define que o jogador não pode finalizar a jogada ainda
	end		    = False			#Define o fim do jogo
	win_game	= False			#Define condição de vitória
	current_string = []  		#Armazena as letras em um array para formar a mensagem 
	chat           = ""	        #Concatena a mensagem que será enviada no chat utilizando o array acima
	chat_queue     = []  		#Armazena as mensagens da janela do chat

	load_sprites()								   #Carrega os sprites
	create_army(player_army)					   #Cria o exército do jogador
	create_army(enemy_army)      			       #Cria o exército do inimigo
	give_pos(player_army) 								   #Distribui o exército do jogador no tabuleiro
	insert_obj(player_army, 1)		   #Insere o exército do inimigo nas listas de controle de tabuleiro
	
	pack_and_send()  							   #Envia o exército do jogador para o servidor
	pack = receive_pack()						   #Aguarda receber o pacote do exército inimigo para atualizar os dados
	update_enemy_army(pack)  #Atualiza os dados do exército do inimigo (x, y, t, L)
	pack = "empty"								   #Esvazia o pacote do exército inimigo

	insert_obj(enemy_army, 2)   #Insere o exército do inimigo nas listas de controle de tabuleiro
	screen.blit(start, (0, 0))                     #Desenha o cenário completo		   
	draw_player(screen, player_army, 1)		   #Desenha o exército do jogador 
	draw_player(screen, enemy_army, 2)   #Desenha o exército do inimigo
	pg.display.update()						       #Renderiza a tela

	receive = Thread(target = receive_packet)	   #Thread que gerencia os pacotes recebidos
	receive.start()								   #Inicia a thread
#Laço do jogo
	while not end: 
		while not vez:							   #Enquanto não for a vez do jogador
			for event in pg.event.get():		   #Verifica eventos 
				if event.type == KEYDOWN:		   #Se o evento for uma tecla pressionada
					write_in_chat(event, screen)   #Chama a função para escrever no chat
					ask_surrender_or_restart(event)#Verifica se o jogador se rendeu ou pediu para reiniciar
					accept_restart_or_surrender()  #O jogador decide se vai aceitar a rendição/reinício

				elif event.type == QUIT: #Clicar no x da janela fecha o jogo
					sock.send(".;~[/out")#Informa o servidor de que o jogo foi fechado
					return

			if vez:	    						   #Se for a vez do jogador
				update_enemy_army(pack)            #Atualiza os dados do exército inimigo (x, y, t, L)		
				pack = "empty"								   #Esvazia o pacote que armazena o exército inimigo
				insert_obj(enemy_army, 2)   #Insere o exército inimigo nas listas de controle de tabuleiro		
				
				screen.blit(update_board, (0, 0))			#Desenha o tabuleiro
				draw_player(screen, player_army, 1)		#Desenha o exército do jogador 
				draw_player(screen, enemy_army, 2)#Desenha o exército do inimigo
				pg.display.update()						    #Renderiza a tela

		while move_cursor and vez:						#Enquanto for a vez do jogador ele pode mover o cursor
			screen.blit(update_board, (0, 0))		    #Desenha o tabuleiro
			draw_player(screen, player_army, 1)		#Desenha o exército do jogador 1
			draw_player(screen, enemy_army, 2)#Desenha o exército do inimigo
			cursor.draw(screen)							#Desenha o cursor
			pg.display.update()							#Renderiza a tela

			for event in pg.event.get():  #Verifica eventos
				if event.type == KEYDOWN: #Se uma tecla é pressionada (direcionais do teclado)
					write_in_chat(event, screen) #Chama função para escrever no chat
					ask_surrender_or_restart(event)#Verifica se o jogador se rendeu ou pediu para reiniciar
					accept_restart_or_surrender()  #O jogador decide se vai aceitar a rendição/reinício
					
					cursor.move(event)	  #Move o cursor
					index = return_index(cursor.get_pos_x(), cursor.get_pos_y()) #Índice usado para detectar qual objeto está na casa
					my_soldier = map_obj[index]								     #O objeto escolhido é o que está no índice da função acima
					
					#Se pressionou enter && a casa contém um herói && diferente de mina && diferente de prisioneiro
					if event.key == K_LCTRL and map_objB[index] == 1 and my_soldier.get_tipo() != 0 and my_soldier.get_tipo() != 11: 
						cursor_confirm.play() #Toca som de confirmação
						cursor.set_pressed(1) #O cursor muda para "selecionado"
						action = True		  #O jogador deverá finalizar a jogada escolhendo para onde vai mover o objeto escolhido
						move_cursor = False	  #O jogador não poderá mais mover o cursor
						#Armazena a casa atual do objeto (após o jogador mudar a posição, essa passa a ser a posição anterior)
						actual_house = return_index(my_soldier.get_pos_x(), my_soldier.get_pos_y())  

				elif event.type == QUIT: #Clicar no x da janela fecha o jogo
					sock.send(".;~[/out")
					return
			time.sleep(0.1)

		while action:
			screen.blit(update_board, (0, 0))			
			draw_player(screen, enemy_army, 2)#Desenha o exército do jogador 2
			draw_player(screen, player_army, 1)		#Desenha o exército do jogador 1
			screen.blit(classe[my_soldier.get_tipo()], (my_soldier.get_pos_x(), my_soldier.get_pos_y()))
			cursor.draw(screen)							#Desenha o cursor
			pg.display.update()							#Renderiza a tela

			#Movimenta o herói
			for event in pg.event.get():
				if event.type == KEYDOWN:      #Se uma tecla é pressionada (enter)
					write_in_chat(event, screen)
					ask_surrender_or_restart(event)#Verifica se o jogador se rendeu ou pediu para reiniciar
					accept_restart_or_surrender()  #O jogador decide se vai aceitar a rendição/reinício

					my_soldier.walk(event, cursor.get_pos_x(), cursor.get_pos_y(), map_objB) #Herói da casa anda
					new_house = return_index(my_soldier.get_pos_x(), my_soldier.get_pos_y())
					
					if actual_house != new_house: #Não permite mover para a mesma posição
						if event.key == K_LCTRL:
							cursor_confirm.play()
							is_enemy = return_index(my_soldier.get_pos_x(), my_soldier.get_pos_y())
							
							win_combat = False
							#Se tem uma peça do inimigo na nova casa
							if map_objB[is_enemy] == 2: 
								enemy_soldier = map_obj[is_enemy]
								win_combat = combat(my_soldier, actual_house, enemy_soldier, map_obj, map_objB, win_game)

							#Nova posição está vazia || Se ganhar o combate:
							if map_objB[is_enemy] == 0 or win_combat:
								map_objB[index] = 0                #Posição antiga da casa recebe 0
								newIndex = return_index(my_soldier.get_pos_x(), my_soldier.get_pos_y()) #Novo índice após mover herói
								map_obj[newIndex] = my_soldier     #Insere o objeto na nova posição
								map_obj[index] = 0  			   #Posição antiga do objeto recebe 0
								map_objB[newIndex] = 1 			   #Nova posição recebe 1

							screen.blit(update_board, (0, 0))
							draw_player(screen, player_army, 1)		#Desenha o exército do jogador 1
							draw_player(screen, enemy_army, 2)#Desenha o exército do jogador 2
							pg.display.update()						    #Renderiza a tela

							cursor.set_pressed(0)
							action = False
							update_my_army(player_army, map_obj, map_objB)
							pack_and_send()	
							vez = False
							move_cursor = True

				elif event.type == QUIT: #Clicar no x da janela fecha o jogo
					return
			time.sleep(0.1)

if __name__ == "__main__":
	main()