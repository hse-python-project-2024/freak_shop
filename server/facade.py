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
        status = requests_pb2.Status()
        if not user[0]:
            status.is_done = False
            status.info = user[1]
            return requests_pb2.ResponseUser(status=status)
        status.is_done = True
        return requests_pb2.ResponseUser(status=status, id=user[1], login=user[2], name=user[3])

    def RegisterUser(self, request, context):
        result = self.db.add_user(_user_login=request.login, _user_name=request.name, _password_1=request.password1,
                                  _password_2=request.password1)
        return requests_pb2.Status(is_done=result[0], info=result[1])

    def LoginUser(self, request, context):
        user = self.db.login_user(_user_login=request.login, _password=request.password1)
        status = requests_pb2.Status(is_done=True, info="OK")
        if not user[0]:
            status.is_done, status.info = False, user[1]
            return requests_pb2.ResponseUser(status=status)
        return requests_pb2.ResponseUser(status=status, id=user[1], login=user[2], name=user[3])
