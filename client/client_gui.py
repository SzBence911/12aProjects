#!python3
"""
GUI for the email client.
Edited by:
Aron L. Hertendi: 
	- class EmailGui: a frame where you can read, refresh, delete e-mails or log out
		^ params: master, user
		^ methods: __init__, load_mails, treeview_sort_column, treeview_double_click, logout, delMSG
	- class WriteLetterDialog: a frame for email editing
		^ params: master, user
		^ methods: __init__, send, end, checkInvalidCh
	- class AuthenticationDialog: a frame for logging in or creating new account
		^ params: master
		^ methods: __init__, get_data, eregister, hasher, checkInvalidCh, login, reminder
	- class Showletter: Toplevel window describing a double-clicked letter
		^ params: master,sender,subject,message,date
...MISSING:
	^ online version.
...Known bugs:
	^ App showing other mail than the one that was clicked.
	^ Long mails
"""

from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import socket,threading,time,os
from datetime import datetime as dt

class EmailGui(Frame):
	"""
		A Frame class which let's the successfully logged in user to browse, sort, delete and initiate writing e-mails.
		NOTE: This frame does not displays itself on it's master upon init.
			Methods:
				__init__ (master, user):
					- creating, costumizing and showing widgets
					- loading the user's incoming e-mails
					- adding bindings
	"""
	def __init__(self, master, user):
		Frame.__init__(self, master)
		self.master = master
		self.user = user

		# Create the widgets
		self.b_logout = ttk.Button(self, text = "Logout", command = self.logout, state = NORMAL)
		self.b_refresh = ttk.Button(self, text = "Refresh", command = self.load_mails, state = NORMAL)
		self.b_write_mail = ttk.Button(self, text = "Send new", command = self.master.write_letter, state = NORMAL)
		self.b_delete_mail = ttk.Button(self, text = "Delete", command = self.delMSG, state = NORMAL)

		self.mail_treeview = ttk.Treeview(self, columns=("From", "Subject", "Date", "Read"), show="headings")

		# Treeview costumize
		for x in self.mail_treeview["columns"]:
			self.mail_treeview.heading(x, text=x, command=lambda _col=x: self.treeview_sort_column(self.mail_treeview, _col, True), anchor=N)
		self.mail_treeview.column("Date", width=70)
		self.mail_treeview.column("Read", width=70)

		# Bindings #
		self.mail_treeview.bind("<Double-1>", self.treeview_double_click) #double click to read an email

		# Manage Mails #
		self.mails=[]
		self.load_mails()
		
		# Grid #
		self.b_logout.grid(row=1, column=1)
		self.b_refresh.grid(row=2, column=1,padx=5)
		self.b_write_mail.grid(row=3, column=1, padx=5)
		self.b_delete_mail.grid(row=4, column=1, padx=5)
		self.mail_treeview.grid(row=0, rowspan=10, column=0)

		

	def load_mails(self):											#FROMSERVER
		"Function to load the user's incoming mails."
		self.mail_treeview.delete(*self.mail_treeview.get_children())
		self.mail_count=0
		with open("{0}.txt".format(self.user), 'a') as f:pass
		with open("{0}.txt".format(self.user), 'r') as f:
			self.mails=[x[:-1] for x in f.readlines()]
		for x in self.mails:
			x=x.split()
			self.mail_treeview.insert("" , self.mail_count, values=(x[0].replace("[kukac]","@"), x[1],x[2], x[3]), text=str(self.mail_count))

	def treeview_sort_column(self,mail_treeview, col, reverse):
		"f(panel: ttk.Treeview, sorting column id, reverse: bool)\nFunction to sort letters when a column is selected to be sorted by - thx stackoverflow"
		l = [(mail_treeview.set(k, col), k) for k in self.mail_treeview.get_children('')]
		l.sort(reverse=reverse)

		# rearrange items in sorted positions
		for index, (val, k) in enumerate(l):
			mail_treeview.move(k, '', index)

		# reverse sort next time
		mail_treeview.heading(col, command=lambda: \
					self.treeview_sort_column(self.mail_treeview, col, not reverse))

	def treeview_double_click(self,event):								#TOSERVER
		"f(double click:event) Function binded to double clicking, detecting which mail was chosen, forwarding it to class ShowLetter"
		item = self.mail_treeview.identify('item',event.x,event.y)
		if self.mail_treeview.item(item,"values"):
			i = int(self.mail_treeview.item(self.mail_treeview.focus())["text"])
			self.mails[i] = self.mails[i].replace("olvasatlan", "olvasott")
			with open("{0}.txt".format(self.user), 'w') as f:
				for x in self.mails:
					f.write(x+"\n")
			self.load_mails()
			mail=self.mails[i][self.mails[i].find("{")+1:-1]
			mail_attr=self.mails[i].split()
			ShowLetter(self, mail_attr[0].replace("[kukac]","@"),mail_attr[1], mail, mail_attr[2])
			# will read email based on the id in self.mail_treeview.item(item, "text")
			# which means on the server side the email is considered read, and on successful read, we refresh this property on client-side

	def logout(self):
		"logout process"
		self.destroy()
		self.master.logout()


	def delMSG(self):							#TOSERVER
		"Letter deletion dialog"
		focus=self.mail_treeview.focus()
		if not focus:return
		cont = messagebox.askyesno('Delete', 'Are you sure you want to delete the selected message?')
		if not cont: return
		#index of letter to be deleted in stored self.mails
		i=int(self.mail_treeview.item(focus)["text"])
		del self.mails[i]
		with open("{0}.txt".format(self.user), 'w') as f:
			for x in self.mails:
				f.write(x+"\n")

		self.mail_treeview.delete(focus)


