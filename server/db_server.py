from concurrent import futures
import db_connection

import grpc
import db_pb2_grpc
import db_pb2


class DBServer(db_pb2_grpc.DbServiceServicer):
    def __init__(self):
        super().__init__()
        self.db = db_connection.DBConnection()

    def GetUserById(self, request, context):
        print("Already connected")
        user = self.db.get_user_by_id(_user_id=request.id)
        if user is not None:
            return db_pb2.User(login=user[0], name=user[1])
        return db_pb2.User(login="", name="")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    db_pb2_grpc.add_DbServiceServicer_to_server(DBServer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
