import logging
import time
from enum import Enum

from simple.grpcGen.calculate_pb2 import CalculateSomethingResponse
from simple.grpcGen.calculate_pb2_grpc import CalculateServiceServicer


class OperationType(Enum):
    ADD = 0
    MUL = 1


async def print_message_sent(numbers):
    logging.info(f"Message sent, numbers = {numbers}")


class CalculateService(CalculateServiceServicer):

    async def CalculateSomething(self, request_iterator, context):
        try:
            request = next(request_iterator)
            logging.info("Received a phone call request for number [%s]",
                         request.phone_number)
        except StopIteration:
            raise RuntimeError("Failed to receive call request")
        logging.info(f'Received numbers = {request.numbers}')
        time.sleep(1)
        context.add_callback(lambda: print_message_sent(request.numbers))
        logging.info(f'Started processing numbers = {request.numbers}')
        if request.divider == 0:
            yield CalculateSomethingResponse(
                invalid_result=CalculateSomethingResponse.CalculateSomethingResponseInvalid(code=123,
                                                                                            message="Cannot divide by 0."))
        if request.operation_type == OperationType.MUL.value:
            result = 1
            for number in request.numbers:
                result *= number
        elif request.operation_type == OperationType.ADD.value:
            result = 0
            for number in request.numbers:
                result += number
        logging.info(f'Streaming processed numbers = {request.numbers}')
        yield CalculateSomethingResponse(valid_result=CalculateSomethingResponse.CalculateSomethingResponseValid(
            result=int(result / request.divider), operation_type=request.operation_type))
        time.sleep(2)
        logging.info(f'Numbers sent 2 seconds ago, numbers = {request.numbers}')
