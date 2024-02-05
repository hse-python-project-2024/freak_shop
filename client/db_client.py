import db_pb2
import db_pb2_grpc
import grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = db_pb2_grpc.DbServiceStub(channel)
        while True:
            n = int(input("Enter user_id\n"))
            request = db_pb2.UserId(id=n)
            response = stub.GetUserById(request)
            print("Response:\n" + str(response))


if __name__ == '__main__':
    run()
