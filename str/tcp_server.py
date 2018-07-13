import socket
import threading
import queue
from tcp_connection import *
from tcp_client import *


class TcpServer:

    def __init__(self, ip, port, on_connect, on_disconnect, on_recv_data):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((ip, port))
        self.listen_socket.listen(5)
        self.tcp_conntions = []
        self.accept_thread = None
        self.stoped = False
        self.on_connect = on_connect
        self.on_dis = on_disconnect
        self.on_data  = on_recv_data

    def start(self):
        self.stoped = True
        # self.accept_thread = start thread with self.accept_loop
        self.accept_thread = threading.Thread(target=self.accept_loop)
        self.accept_thread.start()

    def stop(self):
        if not self.stoped:
            return
        self.stoped = False
        # quit self.accept_thread
        self.accept_thread.exit()
        # close self.listen_socket
        self.listen_socket.close()
        # close all tcp connction in self.tcp_conntions
        for i in self.tcp_conntions:
            i.close()

    def accept_loop(self):
        while True:
            try:
                # accept new connection from self.listen_socket.tcp_conntion = TcpConnection(...)
                conn, _ = self.listen_socket.accept()
                
                tcp_conn = TcpConnection(conn, self.on_dis, self.on_data)
                tcp_conn.start()
                self.on_connect(tcp_conn)

              
              
                self.tcp_conntions.append(tcp_conn)
            except socket.error as error:
                break

    
        


def new_tcp_server(ip, port, on_con, on_dis, on_data):
    s = TcpServer(ip, port, on_con, on_dis, on_data)
    s.start()
    return s
