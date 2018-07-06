import struct



def dumps(object):
    string = b''
    # 先从e_list开始
    for k, v in object.items():
        # 元素的值的类型
        if type(v) is str:
            string = string + b'\x02' + packEName(k) + struct.pack("i", len(v) + 1) \
                     + bytes(v,encoding='utf-8') + b'\x00'
        elif type(v) is int:
            string = string + b'\x10' + packEName(k) + struct.pack("i", v)
        elif type(v) is dict:
            string = string + b'\x03' + packEName(k) + dumps(v)
        elif type(v) is list:
            string = string + b'\x04'
            # 元素
            dictionary = {}
            for i in range(0, len(v)):
                dictionary[str(i)] = v[i]
            string = string + packEName(k) + dumps(dictionary)
    # 加上document的长度和结尾
    string = struct.pack("i", len(string) + 4 + 1) + string + b'\x00'
    return string


def packEName(k):
    # 元素的键
    eName = bytes(k, encoding='utf-8') + b'\x00'
    return eName


TYPES = {
    "str": 2,
    "int": 16,
    "dict": 3,
    "array": 4,
    "end": 0
}


def loads(string):
    object = {}
    start = 4
    end = len(string)
    while start < end:
        if string[start] == TYPES["str"]:
            start, k = unpackEName(string, start)
            # 元素的值
            v = b''
            i = 0
            while string[start + 4 + i] != TYPES["end"]:
                v = v + bytes((string[start + 4 + i],))
                i += 1
            # 放入object
            start = start + 4 + i + 1
            object[str(k, encoding="utf-8")] = str(v, encoding="utf-8")
        elif string[start] == TYPES["int"]:
            start, k = unpackEName(string, start)
            # 元素的值
            v = struct.unpack("i", string[start:start + 4])
            # 放入object
            start = start + 4
            object[str(k, encoding="utf-8")] = v[0]
        elif string[start] == TYPES["dict"]:
            start, k = unpackEName(string, start)
            # 元素的值
            dictLen = struct.unpack("i", string[start:start + 4])[0]
            v = loads(string[start:start + dictLen])
            # 放入object
            start = start + dictLen
            object[str(k, encoding="utf-8")] = v
        elif string[start] == TYPES["array"]:
            start, k = unpackEName(string, start)
            # 元素的值
            dictLen = struct.unpack("i", string[start:start + 4])[0]
            temp = loads(string[start:start + dictLen])
            v = []
            for _, t in temp.items():
                v.append(t)
            # 放入object
            start = start + dictLen
            object[str(k, encoding="utf-8")] = v
        elif string[start] == TYPES["end"]:
            return object


def unpackEName(string, start):
    # 元素的键
    k = b''
    i = 0
    while bytes((string[start + 1 + i],)) != b'\x00':
        k = k + bytes((string[start + 1 + i],))
        i += 1
    start = start + 1 + i + 1
    return start, k


object = {
    "type_of_string": "abchina",
    "type_of_number": 65535,
    "type_of_dict": {"a": 255, "b": 65535},
    "type_of_array": {"BSON": ["awesome", 1986]}
}

assert (loads(dumps(object)) == object)

