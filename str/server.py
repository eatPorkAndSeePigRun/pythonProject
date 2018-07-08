import socket

# socket.AF_INET --> 机器网络之间的通信
# socket.SOCK_STREAM --> TCP协议通信
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 8080))  # 绑定到对应的ip和port
    s.listen(1)  # 启动socket 网络监听服务,一直监听client的网络请求
    conn, addr = s.accept()  # 调用accept()方法开始监听，等待客户端的连接
    with conn:
        print("***服务器即将启动，等待客户端的连接***")
        i = 1
        while True:
            data = conn.recv(1024)
            if data == bytes(str(i) + "\n", encoding="utf-8") and data != b'close':
                print("我是服务器端，客户端说：", end="")
                print(data)
                msg = bytes(str(i + 1) + "\n", encoding="utf-8")
                conn.send(msg)
                print("我回复：", end="")
                print(msg)
                i += 2
            else:
                conn.close()
                print("服务器端退出了")
                break
