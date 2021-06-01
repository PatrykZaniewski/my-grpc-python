import asyncio
import logging

import grpc

from stream.grpcGen import calculate_stream_pb2_grpc
from stream.server.grpcImpl.calculate_service import CalculateService


async def serve():
    grpc_server = grpc.aio.server()
    calculate_stream_pb2_grpc.add_CalculateServiceServicer_to_server(CalculateService(), grpc_server)
    grpc_server.add_insecure_port('[::]:50051')
    await grpc_server.start()
    await grpc_server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    asyncio.run(serve())
