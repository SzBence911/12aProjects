#!python3
"""
GUI for the email client.
Edited by:
Aron L. Hertendi: 
	- class EmailGui: a scratch
		^ methods: __init__, _delete_window, treeview_sort_column, tv_double, login, logout, eregister, refresh, sendMSG, delMSG
...
"""

from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import socket,threading,time,os

class EmailGui(Frame):
	"""Main dialog"""
	def __init__(self):
		Frame.__init__(self)

		# Frame properties #
		
		self.master.title('Email-client')
		self.master.resizable(0,0)
		self.master.protocol("WM_DELETE_WINDOW", self._delete_window)
		#self.master.attributes('-fullscreen', True)
		self.master.geometry("+%d+%d" % (self.master.winfo_rootx()+50,
                                  self.master.winfo_rooty()+50))

		# Objects #

		self.b_Login = ttk.Button(self, text = "Login", command = self.login, state = NORMAL)
		self.b_logout = ttk.Button(self, text = "Logout", command = self.logout, state = DISABLED)
		self.b_register = ttk.Button(self, text = "Register", command = self.eregister, state = NORMAL)
		self.b_refresh = ttk.Button(self, text = "Refresh", command = self.refresh, state = DISABLED)
		self.b_send = ttk.Button(self, text = "Send new", command = self.sendMSG, state = DISABLED)
		self.b_del = ttk.Button(self, text = "Delete", command = self.delMSG, state = DISABLED)

		self.tv = ttk.Treeview(self, columns=("Title", "Subject", "Date", "Read"), show="headings")

		# Treeview costumize

		for x in self.tv["columns"]:
			self.tv.heading(x, text=x, command=lambda _col=x: self.treeview_sort_column(self.tv, _col, True), anchor=N)
		self.tv.column("Date", width=50)
		self.tv.column("Read", width=50)

		#TEST LINES		- TO BE DELETED
		self.tv.insert("" , 0, values=("Egy","C", "05.05.", "Read"))
		self.tv.insert("" , 1, values=("Kettő","A", "05.06.", "New"))
		self.tv.insert("" , 2, values=("Három","B", "05.03.", "New"), text="id03") #letter id goes to 'text', which is hidden by show="headings" in line(32): define self.tv
		#END

		#Bindings
		self.tv.bind("<Double-1>", self.tv_double) #double click to read an email

		# Grid #

		self.b_Login.grid(row=0, column=1)
		self.b_logout.grid(row=1, column=1)
		self.b_register.grid(row=0, rowspan=2, column=2, ipady =20, padx=5)
		self.b_refresh.grid(row=2, column=1,padx=5)
		self.b_send.grid(row=3, column=1, padx=5)
		self.b_del.grid(row=4, column=1, padx=5)
		self.tv.grid(row=0, rowspan=10, column=0)
		self.grid()

	def _delete_window(self):
		"function to close active connections before exiting"
		try:
			self.connection.send(bytes('#fin#', 'utf-8'))
		except Exception as e:
			pass
		finally:
			self.master.destroy()

	def treeview_sort_column(self,tv, col, reverse):
		"function to sort letters by col - thx stackoverflow"
		l = [(tv.set(k, col), k) for k in self.tv.get_children('')]
		l.sort(reverse=reverse)

		# rearrange items in sorted positions
		for index, (val, k) in enumerate(l):
			tv.move(k, '', index)

		# reverse sort next time
		tv.heading(col, command=lambda: \
					self.treeview_sort_column(self.tv, col, not reverse))

	def tv_double(self,event):
		item =self.tv.identify('item',event.x,event.y)
		print("you clicked on", self.tv.item(item))
		if self.tv.item(item,"values"):
			pass
			# will read email based on the id in self.tv.item(item, "text")
			# which means on the server side the email is considered read, and on successful read, we refresh this property on client-side

	def login(self):
		"login dialog"
		pass

	def logout(self):
		"logout process"
		pass

	def eregister(self):
		"registration dialog"
		pass

	def refresh(self):
		"reloading mails"
		pass

	def sendMSG(self):
		"Letter writing dialog"
		pass

	def delMSG(self):
		"Letter writing dialog"
		pass


if __name__ == '__main__':
	root = EmailGui()
	root.mainloop()