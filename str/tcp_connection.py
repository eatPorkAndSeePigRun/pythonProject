import threading
from util import *


class TcpConnection:

    def __init__(self, socket, send_queue, recv_queue):
        self.socket = socket
        self.recv_thread = None
        self.send_thread = None
        self.send_queue = send_queue
        self.recv_queue = recv_queue
        self.stoped = False

    def send_binary(self, binary):
        # put binary to queue
        self.recv_queue.put(binary)

    def start(self):
        self.stoped = True
        # self.xxx_thread = start thread with self.xxx_loop
        self.recv_thread = threading.Thread(target = self.recv_loop)
        self.send_thread = threading.Thread(target = self.send_loop)
        self.recv_thread.start()
        self.send_thread.start()

    def recv_loop(self):
        while self.stoped:
            try:
                data = self.socket.recv(1024)
                self.send_binary(data)
            except BaseException as e:
                print(e)
                break

    def send_loop(self):
        while self.stoped:
            try:
                data = self.recv_queue.get()
                socket_send_n(self.socket, data)
            except BaseException as e:
                print(e)
                break

    def stop(self):
        if self.stoped:
            return
        self.stoped = False
        # uninit all of this connection close all resource of this connection
