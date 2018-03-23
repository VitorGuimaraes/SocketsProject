# -*-coding: utf-8-*-
"""
Pacotes de exército chegam em momentos específicos e devem ser enviados em 
momentos específicos. Os outros pacotes podem chegar a qualquer momento
e devem ser enviados instantaneamente. Este é o caso de mensagens de chat, 
pedidos de rendição e reinício. Estes pacotes são armazenados na variável 
"packet" e os pacotes de exército são armazenados nas variáveis player1_json 
e player2_json
A forma utilizada para saber que chegou um pacote de exército é verificando o
tamanho dessas variáveis. Os clientes enviam json, que possuem tamanho médio
de 2000 bytes. 
"""
from socket import *
from threading import Thread
import time
from server import SocketServer

BUFFER = 2048

def main():
	sock = SocketServer()	#Instancia um objeto socket
	sock.listen(2)			#Servidor está escutando e aceita até duas conexões

	global player1_json 	#Armazena exército do jogador1
	global player2_json		#Armazena exército do jogador2

	player1_json = "empty"  #Inicia o pacote como "vazio"		
	player2_json = "empty"	#Inicia o pacote como "vazio"

	for i in range(0, 2):	#Aguarda os dois jogadores se conectares
		print "Aguardando jogador " + str(i+1) + " se conectar..."
		sock.conn[i], sock.addr[i] = sock.sock.accept()
		print "Cliente " + str(sock.addr[i]) + " conectado com sucesso!\n"

	#Recebe o exército do jogador1 e do jogador2
	player1_json = sock.conn[0].recv(BUFFER)
	player2_json = sock.conn[1].recv(BUFFER)

	#Envia o exército de um jogador para o outro
	sock.conn[0].send(player2_json)
	sock.conn[1].send(player1_json)

	#Libera o jogador1 para jogar
	sock.conn[0].send(".;~[/vez")

	def run_player1():		
		global player1_json  
		global player2_json 
		
		packet = ".;~[/"	
						
		while True:
			packet = sock.conn[0].recv(BUFFER)

			if len(packet) > 1024:	#É Pacote de exército
				sock.conn[1].send(".;~[/vez")
				player1_json = packet

			elif packet[:5] == ".;~[/": #Protocolo de confirmação de recebimento
				if packet == ".;~[/vez recebida":
					if len(player2_json) > 1024:	
						sock.conn[0].send(player2_json)
						player2_json = "empty"

				elif packet == ".;~[/re":
					sock.conn[1].send(".;~[/re") 		#É pedido de restart

				elif packet == ".;~[/su":
					sock.conn[1].send(".;~[/su") 		#É pedido de surrender

				elif packet == ".;~[/accres":
					sock.conn[1].send(".;~[/accres") 	#É resposta de restart

				elif packet == ".;~[/accsu":
					sock.conn[1].send(".;~[/accsu") 	#É resposta de surrender

				elif packet == ".;~[/out":
					sock.conn[1].send(".;~[/out") 	    #O jogador fechou o jogo

			elif packet[:5] != ".;~[/":	#É mensagem do chat
				sock.conn[1].send(packet)

			#Esvazia o pacote, senão quando voltar pro início do while vai considerar que uma mensagem chegou
			packet = ".;~[/"	

	def run_player2():
		global player1_json
		global player2_json
		
		packet = ".;~[/"
		
		while True:
			packet = sock.conn[1].recv(BUFFER)

			if len(packet) > 1024:	#É Pacote de exército
				sock.conn[0].send(".;~[/vez")
				player2_json = packet

			elif packet[:5] == ".;~[/": #Protocolo de confirmação de recebimento
				if packet == ".;~[/vez recebida":
					if len(player1_json) > 1024:	
						sock.conn[1].send(player1_json)
						player1_json = "empty"

				elif packet == ".;~[/re":
					sock.conn[0].send(".;~[/re") 		#É pedido de restart

				elif packet == ".;~[/su":
					sock.conn[0].send(".;~[/su") 		#É pedido de surrender

				elif packet == ".;~[/accres":
					sock.conn[0].send(".;~[/accres") 	#É resposta de restart

				elif packet == ".;~[/accsu":
					sock.conn[0].send(".;~[/accsu") 	#É resposta de surrender

				elif packet == ".;~[/out":
					sock.conn[0].send(".;~[/out") 	    #O jogador fechou o jogo

			elif packet[:5] != ".;~[/":	#É mensagem do chat
				sock.conn[0].send(packet)

			#Esvazia o pacote, senão quando voltar pro início do while vai considerar que uma mensagem chegou
			packet = ".;~[/"	 

	player1 = Thread(target = run_player1)
	player2 = Thread(target = run_player2)

	player1.start()
	player2.start()

if __name__ == "__main__":
	main()