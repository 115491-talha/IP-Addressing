from enum import Enum

class Class(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5

def get_class(octet: int) -> Class:
    if 0 <= octet <= 127:
        return Class.A
    elif 128 <= octet <= 191:
        return Class.B
    elif 192 <= octet <= 223:
        return Class.C
    elif 224 <= octet <= 239:
        return Class.D
    elif 240 <= octet <= 255:
        return Class.E
    else:
        raise ValueError("Invalid octet value")