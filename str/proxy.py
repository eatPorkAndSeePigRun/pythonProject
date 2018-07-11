import socket
import threading
import queue
from util import *


class recvThread(threading.Thread):
    def __init__(self, socket, q):
        threading.Thread.__init__(self)
        self.socket = socket
        self.q = q

    def run(self):
        while True:
            if self.q.empty():
                threadLock.acquire()
                data = socket_recv_content(self.socket)
                self.q.put(data)
                threadLock.release()
                break
        print("exit recvThread")
        self.socket.close()


class sendThread(threading.Thread):
    def __init__(self, socket, q):
        threading.Thread.__init__(self)
        self.socket = socket
        self.q = q

    def run(self):
        while True:
            if not self.q.empty():
                threadLock.acquire()
                data = self.q.get()
                socket_send_content(self.socket, data)
                threadLock.release()
                break
        print("exit sendThread")
        self.socket.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 8888))  # 绑定到对应的ip和port
s.listen(5)  # 启动socket 网络监听服务,一直监听client的网络请求
print("***服务器即将启动，等待客户端的连接***")
threadLock = threading.Lock()
queueAtoB = queue.Queue(10)
queueBtoA = queue.Queue(10)
while True:
    connA, _ = s.accept()  # 调用accept()方法开始监听，等待客户端的连接
    rthreadA = recvThread(connA, queueAtoB)
    # sthreadA = sendThread(connA, queueBtoA)
    rthreadA.start()
    # sthreadA.start()
    connB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connB.connect(("127.0.0.1", 9999))
    # rthreadB = recvThread(connB, queueBtoA)
    sthreadB = sendThread(connB, queueAtoB)
    # rthreadB.start()
    sthreadB.start()
s.close()
