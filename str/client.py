import socket
import struct


def socket_send_n(socket, data):
    hasSize = 0
    dataSize = len(data)
    while not hasSize >= dataSize:
        hasSize += socket.send(data[hasSize:hasSize + 1024])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 8080))
    print("***客户端即将启动，正在连接服务器端***")
    for pic in ["1.jpg", "2.jpg", "3.jpg"]:  # 发送3张图
        # 文件长度
        with open(pic, "rb") as file:
            fileContent = file.read()
        fileSize = len(fileContent)
        print("我是客户端，要发送" + pic + "的大小为：", fileSize)
        socket_send_n(s, struct.pack("i", fileSize))

        # 文件内容
        socket_send_n(s, fileContent)
        print(pic + "发送完成。")
