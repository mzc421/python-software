import socket  # 导入socket
import base64
import time
import sys
import struct
import os


def SingleReceiveText():
    """
    单次接收发送文字
    """
    host = "192.168.10.1"  # 设置IP
    port = 6666  # 设置端口号
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP/IP套接字
    tcpserver.bind((host, port))  # 绑定地址（host, port）到套接字
    tcpserver.listen(5)  # 设置最多连接数量
    print("等待客户端连接...")
    tcpclient, addr = tcpserver.accept()  # 被动接收TCP客户端连接
    print("客户端已经连接")
    info = tcpclient.recv(1024).decode()  # 接收客户端数据
    print("接收到的内容：", info)
    send_data = input("请输入要发送的内容：")
    tcpclient.send(send_data.encode())  # 发送TCP数据
    tcpclient.close()
    tcpserver.close()


def ReceiveTextCircularly():
    """
    循环接收发送文字
    """
    host = "192.168.10.1"  # 设置IP
    port = 6666  # 设置端口号
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP/IP套接字
    tcpserver.bind((host, port))  # 绑定地址（host, port）到套接字
    tcpserver.listen(5)  # 设置最多连接数量
    print("等待客户端连接...")
    tcpclient, addr = tcpserver.accept()  # 被动接收TCP客户端连接
    print("客户端已经连接")
    while True:  # 判断是否退出
        info = tcpclient.recv(1024).decode()  # 接收客户端数据
        if info == "byebye":
            break
        print("接收到的内容：", info)
        send_data = input("请输入要发送的内容：")
        tcpclient.send(send_data.encode())  # 发送TCP数据
        if send_data == "byebye":
            break
    tcpclient.close()
    tcpserver.close()


def base2picture(base64_img):
    """
    使用base64进行解码图片数据
    """
    now_time = time.strftime("%Y%m%d-%H%M%S")
    print(f"保存为：./{now_time}.jpg")
    b64decode = base64.b64decode(base64_img)
    file = open(r"./" + now_time + r".jpg", 'wb')
    file.write(b64decode)
    file.close()


def SingleReceivePicture():
    """
    单次接收图片
    """
    host = "192.168.10.1"
    port = 6666
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpserver.bind((host, port))
    tcpserver.listen(5)
    print("等待客户端连接...")
    tcpclient, addr = tcpserver.accept()
    print("开始接收")
    base64_data = ""
    while True:
        rdata = tcpclient.recv(1024)
        base64_data += str(rdata, 'utf-8')
        if not rdata:
            break
    base2picture(base64_data)
    tcpclient.close()
    tcpserver.close()
    print("接收完成")


def ReceivePicturesCircularly():
    """
    循环接收图片
    """
    host = "192.168.10.1"
    port = 6666
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpserver.bind((host, port))
    tcpserver.listen(5)
    print("等待客户端连接...")

    while True:
        tcpclient, addr = tcpserver.accept()
        print("-" * 5 + "开始接收" + "-" * 5)
        base64_data = ""
        while True:
            rdata = tcpclient.recv(1024)
            base64_data += str(rdata, 'utf-8')
            if not rdata:
                break
        base2picture(base64_data)
        tcpclient.close()
        print("-" * 5 + "接收完成" + "-" * 5)

    tcpserver.close()


def socket_service_image():
    try:
        host = "192.168.10.1"
        port = 6666
        tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpserver.bind((host, port))
        tcpserver.listen(5)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("Wait for Connection.....................")

    while True:
        sock, addr = tcpserver.accept()  # addr是一个元组(ip,port)
        deal_image(sock, addr)


def deal_image(sock, addr):
    print("Accept connection from {0}".format(addr))  # 查看发送端的ip和端口

    while True:
        print("-"*5 + "开始接收" + "-"*5)
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


def ReceivingFile():
    """
    接收文件
    """
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
            new_file = open(new_filename, "a", encoding="utf-8")
            tcpclient.send("ok".encode("utf-8"))
            while True:
                rdata = tcpclient.recv(1024)  # 接收文件内容
                if not rdata:
                    break
                new_file.write(rdata.decode("utf-8"))
            new_file.close()
            print("-" * 5 + "接收完成" + "-" * 5)
            break
        tcpclient.close()
        break  # 注释则可以循环接收
    tcpserver.close()


SingleReceiveText()  # 单次接收文字   与 SingleSendText() 配合使用
# ReceiveTextCircularly()  # 循环接收文字   与 CycleSendText() 配合使用
# SingleReceivePicture()  # 单次接收图片   与 SingleSendPicture() 配合使用
# ReceivePicturesCircularly()  # 循环接收图片  与 SingleSendPicture() 配合使用
# socket_service_image()  # 可以单次/循环接收图片  与 sock_client_image() 配合使用
# ReceivingFile()  # 可以单次/循环接收文件  与 SendFile() 配合使用
