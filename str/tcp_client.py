import socket
from log import *
from tcp_connection import *


class TcpClient:

    def __init__(self, ip, port, on_connect, on_disconnect, on_recv_data):
        self.ip = ip
        self.port = port
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.on_recv_data = on_recv_data
        self.is_open = True
        self.is_close = True
        log("TcpClient __init__ %s %s %s" % (ip, port, self))

    def backup(self):
        pass

    # def open_with_thread():
    #    start thread with self.open
    #    return

    def open(self):
        if not self.is_close:
            return
        log("TcpClient open %s" % self)
        self.is_close = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        self.connection = TcpConnection(self, self.socket, self.on_disconnect, self.on_recv_data)
        self.on_connect(self.connection)
        self.connection.open()

    def close(self):
        if not self.is_open:
            return
        log("TcpClient close %s" % self)
        self.is_open = False
        self.socket.close()
        self.connection.close()
