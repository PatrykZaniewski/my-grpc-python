from one.grpcGen.calculate_pb2 import CalculateSomethingResponse
from one.grpcGen.calculate_pb2_grpc import CalculateServiceServicer


class CalculateService(CalculateServiceServicer):

    def CalculateSomething(self, request, context):
        return CalculateSomethingResponse(result=15, operationType='ADD')
