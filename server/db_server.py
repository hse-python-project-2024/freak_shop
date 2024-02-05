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
            return db_pb2.User(id=user[0], login=user[1], name=user[2])
        return db_pb2.User()

    def AddUser(self, request, context):
        return db_pb2.IsDone(is_done=self.db.add_user(_user_login=request.login, _user_name=request.name))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    db_pb2_grpc.add_DbServiceServicer_to_server(DBServer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
