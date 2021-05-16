import grpc

from one.grpcGen import hello_pb2_grpc, hello_pb2


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hello_pb2_grpc.HelloServiceStub(channel)
        response = stub.SayHello(hello_pb2.HelloRequest(name='ABC'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()
