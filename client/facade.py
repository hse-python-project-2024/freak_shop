import requests_pb2_grpc
import requests_pb2
import grpc

# from server.server_address_config import host, port


class ClientRequests:
    def __init__(self):
        channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = requests_pb2_grpc.DbServiceStub(channel)

    def get_user_by_id(self, _user_id: int):
        request = requests_pb2.Id(id=_user_id)
        response = self.stub.GetUserById(request)
        return response

    def add_user(self, _user_login: str, _user_name: str, _password1: str, _password2: str) -> bool:
        requests = requests_pb2.NewUser(login=_user_login, name=_user_name, password1=_password1, password2=_password2)
        return self.stub.AddUser(requests)
