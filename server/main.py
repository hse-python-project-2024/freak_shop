from concurrent import futures
from facade import Facade

from server_address_config import host, port
import grpc
import requests_pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    requests_pb2_grpc.add_DbServiceServicer_to_server(Facade(), server)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
