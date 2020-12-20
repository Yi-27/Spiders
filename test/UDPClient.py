# -*- coding: utf-8 -*-

import socket
sk = socket.socket(type=socket.SOCK_DGRAM)
name = input('请输入您的名字:>>>')
while 1:
    msg_s = input('>>>')
    msg_s = name + " : "+msg_s
    sk.sendto(msg_s.encode('utf-8'),('127.0.0.1',9090))# 发给谁一条消息
    if msg_s is 'q':
        break
    msg_r,addr = sk.recvfrom(1024)
    msg_r = msg_r.decode('utf-8')
    print(msg_r)
    if msg_r == 'q':
        break

sk.close()