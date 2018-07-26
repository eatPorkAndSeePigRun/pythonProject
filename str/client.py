import time
import socket
import threading
from log import *


class ChatClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.opened = False
        log("ChatClient __init__")

    def open(self):
        self.opened = True
        log("ChatClient open")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        self.recv_content_thread = threading.Thread(target=self.recv_content_loop)
        self.recv_content_thread.start()
        self.send_content_loop()

    def close(self):
        if not self.opened:
            return
        log("ChatClient close")
        self.opened = False
        self.socket.close()

    def recv_content_loop(self):
        log("ChatClient recv_loop start")
        while self.opened:
            try:
                msg = str(self.socket.recv(1024), encoding="utf-8")
                print("\n<<<", msg)
                print(">>>")
            except socket.error as e:
                log("ChatClient recv_content_loop exception %s %s" % (e, self))
                break
        log("ChatClient recv_loop end")

    def send_content_loop(self):
        log("ChatClient send_loop start")
        while self.opened:
            try:
                content = input(">>>")
                self.send_n(bytes(content, encoding="utf-8") + b'\x00')
            except KeyboardInterrupt as e:
                break
        log("ChatClient send_loop end")

    def send_n(self, data):
        if data == b'':
            return
        log("ChatClient send_n %s %s" % (data, self))
        hasSize = 0
        dataSize = len(data)
        while not hasSize >= dataSize:
            try:
                hasSize += self.socket.send(data[hasSize:hasSize + 1])
                time.sleep(1)
            except socket.timeout:
                continue


def main():
    chatClient = ChatClient("127.0.0.1", 8080)
    print("***客户端即将启动，正在连接服务器端***")
    chatClient.open()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt as e:
            break
    chatClient.close()


main()
log("client main thread exit")
