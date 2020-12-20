# -*- coding: utf-8 -*-

import socket
sk = socket.socket(type=socket.SOCK_STREAM)  # socket.SOCK_STREAM = 1,
sk.bind(('127.0.0.1',9090))
sk.listen()

while 1:
    # print(123)
    conn,addr = sk.accept() #  等待连接 -- 阻塞
    # print(456)
    while 1:
        # print(789)
        msg_r = conn.recv(1024).decode('utf-8') # 阻塞等待接收客户端发来的消息
        # print('jqk')
        print('接收到来自%s的一个消息:%s' % (addr, msg_r))
        if msg_r == 'q':
            break
        msg_s = input('>>>')
        conn.send(msg_s.encode('utf-8'))# 发送给客户端消息
        if msg_s == 'q':
            break
    conn.close()# 服务器和当前客户端断开连接,程序回到上一层死循环,重新等待客户端的连接
sk.close()