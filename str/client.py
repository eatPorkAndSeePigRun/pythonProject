import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 8080))
    print("***客户端即将启动，正在连接服务器端***")
    s.send(bytes("1\n", encoding="utf-8"))
    i = 2
    while True:
        data = s.recv(1024)
        if data == bytes(str(i) + "\n", encoding="utf-8") and data != b'8\n':
            print("我是客户端，服务器端说：", end="")
            print(data)
            msg = bytes(str(i + 1) + "\n", encoding="utf-8")
            s.send(msg)
            print("我回复：", end="")
            print(msg)
            i += 2
        else:
            s.send(b'close')
            s.close()
            print("客户端退出了。")
            break

