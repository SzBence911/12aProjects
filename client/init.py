#!python3
"""
Main root for the client, managing switching in-between the different interfaces of the client: 
		login - read - write
Run offline:
	cmd: python3 init.py offline
Missing Communication with the server.
"""
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import socket,threading,time,os,getpass
from datetime import datetime as dt

from client_gui import EmailGui, WriteLetterDialog, AuthenticationDialog, ShowLetter

class EmailClient(Frame):
	"""
	Class(host:id/ip, port:n, name:id)
	Main modul of client.
	Redirection between interfaces."""
	def __init__(self, host, port, name, online):
		Frame.__init__(self)
		self.online=online
		self.master.resizable(0,0)
		self.master.protocol("WM_DELETE_WINDOW", self._delete_window)
		self.center_window()
		self.connected=False
		#self.master.attributes('-fullscreen', True)

		# Widgets #
		self.auth = AuthenticationDialog(self)
		
		#online mode
		self.data = [StringVar(),StringVar(),StringVar()]
		self.data[0].set(host)
		self.data[1].set(port)
		self.data[2].set(name)
		if online:
			self.connect()
		if self.connected:
			self.c=Communication(self.connection,self)
			self.c.start()

		#start

		self.auth.grid()
		self.grid()

		self.master.title('Login or register')


	def _delete_window(self):
		"function to close active connections before exiting"
		try:
			self.connection.send(bytes('#fin#', 'utf-8'))
		except Exception as e:
			pass
		finally:
			self.master.destroy()

	def center_window(self):
		"center the window."
		self.master.update_idletasks()
		self.master.geometry("+%d+%d" % (self.master.winfo_screenwidth()/2-(self.master.winfo_reqwidth()/2),
                                  self.master.winfo_screenheight()/2-(self.master.winfo_reqheight()/2)-75))


	def login_success(self, user):
		"f(user)"
		self.master.title('Email-client')
		self.auth.grid_forget()
		self.user = user
		self.client = EmailGui(self, user)
		self.client.grid()
		self.center_window()

	def logout(self):
		"Users auth-ed mail frame has destroyed self." #prolly thats not the right way tho
		self.auth.grid()
		self.master.title('Login or register')
		self.center_window()
		
	def write_letter(self):
		"Go to writing dialog."
		self.client.grid_forget()
		self.master.title('Send new message')
		self.send = WriteLetterDialog(self, self.user)
		self.send.grid()
		self.center_window()

	def send_over(self):
		"Get back to (re-grid) incoming mails, when the writing dialog is closed."
		self.master.title('Email-client')
		self.client.grid()
		self.center_window()

	def connect(self):
		self.connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Csatlakozás - IPv4: {0}, Port: {1}".format(self.data[0].get(),self.data[1].get()))
		HOST, PORT=self.data[0].get(),int(self.data[1].get())
		try:
			self.connection.connect((HOST, PORT))
			print("A kapcsolat létrejött.")
			self.connection.send(bytes(self.data[2].get(), 'utf-8'))
			self.data[2].set(self.connection.recv(1024).decode('utf-8'))  #may receive a unique id
			self.connected=True
		except socket.error as e:
			print(str(e))
			print("A kapcsolat meghiúsult")
			self.connected=False
			return

class Communication(threading.Thread):
	"""docstring for Communication"""
	def __init__(self, conn, root):
		threading.Thread.__init__(self)
		self.conn = conn
		self.root = root

	def run(self):
		while 1:
			if self.root.connected:
				self.conn.send(bytes("a", 'utf-8'))
				sleep(60)
			else:break
		

if __name__ == '__main__':
	import sys
	online=True
	print(sys.argv)
	if len(sys.argv)>1 and sys.argv[1]=="offline":
		online=False
	host = socket.gethostname()  # Get local machine name
	port = 50000  # Reserve a port for your service.
	name = os.environ['COMPUTERNAME']+'\\'+getpass.getuser() # log in with username
	root=EmailClient(host, port, name, online)
	root.mainloop()