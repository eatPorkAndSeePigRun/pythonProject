import threading
from util import *
import queue

class TcpConnection:

    def __init__(self, socket, on_dis, on_data):
        self.socket = socket
        self.recv_thread = None
        self.send_thread = None
        self.send_queue = queue.Queue(10)
        
        self.stoped = False
        self.on_data = on_data
        self.on_dis = on_dis
        

    def send_binary(self, binary):
        # put binary to queue
        self.send_queue.put(binary)

    def start(self):
        self.recv_thread = threading.Thread(target=self.recv_loop)
        self.send_thread = threading.Thread(target=self.send_loop)
        self.recv_thread.start()
        self.send_thread.start()

    def recv_loop(self):
        while not self.stoped:
            try:
                print("recv beign", self.socket)
                data = self.socket.recv(1024)
                print("recv", self.socket, len(data))
                # data  == "' should stop here TODO
                if data == b'':
                    print("recv nothing mean socket close", self.socket)
                    break
                self.on_data(self, data)
            except BaseException as e:
                print(e)
                break

    def send_loop(self):
        while not self.stoped:
            try:
                data = self.send_queue.get()
                if data == b'':
                    continue
                print("send", self.socket, len(data))
                socket_send_n(self.socket, data)
            except BaseException as e:
                print(e)
                break

    def stop(self):
        if not self.stoped:
            return
        self.stoped = True
        # uninit all of this connection close all resource of this connection
