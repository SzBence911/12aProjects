#!python3
"""
GUI for the email client.
Edited by:
Aron L. Hertendi: 
	- class EmailGui: a sketch
		^ methods: __init__, _delete_window, treeview_sort_column, tv_double, login, logout, eregister, refresh, sendMSG, delMSG, login_success, login_fail, logout_success
	- class WriteLetter: a sketch
		^ methods: __init__, send, end
...
"""

from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import socket,threading,time,os
from datetime import datetime as dt

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

		self.b_login = ttk.Button(self, text = "Login", command = self.login, state = NORMAL)
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

		self.b_login.grid(row=0, column=1)
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
		self.login_success() #for test

	def logout(self):
		"logout process"
		self.logout_success()

	def eregister(self):
		"registration dialog"
		pass

	def refresh(self):
		"reloading mails"
		pass

	def sendMSG(self):
		"Letter writing dialog"
		writing=WriteLetter(self)

	def delMSG(self):
		"Letter deletion dialog"
		pass

	def login_success(self):
		"actions to do on successful login #GUI"
		self.b_send.config(state=NORMAL)
		self.b_logout.config(state=NORMAL)
		self.b_del.config(state=NORMAL)
		self.b_refresh.config(state=NORMAL)
		
		self.b_login.config(state=DISABLED)
		self.b_register.config(state=DISABLED)

	def login_fail(self):
		"actions to do on failed login attempt"
		pass

	def logout_success(self):
		"actions to do on logout #GUI"
		self.b_send.config(state=DISABLED)
		self.b_logout.config(state=DISABLED)
		self.b_del.config(state=DISABLED)
		self.b_refresh.config(state=DISABLED)
		
		self.b_login.config(state=NORMAL)
		self.b_register.config(state=NORMAL)


class WriteLetter(Toplevel):
	"""Toplevel window for email writing"""
	def __init__(self,master):
		Toplevel.__init__(self, master)
		self.master = master
		self.grab_set()
		self.title("Send message")
		self.geometry("+%d+%d" % (self.master.winfo_rootx()+50,
                                  self.master.winfo_rooty()+50))
		self.resizable(0,0)
		self.transient(self.master)

		# Objects
		Label(self,text="Mail to:").grid(row=0, column=0, pady=5, sticky=NE)
		Label(self,text="Subject:").grid(row=1, column=0, pady=5, sticky=NE)
		Label(self,text="Mail:").grid(row=2, column=0, pady=5, sticky=NE)

		self.e_Address=ttk.Entry(self, width=67)
		self.e_Address.grid(row=0, column=1, pady=5)

		self.e_Subject=ttk.Entry(self, width=67)
		self.e_Subject.grid(row=1, column=1, pady=5)

		self.textbox=Text(self, width=50)
		self.textbox.grid(row=2, column=1, pady=10, padx=10,rowspan=10)

		self.b_sendmail=ttk.Button(self, text="Send", width=7, command=self.send)
		self.b_sendmail.grid(row=10, column=0,sticky=SE,padx=6)

	def send(self):
		"sending the letter after formally checked"
		address=self.e_Address.get()
		subject=self.e_Subject.get()
		message=self.textbox.get(1.0,END)
		date=str(dt.now())[5:10].replace("-",".")
		#check address syntax
		if "@" in address:
			if "." in address.split("@")[1]:
				if len(address.split("@")[1].split('.')[1])>0:
					pass
				else:messagebox.showinfo('Error', "Invalid address");return
			else:messagebox.showinfo('Error', "Invalid address");return
		else:messagebox.showinfo('Error', "Invalid address");return
		#check Subject syntax: 1 word, 15 ch at max
		if " " in subject or len(subject)>15:
			messagebox.showinfo('Error', "Invalid subject")
			return
		elif subject=="":
			cont = messagebox.askyesno('No subject', 'Are you sure you want to send this message without a subject specified?')
			if not cont: return


		#close window after the process, if succeeded, otherwise returned before with a messagebox description of what happened
		self.end()

	def end(self):
		self.destroy()
		

if __name__ == '__main__':
	root = EmailGui()
	root.mainloop()