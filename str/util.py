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
