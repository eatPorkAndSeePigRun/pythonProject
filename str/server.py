import time
from tcp_server import *


class ChatServer:
    def __init__(self):
        self.tcp_server = TcpServer("127.0.0.1", 8080, self.on_connect, self.on_disconnect, self.on_recv_data)

    def on_connect(self, tcp_connection):
        pass

    def on_disconnect(self):
        pass

    def on_recv_data(self, tcp_connection, data):
        for i in self.tcp_server.tcp_connections:
            if i != tcp_connection:
                i.send_binary(data)

    def open(self):
        self.tcp_server.open()

    def close(self):
        self.tcp_server.close()


def main():
    chatServer = ChatServer()
    print("***服务器即将启动，等待客户端的连接***")
    chatServer.open()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt as e:
            break
    chatServer.close()


main()
log("server main thread exit")
