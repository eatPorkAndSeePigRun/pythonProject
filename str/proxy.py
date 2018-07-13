import time
from tcp_server import *


def main():
    s = new_tcp_server("127.0.0.1", 8888)
    while True:
        try:
            time.sleep(1)
            # print("main loop sleep")
        except KeyboardInterrupt as exp:
            break
    s.stop()


main()
