from enum import Enum

from simple.grpcGen.calculate_pb2 import CalculateSomethingResponse, CalculateSomethingRequest
from simple.grpcGen.calculate_pb2_grpc import CalculateServiceServicer


class OperationType(Enum):
    ADD = 0
    MUL = 1


class CalculateService(CalculateServiceServicer):

    async def CalculateSomething(self, request: CalculateSomethingRequest, context):
        if request.divider == 0:
            return CalculateSomethingResponse(
                invalid_result=CalculateSomethingResponse.CalculateSomethingResponseInvalid(code=123,
                                                                                            message="Cannot divide by 0."))
        if request.operation_type == OperationType.MUL.value:
            result = 1
            for number in request.numbers:
                result *= number
        elif request.operation_type in [OperationType.ADD.value, OperationType.UNKNOWN.value]:
            result = 0
            for number in request.numbers:
                result += number

        return CalculateSomethingResponse(valid_result=CalculateSomethingResponse.CalculateSomethingResponseValid(
            result=int(result / request.divider), operation_type=request.operation_type))
