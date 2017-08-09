

import logging
 
import thriftpy
from thriftpy.rpc import make_client
 
logging.basicConfig(level=logging.DEBUG)
 
pingpong_thrift = thriftpy.load("pingpong.thrift",
                                module_name="pingpong_thrift")
 
client = make_client(pingpong_thrift.PingPong, '127.0.0.1', 6000)
print(client.ping())
