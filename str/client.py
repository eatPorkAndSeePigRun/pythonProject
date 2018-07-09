import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 8080))
    print("***客户端即将启动，正在连接服务器端***")
    for i in range(3):  # 发送3张图
        # 文件长度
        file = open(str(i + 1) + ".jpg", "rb")
        fileContent = file.read()
        file.close()
        fileSize = len(fileContent)
        print("我是客户端，要发送" + str(i + 1) + ".jpg的大小为：", end="")
        print(fileSize)
        s.send(bytes(str(fileSize), encoding="utf-8"))
        # 文件内容
        data = s.recv(1024)
        if data == b'start':
            print(str(i + 1) + ".jpg开始发送。")
            hasSize = 0
            while True:
                if hasSize + 1024 <= fileSize:
                    hasSize += s.send(fileContent[hasSize:hasSize + 1024])
                else:
                    hasSize += s.send(fileContent[hasSize:fileSize])
                    print(str(i + 1) + ".jpg发送完毕。")
                    print("总共发送的大小：", end="")
                    print(hasSize)
                    if s.recv(1024) == b'end':
                        break
    s.close()