class ShowLetter(Toplevel):
	"""Toplevel class for displaying mails."""
	def __init__(self, master,sender,subject,message,date):
		Toplevel.__init__(self,master)
		self.master = master
		self.sender = sender
		self.subject = subject
		self.message = message
		self.date = date
		self.title("Email")
		Label(self,text="From: %s\nSubject: %s\n\nMessage:\n%s\n\n%s"%(sender, subject, message, date), justify=LEFT).grid()
		self.update_idletasks()
		self.geometry("+%d+%d" % (self.master.winfo_screenwidth()/2-(self.master.winfo_reqwidth()/2),
                                  self.master.winfo_screenheight()/2-(self.master.winfo_reqheight()/2)-75))
		

class WriteLetterDialog(Frame):
	"""
		A Frame class containing the mail writing dialog.
		NOTE: This frame does not displays itself on it's master upon init, but does destroy self on send or back action.
			Methods:
				__init__:
					- inicializing widgets
					- saving the valid characters to be used in different functions
				send:
					- getting the inputs from the form
					- verifying correct the correct mail formulas
					- sending out the mail (to txt file)
				checkInvalidCh:
					- checks for invalid chars
				end:
					- destroys self, notifies/calls master's send_over method
				"""
	def __init__(self,master,user):
		Frame.__init__(self, master)
		self.master = master
		self.user = user

		# Widgets

		Label(self,text="Mail to:").grid(row=0, column=0, pady=5, sticky=NE)
		Label(self,text="Subject:").grid(row=1, column=0, pady=5, sticky=NE)
		Label(self,text="Mail:").grid(row=2, column=0, pady=5, sticky=NE)

		self.e_Address=ttk.Entry(self, width=67)
		self.e_Address.grid(row=0, column=1, pady=5)

		self.e_Subject=ttk.Entry(self, width=67)
		self.e_Subject.grid(row=1, column=1, pady=5)

		self.textbox=Text(self, width=50)
		self.textbox.grid(row=2, column=1, pady=10, padx=10,rowspan=10)

		self.b_back=ttk.Button(self, text="Back", width=7, command=self.end)
		self.b_sendmail=ttk.Button(self, text="Send", width=7, command=self.send)

		self.b_back.grid(row=9, column=0, sticky=SE, padx=6)
		self.b_sendmail.grid(row=10, column=0,sticky=SE,padx=6)

		# Valid chars
		self.validch=[chr(x) for x in range(97,123)]+[chr(x) for x in range(65,91)]+[str(x) for x in range(0,10)]

	def send(self):
		"sending the letter after formally checked"
		address=self.e_Address.get()
		subject=self.e_Subject.get()
		message=self.textbox.get(1.0,END)[:-1]
		date=str(dt.now())[5:10].replace("-",".")+"."
		#check address syntax
		if "@" in address or not self.checkInvalidCh(address):
			if "." in address.split("@")[1]:
				if len(address.split("@")[1].split('.')[1])>0:
					pass
				else:messagebox.showinfo('Error', "Invalid address");return
			else:messagebox.showinfo('Error', "Invalid address");return
		else:messagebox.showinfo('Error', "Invalid address");return
		#check Subject syntax: 1 word, 15 ch at max
		if " " in subject or len(subject)>15 or self.checkInvalidCh(subject):
			messagebox.showinfo('Error', "Invalid subject")
			return
		elif subject=="":
			cont = messagebox.askyesno('No subject', 'Are you sure you want to send this message without a subject specified?')
			if not cont: return
			else: subject = "nincs_megadva"   #this would be more proper to be on server side

		with open("{0}.txt".format(address[:-9]), 'a') as f:
			f.write(self.user+"@dusza.hu "+subject+" "+date+" olvasatlan "+"{"+message+"}\n")

		messagebox.showinfo('Success', "Email sent!")
		#close window after the process, if succeeded, otherwise returned before with a messagebox description of what happened
		self.end()

	def checkInvalidCh(self, string_):
		"f(str) checks for invalid chars in username/pass/reminder"			#should probably have used regex here,w/e works fine
		for x in string_:
			if x not in self.validch:
				return True
		return False
	def end(self):
		self.destroy()
		self.master.send_over()

