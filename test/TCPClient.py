# -*- coding: utf-8 -*-

from socket import  socket
sk = socket()
sk.connect(('127.0.0.1',9090))

while 1:
    msg_s = input('>>>')
    sk.send(msg_s.encode('utf-8'))
    if msg_s == 'q':
        break
    msg_r = sk.recv(1024).decode('utf-8')
    print(msg_r)
    if msg_r == 'q':
        break

sk.close()