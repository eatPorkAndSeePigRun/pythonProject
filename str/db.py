import sys
import struct
from bson import *

if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage1; python db.py get key ")
        print("Usage2: python db.py set key value ")
        print("Usage3: python db.py del value ")
        exit(1)
    operate = sys.argv[1]
    if operate == "set":
        key = sys.argv[2]
        value = sys.argv[3]
        file = open("db.txt", "ab")
        dictionary = {key: value}
        file.write(dumps(dictionary))
        print(dictionary[key])
        file.close()
    elif operate == "del":
        value = sys.argv[2]
        file = open("db.txt", "rb")
        string = file.read()
        file.close()
        open("db.txt", "wb").close()
        start = 0
        end = len(string)
        itemLen = struct.unpack("i", string[start:start + 4])[0]
        file = open("db.txt", "ab")
        while start < end:
            temp = loads(string[start:start + itemLen])
            tk = list(temp.keys())[0]
            tv = list(temp.values())[0]
            # 找出相应的value,并修改为None
            if tv == value:
                tv = "None"
            file.write(dumps({tk: tv}))
            start += itemLen
            if start < end:
                itemLen = struct.unpack("i", string[start:start + 4])[0]
        file.close()

    elif operate == "get":
        key = sys.argv[2]
        file = open("db.txt", "rb")
        string = file.read()
        file.close()
        start = 0
        end = len(string)
        itemLen = struct.unpack("i", string[start:start + 4])[0]
        while start < end:
            dictionary = loads(string[start:start + itemLen])
            # 找出相应的key,并输出
            if key == list(dictionary.keys())[0]:
                print(dictionary[key])
                break
            else:
                start += itemLen
                if start < end:
                    itemLen = struct.unpack("i", string[start:start + 4])[0]
