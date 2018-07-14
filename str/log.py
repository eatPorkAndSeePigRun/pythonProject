import time
import sys


name = str(sys.argv[0]) + "." + str(int(time.time())) + ".log"
file = open(name,"a+")
    
def log(msg):
    cont = str(time.asctime()) + " " + str(msg) + " \n"
    file.write(cont)
