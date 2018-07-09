import sys
import struct
from bson import *

if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage1; python db.py get key ")
        print("Usage2: python db.py set key value ")
        print("Usage3: python db.py del key ")
        exit(1)
    operate = sys.argv[1]
    open("db.txt", "ab").close()
    if operate == "set":
        key = sys.argv[2]
        value = sys.argv[3]
        with open("db.txt", "rb+") as file:
            dictionary = loads(file.read())
            dictionary[key] = value
            file.seek(0, 0)
            file.write(dumps(dictionary))
        print("OK")
    elif operate == "del":
        key = sys.argv[2]
        with open("db.txt", "rb+") as file:
            dictionary = loads(file.read())
            try:
                del dictionary[key]
            except KeyError:
                print("false")
            else:
                print("true")
                file.seek(0, 0)
                file.write(dumps(dictionary))
    elif operate == "get":
        key = sys.argv[2]
        with open("db.txt", "rb") as file:
            dictionary = loads(file.read())
            try:
                print(dictionary[key])
            except KeyError:
                print("None")
