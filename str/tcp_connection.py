import queue
import socket
import threading
from log import *


class TcpConnection:

    def __init__(self, owner, socket, on_disconnect, on_recv_data):
        self.owner = owner
        self.socket = socket
        self.socket.settimeout(1)
        self.on_disconnect = on_disconnect
        self.on_recv_data = on_recv_data
        self.recv_thread = None
        self.send_thread = None
        self.thread_lock = threading.Lock()
        self.send_queue = queue.Queue(10)
        self.is_open = True
        self.is_close = True
        log("TcpConnection __init__ %s %s" % (socket, self))

    def send_binary(self, binary):
        if binary == b'':
            return
        log("TcpConnection send_binary %s %s" % (binary, self))
        self.send_queue.put(binary)

    def open(self):
        if not self.is_close:
            return
        log("TcpConnection open %s" % self)
        self.is_close = False
        self.recv_thread = threading.Thread(target=self.recv_loop)
        self.send_thread = threading.Thread(target=self.send_loop)
        self.recv_thread.start()
        self.send_thread.start()

    def recv_loop(self):
        log("TcpConnection recv_loop %s" % self)
        while True:
            try:
                data = self.socket.recv(1024)
                if data == b'':
                    log("TcpConnection recv_loop exception:recv nothing mean socket close %s" % self)
                    self.close()
                    break
                self.on_recv_data(self, data)
            except socket.timeout:
                continue
            except socket.error as e:
                log("TcpConnection recv_loop exception %s %s" % (e, self))
                break
        log("TcpConnection recv_loop recv_thread exit %s" % self)

    def send_loop(self):
        log("TcpConnection send_loop %s" % self)
        while True:
            try:
                self.socket.send(b'')
                if not self.send_queue.empty():
                    data = self.send_queue.get()
                    self.send_n(data)
            except socket.error as e:
                log("TcpConnection send_loop exception %s %s" % (e, self))
                break
        log("TcpConnection send_loop send_thread exit %s" % self)

    def close(self):
        self.thread_lock.acquire()
        if not self.is_open:
            return
        log("TcpConnection close %s" % self)
        self.is_open = False
        self.socket.close()
        self.thread_lock.release()

    def send_n(self, data):
        if data == b'':
            return
        log("TcpConnection send_n %s %s" % (data, self))
        hasSize = 0
        dataSize = len(data)
        while not hasSize >= dataSize:
            try:
                hasSize += self.socket.send(data[hasSize:hasSize + 1024])
            except socket.timeout:
                continue
