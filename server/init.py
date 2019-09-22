from crypting import *
from socket import *
import threading
import datetime

connected = {}

def newcon(c, addr,con):    #get connection type
    data = c.recv(1024)
    if data.split(';', 0) == "r":
        registerin(data,c)
    elif data.split(';', 0) == "l":
        loggingin(data,c)

def send(con, mail): #If user want to send mail
    mail = mail


def receive(con): #If user have new mail and he logged in
    store(con)

def store(con): #Stone emails
    print("sucess")

def logged(id, name,c): #Pin  user to connected dictionary
    connected[id] = name

def registerin(data,c): #Register user to the system using DB
    data = data.split(';', 2)
    register(data[2], data[1])
    loggingin(data[0]+ data[1]+data[2],c)

def loggingin(data,c):    #Get datas from DB(Is user existed?)
    data = data.split(';', 2)
    suc = login(data[2], data[1])
    if suc == True:
        count1 = 0
        while True:
            if count1 in connected.keys():
                count1 += 1
            else:
                log(data[1] + " sikeresen bejelentkezett")
                connected[count1] = data[1]
                c.send(count1)
                logged(count1, data[1],c)

def log(s):  # logs
    with open("logs/" + datetime.datetime.now().strftime("%Y.%m.%d") + "-console-log.log",encoding="utf-8", mode="a") as f:
        f.write(s + "\n")

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
