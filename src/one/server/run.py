import asyncio
from concurrent import futures

from sanic import Sanic
from sanic.response import json
import grpc

from one.grpcGen import calculate_pb2_grpc, hello_pb2_grpc
from one.grpcGen.calculate_pb2_grpc import CalculateService
from one.server.grpcImpl.hello_service import HelloService

app = Sanic("My Hello, world app")
grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
server = app.create_server("0.0.0.0", port=8000, return_asyncio_server=True)

@app.get('/')
async def test(request):
    return json({'hello': 'world'})


async def serve():
    hello_pb2_grpc.add_HelloServiceServicer_to_server(HelloService(), grpc_server)
    calculate_pb2_grpc.add_CalculateServiceServicer_to_server(CalculateService(), grpc_server)
    grpc_server.add_insecure_port('[::]:50051')
    grpc_server.start()
    # grpc_server.wait_for_termination()


if __name__ == '__main__':
    # app.run()

    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(server)
    task2 = asyncio.ensure_future(serve())
    loop.run_forever()
    # serve()
    # app.run()
