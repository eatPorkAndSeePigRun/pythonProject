import socket
import threading
import queue
from tcp_connection import *
from tcp_client import *


class TcpServer:

    def __init__(self, ip, port):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((ip, port))
        self.listen_socket.listen(5)
        self.tcp_conntions = []
        self.accept_thread = None
        self.stoped = False

    def start(self):
        self.stoped = True
        # self.accept_thread = start thread with self.accept_loop
        self.accept_thread = threading.Thread(target=self.accept_loop)
        self.accept_thread.start()

    def stop(self):
        if self.stoped:
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
                print("start")
                conn, _ = self.listen_socket.accept()
                bsworkQueue = queue.Queue(10)
                brworkQueue = queue.Queue(10)
                tcp_conn = TcpConnection(conn, brworkQueue, bsworkQueue)
                tcp_conn.start()
                c = new_tcp_client("127.0.0.1", 9999, bsworkQueue, brworkQueue)
                # self.tcp_connection.append(tcp_connection)
                self.tcp_conntions.append(tcp_conn)
            except socket.error as error:
                break


def new_tcp_server(ip, port):
    s = TcpServer(ip, port)
    s.start()
    return s
