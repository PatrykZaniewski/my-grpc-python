from enum import Enum

import grpc

from one.grpcGen import hello_pb2_grpc, hello_pb2, calculate_pb2_grpc
from one.grpcGen.calculate_pb2 import CalculateSomethingRequest

channel = grpc.insecure_channel('localhost:50051')


class OperationType(Enum):
    ADD = 1
    MUL = 2


def run_hello():
    stub = hello_pb2_grpc.HelloServiceStub(channel)
    response = stub.SayHello(hello_pb2.HelloRequest(name='ABC'))
    print("Received message: " + response.message)


def run_calculate():
    stub = calculate_pb2_grpc.CalculateServiceStub(channel)
    response = stub.CalculateSomething(CalculateSomethingRequest(numbers=[1, 2, 3], divider=2, operation_type=None))
    print("Greeter client received: ")


if __name__ == '__main__':
    # run_hello()
    run_calculate()
