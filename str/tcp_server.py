import socket
import threading
import queue
from tcp_connection import *
from tcp_client import *
from log import *


class TcpServer:

    def __init__(self, ip, port, on_connect, on_disconnect, on_recv_data):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((ip, port))
        self.listen_socket.listen(5)
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.on_recv_data = on_recv_data
        self.tcp_connections = []
        self.accept_thread = None
        self.is_open = True
        self.is_close = True
        log("TcpServer __init__ %s %s %s" % (ip, port, self))

    def open(self):
        if not self.is_close:
            return
        log("TcpServer open %s" % self)
        self.is_close = False
        self.accept_thread = threading.Thread(target=self.accept_loop)
        self.accept_thread.start()

    def close(self):
        if not self.is_open:
            return
        log("TcpServer close %s" % self)
        self.is_open = False
        self.accept_thread.exit()
        self.listen_socket.close()
        for i in self.tcp_connections:
            i.close()

    def accept_loop(self):
        log("TcpServer accept_loop %s" % self)
        while True:
            try:
                conn, _ = self.listen_socket.accept()
                tcp_connection = TcpConnection(self, conn, self.on_disconnect, self.on_recv_data)
                tcp_connection.open()
                self.on_connect(tcp_connection)
                self.tcp_connections.append(tcp_connection)
            except socket.error as error:
                break


def new_tcp_server(ip, port, on_connect, on_disconnect, on_data):
    s = TcpServer(ip, port, on_connect, on_disconnect, on_data)
    s.open()
    return s
