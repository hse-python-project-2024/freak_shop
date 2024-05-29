from concurrent import futures
from facade import Facade

from config import host, port
import grpc
import requests_pb2_grpc
from logs.loggers import get_logger


def serve():
    _LOGGER = get_logger(__name__)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    requests_pb2_grpc.add_DbServiceServicer_to_server(Facade(), server)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    _LOGGER.info(f'Сервер успешно поднят на хосте {host} с портом {port} и готов принимать запросы')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
