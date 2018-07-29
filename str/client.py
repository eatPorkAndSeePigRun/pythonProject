import socket

s = socket.socket()
s.connect(("127.0.0.1", 8080))
while True:
    msg = bytes(input("发送："), encoding="utf-8")
    s.send(msg)
    data = s.recv(1024)
    print('收到：', str(data, encoding="utf-8"))