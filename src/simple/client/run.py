from enum import Enum

import grpc

from simple.grpcGen import hello_pb2_grpc, hello_pb2, calculate_pb2_grpc
from simple.grpcGen.calculate_pb2 import CalculateSomethingRequest

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
    if response.WhichOneof("result") == 'valid_result':
        print(f'Calculated result {response.valid_result.result}')
    else:
        print(f'Calculation error: {response.invalid_result.message}')


if __name__ == '__main__':
    # run_hello()
    run_calculate()
