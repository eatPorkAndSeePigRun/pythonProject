import socket
from tcp_connection import *


class TcpClient:

    def __init__(self, ip, port, on_con, on_dis, on_data):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        self.conn = TcpConnection(self.socket, on_dis, on_data)
        on_con(self.conn)
        
    def start(self):
        self.conn.start()

    def stop(self):
        self.socket.close()
        self.conn.stop()



def new_tcp_client(ip, port, on_con, on_dis, on_data):
    c = TcpClient(ip, port, on_con, on_dis, on_data)
    c.start()
    return c
