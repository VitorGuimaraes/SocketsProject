# -*-coding: utf-8-*-
from socket import* 
from Tkinter import *
from menu import StartMenu

s = socket(AF_INET, SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
my_ip = s.getsockname()[0]
s.close()

root = Tk()
menu = StartMenu(root, "Server", my_ip)
root.mainloop()

ip   =  menu.retrieved_ip
port = int(menu.retrieved_port)

class SocketClient():
	def __init__(self):
		self.host = ip
		self.port = port

		try:
			self.sock = socket(AF_INET, SOCK_STREAM)
			self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
			self.sock.connect((self.host, self.port))
			print "Cliente se conectou"
			
		except:
			print "Falha ao conectar com o servidor"

	def receive(self):
		return self.sock.recv(2048)

	def send(self, packet):
		self.sock.send(packet)