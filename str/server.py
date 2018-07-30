import socket
import select


class RedisServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket()
        self.db = {}
        self.rlist = [self.socket]
        self.wlist = []
        self.msg = {}

    def encode(self, command):
        if type(command) is int:
            return ":%s\r\n" % command
        elif type(command) is str:
            return "+%s\r\n" % command

    def execute(self, string):
        try:
            strings = string.split('\r\n')
            number = int(strings[0][1])
            if number == 2:
                method, key = strings[2].lower(), strings[4]
                if method == "get":
                    if key in self.db:
                        return self.encode(self.db[key])
                    else:
                        return self.encode("None")
                elif method == "del":
                    if key in self.db:
                        del self.db[key]
                        return self.encode(1)
                    else:
                        return self.encode(0)
            elif number == 3:
                method, key, value = strings[2].lower(), strings[4], strings[6]
                if method == "set":
                    self.db[key] = value
                    return self.encode("OK")
            else:
                return "-Error message\r\n"
        except BaseException:
            return "-Error message\r\n"

    def run(self):
        self.socket.setblocking(False)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        while True:
            readable, writable, exceptional = select.select(self.rlist, self.wlist, self.rlist)
            for s in readable:
                if s is self.socket:
                    conn, _ = s.accept()
                    conn.setblocking(False)
                    self.rlist.append(conn)
                    self.msg[conn] = []
                else:
                    try:
                        data = s.recv(1024)
                    except ConnectionResetError:
                        self.rlist.remove(s)
                        if s in self.wlist:
                            self.wlist.remove(s)
                        s.close()
                        del self.msg[s]
                    else:
                        if data:
                            temp = self.execute(str(data, encoding="utf-8"))
                            self.msg[s].append(bytes(temp, encoding="utf-8"))
                            if s not in self.wlist:
                                self.wlist.append(s)
            for s in writable:
                if s not in self.msg:
                    break
                try:
                    msg = self.msg[s].pop()
                    s.send(msg)
                except IndexError:
                    self.wlist.remove(s)
                except ConnectionResetError:
                    self.wlist.remove(s)
            for s in exceptional:
                self.rlist.remove(s)
                if s in self.wlist:
                    self.wlist.remove(s)
                s.close()
                del self.msg[s]


def main():
    redisServer = RedisServer("127.0.0.1", 8080)
    try:
        redisServer.run()
    except KeyboardInterrupt:
        return


main()
