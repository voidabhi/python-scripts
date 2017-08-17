""""""""""""""
Service Proto

syntax = "proto3";

import "google/api/annotations.proto";

package helloworld;

// The greeting service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {
    option (google.api.http) = {
      post: "/v1/hello"
      body: "*"
    };
  }
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
"""""""""""""


""""""""""""""
Client
""""""""""""""

from __future__ import print_function

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:8000')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()


""""""""""""""
Server
""""""""""""""


from concurrent import futures
import time

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, {}'.format(request.name))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:8000')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
