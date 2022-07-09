# -*- coding:utf-8 -*-
# author:木子川
# Data: 2022/7/9

import socket

host = "192.168.10.1"
port = 6666
tcpclient = socket.socket()
try:
    tcpclient.connect((host, port))
    print('服务器已连接')
except:
    print('服务器连接失败，请修改后重新运行!!')
    exit(0)

while True:
    print("-" * 5 + "开始发送" + "-" * 5)
    filename = "qq.txt"
    print(f"发送的文件为：{filename}")
    with open(filename, "r", encoding="utf-8") as f:
        rdata = f.read()
    tcpclient.send("qq.txt".encode("utf-8"))
    if tcpclient.recv(1024).decode("utf-8") == "ok":
        while True:
            tcpclient.send(rdata.encode('utf-8'))
            break
    print("-" * 5 + "发送完成" + "-" * 5)
    break

tcpclient.close()
