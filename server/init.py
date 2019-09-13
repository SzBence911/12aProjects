from database import *
from crypting import *
from socket import *
from conn import *
import threading

connected = {}

def newcon(c, addr,con):    #get connection type
    data = c.recv(1024)
    if data[0:1] == "r":
        register(data)
    elif data[0:1] == "l":
        loggingin(data)
    else:
        newcon(c,addr,con)

def send(con): #If user want to send mail
    receive(con)

def receive(con): #If user have new mail and he logged in
    store(con)

def store(con): #Stone emails
    print("sucess")

def logged(id, name): #Pin  user to connected dictionary
    connected[id] = name

def register(data): #Register user to the system using DB
    data = data

def loggingin(data):    #Get datas from DB(Is user existed?)
    data = data

s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 50000  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port
s.listen(5)  # Now wait for client connection.
print(createdb("Users"))
print(createtb("Users", "useraut"))
while True: #Create thread to new connection
    c, addr = s.accept()
    con = threading.Thread(target=newcon, args=(c,addr,con))
    con.start()
s.close()
