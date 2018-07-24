import time
from tcp_server import *


class ChatServer:
    def __init__(self):
        self.tcp_server = TcpServer("127.0.0.1", 8080, self.on_connect, self.on_disconnect, self.on_recv_data)
        self.rooms = {}
        self.clientSayInRoom = {}

    def on_connect(self, tcp_connection):
        pass

    def on_disconnect(self):
        pass

    def on_recv_data(self, tcp_connection, data):
        if str(data, encoding="utf-8") == "listroom":
            rooms = " ".join(self.rooms.keys())
            tcp_connection.send_binary(bytes(rooms, encoding="utf-8"))
            return
        try:
            command, content = str(data, encoding="utf-8").split()
            if command == "createroom":
                self.rooms[content] = []
            elif command == "deleteroom":
                del self.rooms[content]
            elif command == "joinroom":
                self.rooms[content].append(tcp_connection)
            elif command == "quitroom":
                self.rooms[content].remove(tcp_connection)
            elif command == "sayroom":
                self.clientSayInRoom[tcp_connection] = content
        except ValueError:
            for i in self.rooms[self.clientSayInRoom[tcp_connection]]:
                if i != tcp_connection and i is not str:
                    i.send_binary(data)
        except BaseException as error:
            print(error)

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
