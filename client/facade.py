import requests_pb2_grpc
import requests_pb2
import grpc

from config import host, port


class ClientRequests:
    def __init__(self):
        channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = requests_pb2_grpc.DbServiceStub(channel)

    def get_user_by_id(self, _user_id: int):
        request = requests_pb2.Id(id=_user_id)
        return self.stub.GetUserById(request)

    def register_user(self, _user_login: str, _user_name: str, _password1: str, _password2: str):
        requests = requests_pb2.NewUser(login=_user_login, name=_user_name, password1=_password1, password2=_password2)
        return self.stub.RegisterUser(requests)

    def login_user(self, _user_login: str, _password: str):
        requests = requests_pb2.NewUser(login=_user_login, password1=_password, password2=_password)
        return self.stub.LoginUser(requests)

