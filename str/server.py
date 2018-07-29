import socket
import select
import queue

server = socket.socket()
server.setblocking(False)
server.bind(("127.0.0.1", 8080))
server.listen()
rlist = [server]
wlist = []
msg_queues = {}
while True:
    readable, writable, exceptional = select.select(rlist, wlist, rlist)
    for s in readable:
        if s is server:
            conn, _ = s.accept()
            conn.setblocking(False)
            rlist.append(conn)
            msg_queues[conn] = queue.Queue()
        else:
            try:
                data = s.recv(1024)
            except ConnectionResetError:
                rlist.remove(s)
                if s in wlist:
                    wlist.remove(s)
                s.close()
                del msg_queues[s]
            else:
                if data:
                    msg_queues[s].put(data)
                    if s not in wlist:
                        wlist.append(s)
    for s in writable:
        try:
            next_msg = msg_queues[s].get_nowait()
        except queue.Empty:
            wlist.remove(s)
        else:
            s.send(next_msg)
    for s in exceptional:
        rlist.remove(s)
        if s in wlist:
            wlist.remove(s)
        s.close()
        del msg_queues[s]