from concurrent import futures
import db_connection

import grpc
import requests_pb2_grpc
import requests_pb2

import server.model as md

from random import randint


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

