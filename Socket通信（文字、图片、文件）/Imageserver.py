# -*- coding:utf-8 -*-
# author:木子川
# Data: 2022/7/9

import socket
import time
import struct


def socket_service_image():
    host = "192.168.10.1"
    port = 6666
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpserver.bind((host, port))
    tcpserver.listen(5)
    print("Wait for Connection.....................")

    while True:
        sock, addr = tcpserver.accept()  # addr是一个元组(ip,port)
        deal_image(sock, addr)


def deal_image(sock, addr):
    print("Accept connection from {0}".format(addr))  # 查看发送端的ip和端口
    print("-" * 5 + "开始接收" + "-" * 5)

    while True:
        fileinfo_size = struct.calcsize('128sq')
        buf = sock.recv(fileinfo_size)  # 接收图片名
        if buf:
            filename, filesize = struct.unpack('128sq', buf)
            fn = filename.decode().strip('\x00')
            recvd_size = 0

            now_time = time.strftime("%Y%m%d-%H%M%S")
            print(f"保存为：./{ now_time} {fn}")
            fp = open(r"./" + now_time + " " + fn, 'wb')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = sock.recv(1024)
                    recvd_size += len(data)
                else:
                    data = sock.recv(1024)
                    recvd_size = filesize
                fp.write(data)  # 写入图片数据
            fp.close()
        print("-"*5 + "接收完成" + "-"*5)
        sock.close()
        break


if __name__ == '__main__':
    socket_service_image()
