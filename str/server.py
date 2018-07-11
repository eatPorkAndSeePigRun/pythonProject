import socket
import struct
import threading
import time


def socket_recv_n(socket, n):
    data = b''
    length = 0
    while length < n:
        data += socket.recv(n-length)
        length = len(data)
    return data


class serverThread(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        pic = str(int(time.time())) + ".jpg"
        # 文件长度
        data = socket_recv_n(self.socket, 4)
        fileSize = struct.unpack("i", data)[0]
        print("我是服务器端，要接收" + pic + "的大小为：", fileSize)

        # 文件内容
        data = socket_recv_n(self.socket, fileSize)
        with open("server" + pic, "wb") as file:
            file.write(data)
        print(pic + "接收完成，总共接收的大小：", len(data))
        self.socket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 8080))  # 绑定到对应的ip和port
    s.listen(5)  # 启动socket 网络监听服务,一直监听client的网络请求
    print("***服务器即将启动，等待客户端的连接***")
    while True:
        conn, _ = s.accept()  # 调用accept()方法开始监听，等待客户端的连接
        thread = serverThread(conn)
        thread.start()
