import struct
import socket


class redis:
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def set(self, key, value):
        command = "set " + key + " " + value
        print(self.execute_command(command))

    def get(self, key):
        command = "get " + key
        data = self.execute_command(command)
        print(data)
        return data

    def delete(self, key):
        command = "del " + key
        print(self.execute_command(command))

    def encode(self, command):
        temp = command.split()
        commands = []
        for i in temp:
            commands.append("$%s\r\n%s\r\n" % (len(i), i))
        s = "*%s\r\n%s" % (len(temp), "".join(commands))
        return s

    def decode(self, string):
        if string[0] == "+":
            return string[1: len(string) - 2]
        elif string[0] == "-":
            pass
        elif string[0] == ":":
            return int(string[1: len(string) - 2])
        elif string[0] == "$":
            return string[4: len(string) - 2]
        elif string[0] == "*":
            pass

    def execute_command(self, command):
        s = self.encode(command)
        self.send_n(bytes(s, encoding="utf-8"))
        data = str(self.socket.recv(1024), encoding="utf-8")
        return self.decode(data)

    def send_n(self, data):
        if data == b'':
            return
        hasSize = 0
        dataSize = len(data)
        while not hasSize >= dataSize:
            try:
                hasSize += self.socket.send(data[hasSize:hasSize + 1024])
            except socket.timeout:
                continue


def main():
    key = "foo"
    value = "bar"
    c = redis("127.0.0.1", 6379)
    c.set(key, value)
    assert (c.get(key) == value)
    c.delete(key)


main()
