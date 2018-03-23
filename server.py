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

class SocketServer():
	def __init__(self):
		self.port = port
		self.ip   = ip
		self.conn = [None]*2
		self.addr = [None]*2

		try:
			self.sock = socket(AF_INET, SOCK_STREAM)
			self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
			self.sock.bind((ip, self.port))

		except:
			print "Error"

	def listen(self, n_conn):
		self.sock.listen(n_conn)
		print "Servidor escutando na porta " + str(self.port)
		print "Servidor possui ip: " + str(self.ip) + "\n"

	def close(self):
		self.sock.close()