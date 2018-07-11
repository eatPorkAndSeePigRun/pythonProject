from bson import *


def socket_recv_n(socket, n):
    data = b''
    length = 0
    while length < n:
        data += socket.recv(n - length)
        length = len(data)
    return data


def socket_send_n(socket, data):
    hasSize = 0
    dataSize = len(data)
    while not hasSize >= dataSize:
        hasSize += socket.send(data[hasSize:hasSize + 1024])


def socket_recv_content(socket):
    # 内容大小
    data = socket_recv_n(socket, 4)
    contSize = struct.unpack("i", data)[0]
    # 真正内容
    data = socket_recv_n(socket, contSize)
    msg = loads(data)["cont"]
    return msg


def socket_send_content(socket, msg):
    cont = dumps({"cont": msg})
    # 内容长度
    contSize = len(cont)
    socket_send_n(socket, struct.pack("i", contSize))
    # 内容
    socket_send_n(socket, cont)

