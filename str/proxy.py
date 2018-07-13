import time
from tcp_server import *

class Proxy:
    def __init__(self, conn):
        self.conn = conn
        self.client = new_tcp_client("127.0.0.1", 9999, self.on_client_connect, self.on_client_disconnect, self.on_client_data)

    def on_client_connect(self, conn):
        print("on client connction")

    def on_client_disconnect(self, conn):
        print("on client on_client_disconnect")

    def on_client_data(self, conn, data):
        print("on client data")
        self.conn.send_binary(data)

all_proxy = []

def on_con(conn):
    print("on con")
    p = Proxy(conn)
    conn.proxy = p
    

def on_dis(conn):
    print("on disconn")
    all_proxy.remove(conn.proxy)


def on_data(conn, data):
    print("on data")
    conn.proxy.client.conn.send_binary(data)

    
def main():
    s = new_tcp_server("127.0.0.1", 8888, on_con , on_dis, on_data)
    while True:
        try:
            time.sleep(1)
            # print("main loop sleep")
        except KeyboardInterrupt as exp:
            break
    s.stop()


main()
