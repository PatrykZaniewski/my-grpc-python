import logging
from enum import Enum

from simple.grpcGen.calculate_pb2 import CalculateSomethingResponse
from simple.grpcGen.calculate_pb2_grpc import CalculateServiceServicer


class OperationType(Enum):
    ADD = 0
    MUL = 1


class CalculateService(CalculateServiceServicer):

    async def CalculateSomething(self, request_iterator, context):
        for request in request_iterator:
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
