# -*- coding: utf-8 -*-

import socket
sk = socket.socket(type=socket.SOCK_DGRAM)# udp协议
sk.bind(('127.0.0.1',9090))
dic = {'alex':'\033[0;33;42m','太白':'\033[0;35;40m'}
while 1:
    msg_r,addr = sk.recvfrom(1024)# 接收来自哪里的消息
    msg_r = msg_r.decode('utf-8')# alex : 我要退学
    # 对于msg_r,通过':'分割,获取下标为0的,也就是name,再去掉name的左右两边的空格
    name = msg_r.split(':')[0].strip()

    color = dic.get(name,'')# 获取字典中 name所对应的 颜色值
    print('%s%s \033[0m'%(color,msg_r))
    if msg_r == 'q':# 如果当前客户端想要断开连接
        continue # 服务器端不应该继续通话了,应该等待接收另一个客户端的连接,返回到recvfrom
    msg_s = input('>>>')
    sk.sendto(msg_s.encode('utf-8'), addr)
    if msg_s == 'q':
        break
sk.close()