# -*- coding:utf-8 -*-
# @author: 木子川
# @Data:   2022/7/24
# @Email:  m21z50c71@163.com

import socket
import os

host = "192.168.10.1"
port = 6666
tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpserver.bind((host, port))
tcpserver.listen(5)
print("等待客户端连接...")

while True:
    tcpclient, addr = tcpserver.accept()
    print('client addr:', addr)
    while True:
        print("-" * 5 + "开始接收" + "-" * 5)
        fileNameData = tcpclient.recv(1024)  # 接收文件名字
        filename = fileNameData.decode('utf-8')
        new_filename = "new_" + filename
        print(f"文件保存为：{new_filename}")
        if os.path.exists(new_filename):
            os.remove(new_filename)
        new_file = open(new_filename, "wb")
        tcpclient.send("ok".encode("utf-8"))
        while True:
            rdata = tcpclient.recv(1024)  # 接收文件内容
            if not rdata:
                break
            new_file.write(rdata)
        new_file.close()
        print("-" * 5 + "接收完成" + "-" * 5)
        break
    tcpclient.close()
    # break  # 注释则可以循环接收
tcpserver.close()
