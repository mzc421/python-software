# -*- coding:utf-8 -*-
# author:木子川
# Data: 2022/7/9

import socket
import os
import sys
import struct


def sock_client_image():
    while True:
        try:
            host = "192.168.10.1"
            port = 6666
            tcpclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpclient.connect((host, port))
        except socket.error as msg:
            print(msg)
            print(sys.exit(1))

        filepath = input('input the file: ')  # 输入当前目录下的图片名
        fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'),
                            os.stat(filepath).st_size)  # 将图片以128sq的格式打包
        tcpclient.send(fhead)

        fp = open(filepath, 'rb')  # 打开要传输的图片
        while True:
            data = fp.read(1024)  # 读入图片数据
            if not data:
                print('{0} send over...'.format(filepath))
                break
            tcpclient.send(data)  # 以二进制格式发送图片数据
        tcpclient.close()
        # break    # 注释则循环发送


if __name__ == '__main__':
    sock_client_image()
