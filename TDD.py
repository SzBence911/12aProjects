import socket

s = socket.socket()

sip = ('localhost', 50000)
s.connect(sip)

s.send(b';l;asd;asd;')