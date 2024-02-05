import db_pb2
import db_pb2_grpc
import time
import grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = db_pb2_grpc.DbServiceStub(channel)
        while True:
            n = int(input("Enter 1\n"))
            if n == 1:
                request = db_pb2.UserId(id=1)
                response = stub.GetUserById(request)
                print("Response -", response)


if __name__ == '__main__':
    run()
