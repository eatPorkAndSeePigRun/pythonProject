import time


class log:
    def info(self, msg):
        file = open("log.txt", "a+")
        file.write(time.asctime() + msg)
        file.close()
