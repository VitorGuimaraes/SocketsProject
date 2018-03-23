from Tkinter import*

class StartMenu:
	def __init__(self, master, title, my_ip):
		self.master  		  = master
		self.my_ip   		  = my_ip
		master.title 		  = title
		master.geometry("230x90")
		master.resizable(width = False, height = False)

		self.label_ip   = Label(master, text = "IP").grid(row = 0, column = 0)
		self.label_port = Label(text = "Port").grid(row = 1, column = 0)

		self.ip_input   = Entry(master, width = 14)
		self.ip_input.grid(row = 0, column = 1)
		self.ip_input.focus_force()

		self.port_input = Entry(master, width = 14)
		self.port_input.grid(row = 1, column = 1)
		self.port_input.focus_force()

		self.use_my_ip = Button(command = lambda:self.set_text(self.my_ip), text = "Use my IP", takefocus = False, width = 6)
		self.use_my_ip.grid(row = 0, column = 2)

		self.confirm = Button(command = self.close_window, text = "OK", takefocus = False, width = 6)
		self.confirm.grid(row = 2, column = 1)

	def set_text(self, text):
		self.ip_input.delete(0, END)
		self.ip_input.insert(0, text)
		return

	def close_window(self): 
		self.retrieved_ip   = self.ip_input.get()
		self.retrieved_port = self.port_input.get()
		self.master.destroy()