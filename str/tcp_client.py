import socket
from tcp_connection import *


class TcpClient:

    def __init__(self, ip, port, send_queue, recv_queue):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        self.conn = TcpConnection(self.socket, send_queue, recv_queue)

    def start(self):
        self.conn.start()

    def stop(self):
        self.socket.close()
        self.conn.stop()


def new_tcp_client(ip, port, send_queue, recv_queue):
    c = TcpClient(ip, port, send_queue, recv_queue)
    return c
