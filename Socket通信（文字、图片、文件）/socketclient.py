import socket  # 导入socket
import base64
import os
import sys
import struct


def SingleSendText():
    """
    单次发送接收文字
    """
    host = "192.168.10.1"  # 设置IP
    port = 6666  # 设置端口号
    tcpclient = socket.socket()  # 创建TCP/IP套接字
    tcpclient.connect((host, port))  # 主动初始化TCP服务器连接
    print("已连接服务端")
    send_data = input("请输入要发送的内容：")
    tcpclient.send(send_data.encode())  # 发送TCP数据
    info = tcpclient.recv(1024).decode()
    print("接收到的内容：", info)
    tcpclient.close()


def CycleSendText():
    """
    循环发送接收文字
    """
    host = "192.168.10.1"  # 设置IP
    port = 6666  # 设置端口号
    tcpclient = socket.socket()  # 创建TCP/IP套接字
    tcpclient.connect((host, port))  # 主动初始化TCP服务器连接
    print("已连接服务端")
    while True:  # 判断是否退出
        send_data = input("请输入要发送的内容：")
        tcpclient.send(send_data.encode())  # 发送TCP数据
        if send_data == "byebye":
            break
        info = tcpclient.recv(1024).decode()
        if info == "byebye":
            break
        else:
            print("接收到的内容：", info)
    tcpclient.close()


def picture2base(path):
    """
    压缩图片数据
    """
    with open(path, 'rb') as img:
        b64encode = base64.b64encode(img.read())
        # 返回base64编码字符串
        return b64encode.decode('utf-8')


def SingleSendPicture():
    """
    单次发送图片
    """
    host = "192.168.10.1"  # 设置IP
    port = 6666  # 设置端口号
    tcpclient = socket.socket()  # 创建TCP/IP套接字
    tcpclient.connect((host, port))  # 主动初始化TCP服务器连接
    print("已连接服务端")
    imgPath = "test.jpg"
    sdata = picture2base(imgPath)
    print(f"开始发送图片 {imgPath}")
    tcpclient.send(sdata.encode())
    tcpclient.close()
    print("发送完成")


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


def SendFile():
    """发送文件"""
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


SingleSendText()  # 单次发送文字
# CycleSendText()  # 循环发送文字
# SingleSendPicture()  # 单次发送图片
# sock_client_image()   # 循环发送图片
# SendFile()  # 单次发送文件
