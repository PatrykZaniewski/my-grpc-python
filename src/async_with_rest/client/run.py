import asyncio
from concurrent import futures
from sanic.response import json

from sanic import Sanic
import grpc

from async_with_rest.grpcGen import calculate_pb2_grpc
from async_with_rest.grpcGen.calculate_pb2 import CalculateSomethingRequest
from async_with_rest.server.grpcImpl.calculate_service import CalculateService

app = Sanic("My Sanic app")
channel = grpc.aio.insecure_channel('localhost:50051')
grpc_server = grpc.aio.server()


@app.route('/post', methods=['POST'])
async def calculate(request):
    payload = request.json
    stub = calculate_pb2_grpc.CalculateServiceStub(channel)
    response = await stub.CalculateSomething(
            CalculateSomethingRequest(numbers=payload.get('numbers'), divider=payload.get('divider'),
                                    operation_type=payload.get('operation_type')))
    if response.WhichOneof("result") == 'valid_result':
        return json(f'Calculated result using rest: {response.valid_result.result}')
    else:
        return json(f'Calculation error using rest: {response.invalid_result.message}')


async def serve():
    calculate_pb2_grpc.add_CalculateServiceServicer_to_server(CalculateService(), grpc_server)
    grpc_server.add_insecure_port('[::]:50052')
    await grpc_server.start()
    await grpc_server.wait_for_termination()


if __name__ == '__main__':
    server = app.create_server("0.0.0.0", port=8000, return_asyncio_server=True)
    loop = asyncio.get_event_loop()
    task_sanic = asyncio.ensure_future(server)
    task_grpc = asyncio.ensure_future(serve())
    loop.run_forever()
