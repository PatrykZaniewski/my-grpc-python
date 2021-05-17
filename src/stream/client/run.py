import asyncio
import logging

import grpc
from sanic import Sanic
from sanic.response import json

from stream.grpcGen import calculate_stream_pb2_grpc
from stream.grpcGen.calculate_stream_pb2 import CalculateSomethingRequest
from stream.server.grpcImpl.calculate_service import CalculateService

app = Sanic("My Sanic app")
channel = grpc.aio.insecure_channel('localhost:50051')
grpc_server = grpc.aio.server()


@app.route('/post', methods=['POST'])
async def calculate(request):
    payload = request.json
    stub = calculate_stream_pb2_grpc.CalculateServiceStub(channel)
    responses = stub.CalculateSomething(create_messages(payload))
    pass

    # for response in responses:
    #     if response.WhichOneof("result") == 'valid_result':
    #         logging.info(f'Calculated result using rest: {response.valid_result.result}')
    #     else:
    #         logging.info(f'Calculation error using rest: {response.invalid_result.message}')


async def create_messages(payload):
    messages = []
    for request in payload.get('data'):
        messages.append(CalculateSomethingRequest(numbers=request.get('numbers'), divider=request.get('divider'),
                                  operation_type=request.get('operation_type')))
    print('abcd')
    logging.info("Started streaming messages")
    # for message in messages:
    #     print(f'Processing message, numbers = {message}')
    #     yield message



async def serve():
    calculate_stream_pb2_grpc.add_CalculateServiceServicer_to_server(CalculateService(), grpc_server)
    grpc_server.add_insecure_port('[::]:50052')
    await grpc_server.start()
    await grpc_server.wait_for_termination()


if __name__ == '__main__':
    server = app.create_server("0.0.0.0", port=8000, return_asyncio_server=True)
    loop = asyncio.get_event_loop()
    task_sanic = asyncio.ensure_future(server)
    task_grpc = asyncio.ensure_future(serve())
    loop.run_forever()
