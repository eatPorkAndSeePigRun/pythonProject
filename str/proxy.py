import time
from tcp_server import *

class Proxy:
    def __init__(self, conn):
        self.conn = conn
        self.client = new_tcp_client("127.0.0.1", 9999, self.on_client_connect, self.on_client_disconnect, self.on_client_data)

    def on_client_connect(self, conn):
        print("Proxy的on_client_connction()函数被调用")

    def on_client_disconnect(self, conn):
        print("Proxy的on_client_disconnect()函数被调用")

    def on_client_data(self, conn, data):
        print("Proxy的on_client_data()函数被调用")
        self.conn.send_binary(data)

all_proxy = []

def on_con(conn):
    print("on_con()函数被调用")
    p = Proxy(conn)
    conn.proxy = p
    

def on_dis(conn):
    print("on_dis函数被调用")
    all_proxy.remove(conn.proxy)


def on_data(conn, data):
    print("on_data函数被调用")
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
