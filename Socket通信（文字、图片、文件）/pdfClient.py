# -*- coding:utf-8 -*-
# @author: 木子川
# @Data:   2022/7/24
# @Email:  m21z50c71@163.com

import socket

host = "192.168.10.1"
port = 6666
tcpclient = socket.socket()
try:
    tcpclient.connect((host, port))
    print('服务器已连接')
except:
    print('服务器连接失败，请先打开服务器!!!')
    exit(0)

while True:
    print("-" * 5 + "开始发送" + "-" * 5)
    filename = "测试文件.pdf"
    print(f"发送的文件为：{filename}")
    with open(filename, "rb") as f:
        rdata = f.read()
    tcpclient.send(filename.encode("utf-8"))
    if tcpclient.recv(1024).decode("utf-8") == "ok":
        while True:
            tcpclient.send(rdata)
            break
    print("-" * 5 + "发送完成" + "-" * 5)
    break

tcpclient.close()
