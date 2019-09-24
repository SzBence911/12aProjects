from crypting import *
from socket import *
import threading
import datetime
import time

connected = {}
idtimer = {}

def newcon(c, addr,con):    #get connection type
    data = c.recv(1024)
    if data.split(';', 0) == "r":
        registerin(data,c)
    elif data.split(';', 0) == "l":
        loggingin(data,c)

def send(c): #If user want to send mail
    c.send("1")
    out = 0
    while True:
        data = c.recv(2048) #256 char buffer
        if data is not None:
            store(data)
        else:
            out += 1
        if out > 10:
            break

def receive(c): #If user have new mail and he logged in
    store(con)

def store(data): #Store emails
    print("sucess")
    return True

def logged(id, name,c): #Pin  user to connected dictionary
    if id in connected.keys():
        while True:
            try:
                data = c.recv(40)
            except:
                data = False
            if data != False:
                data.split(';', 1)
                if data[1] == "s":
                    send(c)
                elif data[1] == "r":
                    receive(c)

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
                idtimer[count1] = 0
                c.send(count1)
                logged(count1, data[1],c)

def log(s):  # logs
    with open("logs/" + datetime.datetime.now().strftime("%Y.%m.%d") + "-console-log.log",encoding="utf-8", mode="a") as f:
        f.write(s + "\n")

def kicker():
    while True:
        time.sleep(1)
        counter = 0
        while counter < idtimer[-1]:
            if counter in idtimer.keys():
                idtimer[counter] += 1
                if idtimer[counter] > 600:
                    del idtimer[counter]
                    del connected[counter]

s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 50000  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port
s.listen(5)  # Now wait for client connection.
print(createdb("Users"))
print(createtb("Users", "useraut"))
kick = threading.Thread(target=kicker, args=())
kick.start()
while True: #Create thread to new connection
    c, addr = s.accept()
    con = threading.Thread(target=newcon, args=(c,addr,con))
    con.start()
s.close()
