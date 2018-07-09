import socket

# socket.AF_INET --> 机器网络之间的通信
# socket.SOCK_STREAM --> TCP协议通信
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 8080))  # 绑定到对应的ip和port
    s.listen(1)  # 启动socket 网络监听服务,一直监听client的网络请求
    conn, addr = s.accept()  # 调用accept()方法开始监听，等待客户端的连接
    with conn:
        print("***服务器即将启动，等待客户端的连接***")
        for i in range(3):  # 接收3张图
            # 文件长度
            data = conn.recv(1024)
            fileSize = int(str(data, encoding="utf-8"))
            print("我是服务器端，要接收" + str(i + 1) + ".jpg的大小为：", end="")
            print(fileSize)

            # 文件内容
            conn.send(b'start')
            print(str(i + 1) + ".jpg开始接收。")
            hasSize = 0
            file = open(str(i + 1) + "server.jpg", "wb")
            while True:
                if hasSize + 1024 <= fileSize:
                    data = conn.recv(1024)
                    file.write(data)
                    hasSize += len(data)
                else:
                    data = conn.recv(1024)
                    file.write(data)
                    file.close()
                    print(str(i + 1) + ".jpg接收完成。")
                    print("总共接收的大小：", end="")
                    print(hasSize + len(data))
                    conn.send(b'end')
                    break
    conn.close()
