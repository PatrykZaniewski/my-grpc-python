import asyncio

import grpc

from async_with_rest.grpcGen import calculate_pb2_grpc
from async_with_rest.server.grpcImpl.calculate_service import CalculateService


async def serve():
    grpc_server = grpc.aio.server()
    calculate_pb2_grpc.add_CalculateServiceServicer_to_server(CalculateService(), grpc_server)
    grpc_server.add_insecure_port('[::]:50051')
    await grpc_server.start()
    await grpc_server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
