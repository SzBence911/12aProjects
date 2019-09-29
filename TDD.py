import socket
import time

s = socket.socket()

sip = ('localhost', 50000)
s.connect(sip)



def  reg():
    s.send(b';r;asd;asd;')

def login():
    s.send(b';l;asd;asd;')
    sendmes(b";asdasdasdasd;")

def sendmes(msg):
    time.sleep(1)
    s.send(b';s;ms')
    if receive() == True:
        s.send(msg)

def receive():
    dat = "b''"
    while str(dat) == "b''":
        dat = s.recv(32)
        dat = str(dat)
        dat = dat.split(';')
        print(dat)
        if dat[1] == "c":
            return True
        else:
            return False

login()