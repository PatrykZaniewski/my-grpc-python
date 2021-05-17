from simple.grpcGen.hello_pb2 import HelloReply
from simple.grpcGen.hello_pb2_grpc import HelloServiceServicer


class HelloService(HelloServiceServicer):

    def SayHello(self, request, context):
        return HelloReply(message=f'Hello {request.name}')
