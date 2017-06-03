from msgpack import packb
from msgpack import unpackb
from time import time
 
def pack(msg):
    return packb(msg, use_bin_type=True)
 
def unpack(msg):
    return unpackb(msg, use_list=False, encoding='utf-8')
 
# Testing lists:
mylist = [1, 2, 3, 5, "something", 'c', False]
print(mylist)
msg = pack(mylist)
print(msg)
result = unpack(msg)
print(result)
 
# Testing dictionaries
mydict = {
    "id": 1,
    "time": time(),
    "stuff": "Hello, world!"
}
print(mydict)
msg = pack(mydict)
print(msg)
result = unpack(msg)
print(result)