class AuthenticationDialog(Frame):
	"""
		A Frame containing dialog for logging in or applying a registration.
		NOTE: This frame does not displays itself on it's master upon init.
			Methods:
				__init__:
					- inicializing widgets
					- saving the valid characters to be used in different functions
				get_data:
					- loads any existing user from file into var named data
				eregister:
					- collect data from registration dialog, check conditions, verify
					- save new acc to txt file
				hasher:
					- hashes the password up successful registration
				checkInvalidCh:
					- checks for invalid chars
				login:
					- login dialog, gathers data, notifies master on successful login by master's login_success method
				reminder:
					- displays a password reminder that was optionally set for the username
	"""
	def __init__(self, master):
		Frame.__init__(self, master)
		self.master = master

		# Widgets #
		self.e_user = ttk.Entry(self, width=19)
		self.e_password = ttk.Entry(self,show="☺", width=30)
		self.b_reminder = ttk.Button(self, text = "Remind me!", command = self.reminder, width=15, state=NORMAL)
		self.b_login = ttk.Button(self, text = "Login", command = self.login, width=30, state = NORMAL)

		self.e_reg_user = ttk.Entry(self, width=19)
		self.e_reg_pass = ttk.Entry(self, width=30,show="☺")
		self.e_reg_pass_confirm = ttk.Entry(self, width=30,show="☺")
		self.e_reg_pass_reminder = ttk.Entry(self, width=30)
		self.b_register = ttk.Button(self, text = "Register", command = self.eregister,width=30, state = NORMAL)

		Label(self, text="Username:").grid(row=0, column=0, sticky=E, padx=5, pady=5)
		Label(self, text="Password:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
		Label(self, text="@dusza.hu").grid(row=0, column=2, sticky=W)
		Label(self, text="@dusza.hu").grid(row=4, column=2, sticky=W)
		Label(self, text="New user:").grid(row=4, column=0, sticky=E, padx=5, pady=5)
		Label(self, text="Password:").grid(row=5, column=0, sticky=E, padx=5, pady=5)
		Label(self, text="Confirm Password:" ).grid(row=6, column=0, sticky=E, padx=5, pady=5)
		Label(self, text="Reminder:").grid(row=7, column=0, sticky=E, padx=5, pady=5)

		self.e_user.grid(row=0, column=1, padx=5, pady=5)
		self.e_password.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
		ttk.Separator(self).grid(row=3, column=0,columnspan=3, sticky="ew",padx=10)
		self.e_reg_user.grid(row=4, column=1, padx=5, pady=5)
		self.e_reg_pass.grid(row=5, column=1, padx=5, pady=5, columnspan=2)
		self.e_reg_pass_confirm.grid(row=6, column=1, columnspan=2, padx=5, pady=5)
		self.e_reg_pass_reminder.grid(row=7, column=1, columnspan=2, padx=5, pady=5)
		
		self.b_reminder.grid(row=2, column=0, padx=5, pady=5)
		self.b_login.grid(row=2,column=1, columnspan=2, padx=5, pady=5)
		self.b_register.grid(row=8,column=1, columnspan=2, padx=5, pady=5)
		
		# valid characters

		self.validch=[chr(x) for x in range(97,123)]+[chr(x) for x in range(65,91)]+[str(x) for x in range(0,10)]
		#self.grid()

	def get_data(self):			#FROMSERVER
		"Importing existing users from file."
		data = {}
		with open('adatok.txt', 'a') as f: pass #make sure it exists
		with open('adatok.txt', 'r') as f:
			adatok=[x[:-1] for x in f.readlines()]

		for x in adatok: 					# ["username hash reminder", "... .. ...",....]
			data[x.split()[0]]=(x.split()[1], x.split()[2])

		return data

	def eregister(self):		#TOSERVER
		"registration check"
		data = self.get_data()

		ERROR_MSG = (\
"""Username, password and the password reminder all the same, may not contain spaces and may only contain numbers or letters from the English alphabet.
Password length is 8 to 10. Username and password reminder length is 1 to 15.""")

		newUser   = self.e_reg_user.get()
		newReminder = self.e_reg_pass_reminder.get()

		if newUser in data:
			messagebox.showinfo('Error', "User already exists.")
			return

		if len(newUser)>15 or not newUser or ' ' in newUser:
			messagebox.showinfo('Error', ERROR_MSG)
			return
		if len(newReminder)>15 or ' ' in newReminder:
			messagebox.showinfo('Error', ERROR_MSG)
			return

		newPass = self.e_reg_pass.get()

		if len(newPass) not in [8,9,10] or not newPass:
			messagebox.showinfo('Error', ERROR_MSG)
			return

		if newPass!=self.e_reg_pass_confirm.get():
			messagebox.showinfo('Error', "Passwords not matching.")
			return

		if self.checkInvalidCh(newUser) or self.checkInvalidCh(newPass) or self.checkInvalidCh(newReminder):
			messagebox.showinfo('Error', ERROR_MSG)
			return

		if not newReminder: newReminder="#"
		# The data can be saved!
		with open('adatok.txt', 'a') as f:
			f.write("{0} {1} {2}\n".format(newUser, self.hasher(newPass), newReminder))
		self.e_reg_user.delete(0,END)
		self.e_reg_pass.delete(0,END)
		self.e_reg_pass_confirm.delete(0,END)
		self.e_reg_pass_reminder.delete(0,END)
		messagebox.showinfo('Success!', "Successful registration!")


	def hasher(self,password):				#ONSERVER?
		"f(pass:str) hashes the password."
		return sum([ord(x) for x in password + "d" * (10 - len(password))])
		
	def checkInvalidCh(self, string_):
		"checks for invalid chars in username/pass/reminder"			#should probably have used regex here,w/e works fine
		for x in string_:
			if x not in self.validch:
				return True
		return False


	def login(self):			#by server approve
		"login data check"
		data = self.get_data()
		user = self.e_user.get()
		if user not in data:
			messagebox.showinfo('Error', "Incorrect username.")
			self.e_user.delete(0,END)
			self.e_password.delete(0,END)
			return
		if str(self.hasher(self.e_password.get())) != data[user][0]:
			messagebox.showinfo('Error', "Incorrect password.")
			self.e_user.delete(0,END)
			self.e_password.delete(0,END)
			return
		self.e_user.delete(0,END)
		self.e_password.delete(0,END)
		self.master.login_success(user)

	def reminder(self):			#FROMSERVER
		"Shows the password reminder if was set."
		data = self.get_data()
		user = self.e_user.get()
		if user not in data:
			messagebox.showinfo('Password reminder', "No such username in the registry.")
			return
		else:
			if data[user][1]!="#":
				messagebox.showinfo('Password reminder', "Your password reminder is:\n{0}".format(data[user][1]))
			else:
				messagebox.showinfo('Password reminder', "You have no password reminder! :(")
			return
