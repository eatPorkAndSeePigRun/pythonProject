import time


class log:
    def info(msg):
        with open("log.txt", "a+") as file:
            cont = str(time.asctime()) + " " + str(msg) + " "
            file.write(cont)
