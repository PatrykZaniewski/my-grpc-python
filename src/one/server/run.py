from concurrent import futures

import grpc

from one.grpcGen import calculate_pb2_grpc, hello_pb2_grpc
from one.server.grpcImpl.calculate_service import CalculateService
from one.server.grpcImpl.hello_service import HelloService


def serve():
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServiceServicer_to_server(HelloService(), grpc_server)
    calculate_pb2_grpc.add_CalculateServiceServicer_to_server(CalculateService(), grpc_server)
    grpc_server.add_insecure_port('[::]:50051')
    grpc_server.start()
    grpc_server.wait_for_termination()


if __name__ == '__main__':
    serve()
