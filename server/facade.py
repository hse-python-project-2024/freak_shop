from concurrent import futures
import db_connection

import grpc
import requests_pb2_grpc
import requests_pb2


class Facade(requests_pb2_grpc.DbServiceServicer):
    def __init__(self):
        super().__init__()
        self.db = db_connection.DBConnection()

    def GetUserById(self, request, context):
        user = self.db.get_user_by_id(_user_id=request.id)
        if not user[0]:
            return requests_pb2.ResponseUser(status=False, info=user[1])
        return requests_pb2.ResponseUser(status=user[0], id=user[1], login=user[2], name=user[3])

    def AddUser(self, request, context):
        result = self.db.add_user(_user_login=request.login, _user_name=request.name, _password_1=request.password1, _password_2=request.password1)
        return requests_pb2.MessageInfo(status=result[0], info=result[1])


