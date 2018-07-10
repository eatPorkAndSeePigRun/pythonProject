import socket
import struct


def socket_recv_n(socket, n):
    data = b''
    while len(data) + 1024 <= n:
        data += socket.recv(1024)
    data += socket.recv(n - len(data))
    return data


# socket.AF_INET --> 机器网络之间的通信
# socket.SOCK_STREAM --> TCP协议通信
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 8080))  # 绑定到对应的ip和port
    s.listen(1)  # 启动socket 网络监听服务,一直监听client的网络请求
    conn, addr = s.accept()  # 调用accept()方法开始监听，等待客户端的连接
    with conn:
        print("***服务器即将启动，等待客户端的连接***")
        for pic in ["1.jpg", "2.jpg", "3.jpg"]:  # 接收3张图
            # 文件长度
            data = socket_recv_n(conn, 4)
            fileSize = struct.unpack("i", data)[0]
            print("我是服务器端，要接收" + pic + "的大小为：", fileSize)

            # 文件内容
            data = socket_recv_n(conn, fileSize)
            with open("server" + pic, "wb") as file:
                file.write(data)
            print(pic + "接收完成，总共接收的大小：", len(data))