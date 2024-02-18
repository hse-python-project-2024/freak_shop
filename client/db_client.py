import db_pb2_grpc
import db_pb2
import grpc


class ClientDb:
    def __init__(self):
        channel = grpc.insecure_channel('localhost:50051')
        self.stub = db_pb2_grpc.DbServiceStub(channel)

    def get_user_by_id(self, _user_id: int):
        request = db_pb2.Id(id=_user_id)
        response = self.stub.GetUserById(request)
        return response

    def add_user(self, _user_login: str, _user_name: str) -> bool:
        requests = db_pb2.User(login=_user_login, name=_user_name)
        return self.stub.AddUser(requests)


if __name__ == '__main__':
    client = ClientDb()
    while True:
        n = int(input("Enter 1 to add user and 2 to ask user by id\n"))
        if n == 1:
            s1 = input("Enter user login:\n")
            s2 = input("Enter user name:\n")
            response = client.add_user(s1, s2)
            if response:
                print("User added")
            else:
                print("Error while adding user")
        else:
            _id = int(input("Enter user id:\n"))
            response = client.get_user_by_id(_id)
            print(response)