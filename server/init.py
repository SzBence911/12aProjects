from crypting import *
import socket
import threading
import datetime
import time

connected = {}
idtimer = {}

def newcon(c, addr):    #get connection type
    data = c.recv(1024)
    data = str(data)
    print(data.split(';'))
    spliter = data.split(';')
    if spliter[1] == "r":
        print("reg required")
        registerin(spliter,c)
    elif spliter[1] == "l":
        loggingin(spliter,c)

def send(c,id): #If user want to send mail
    c.send("1")
    out = 0
    while True:
        data = c.recv(2048) #256 char buffer
        if data is not None:
            ret = False
            integ = -1
            while ret != True:
                integ += 1
                ret = createln("mails",connected[id],str(integ))
        else:
            out += 1
        if out > 10:
            break

def receive(c): #If user have new mail and he logged in
    while True:
        c.send()

def logged(id, name,c): #Pin  user to connected dictionary
    if id in connected.keys():
        while True:
            try:
                data = c.recv(40)
            except:
                data = False
            if data != False:
                data = str(data)
                if data[1] == "s":
                    idtimer[id] = 0
                    send(c,id)
                elif data[1] == "r":
                    idtimer[id] = 0
                    receive(c)

def registerin(data,c): #Register user to the system using DB
    if register(data[3], data[2]) == True:
        loggingin(data,c)
    else:
        print("Hibás regisztráció")

def loggingin(data,c):    #Get datas from DB(Is user existed?
    suc = login(data[3], data[2])
    if suc == True:
        count1 = 0
        while True:
            if count1 in connected.keys():
                count1 += 1
            else:
                log(data[1] + " sikeresen bejelentkezett")
                connected[count1] = data[1]
                idtimer[count1] = 0
                c.send(bytes(count1))
                logged(count1, data[1],c)

def log(s):  # logs
    with open("logs/" + datetime.datetime.now().strftime("%Y.%m.%d") + "-console-log.log",encoding="utf-8", mode="a") as f:
        f.write(s + "\n")

def kicker():
    while True:
        try:
            time.sleep(1)
            counter = 0
            while counter < idtimer[-1]:
                if counter in idtimer.keys():
                    idtimer[counter] += 1
                    if idtimer[counter] > 600:
                        del idtimer[counter]
                        del connected[counter]
                        log()
        except:
            time.sleep(1)

s = socket.socket()  # Create a socket object
host = "localhost"  # Get local machine name
port = 50000  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port
s.listen(5)  # Now wait for client connection.
print(createdb("Users"))
print(createtb("Users", "useraut"))
kick = threading.Thread(target=kicker, args=())
kick.start()
while True: #Create thread to new connection
    c, addr = s.accept()
    con = threading.Thread(target=newcon, args=(c,addr))
    con.start()
s.close()
