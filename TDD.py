import socket
import time

s = socket.socket()

sip = ('localhost', 50000)
s.connect(sip)



def  reg():
    s.send(b';r;asd;asd;')

def login():
    s.send(b';l;asd;asd;')
    sendmes(b";Sikeres teszt;")

def sendmes(msg):
    time.sleep(1)
    s.send(b';s;ms')
    log = receive()
    print(log)
    if log == True:
        s.send(msg)

def receive():
    dat = "b''"
    while str(dat) == "b''":
        dat = s.recv(1)
        dat = dat.decode('utf8')
        print(dat)
        try:
            if dat == "c":
                return True
            else:
                return False
        except:
                if "\x00" in dat:
                    return True

login()
