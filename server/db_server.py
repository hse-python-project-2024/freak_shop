from concurrent import futures
import time

import grpc
import db_pb2
import db_pb2_grpc


class DBServer(db_pb2_grpc.DbServiceServicer):
    def GetUserById(self, request, context):
        print("Already connected")
        reply = db_pb2.User(login="gab1k", name="Kamil")
        return reply


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    db_pb2_grpc.add_DbServiceServicer_to_server(DBServer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
