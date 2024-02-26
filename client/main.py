from facade import ClientRequests

if __name__ == '__main__':
    client = ClientRequests()
    while True:
        n = int(input("Enter 1 to add user and 2 to ask user by id\n"))
        if n == 1:
            s1 = input("Enter user login:\n")
            s2 = input("Enter user name:\n")
            s3 = input("Enter password\n")
            s4 = input("Confirm password:\n")
            response = client.add_user(s1, s2, s3, s4)
            print(response)
        else:
            _id = int(input("Enter user id:\n"))
            response = client.get_user_by_id(_id)
            print(response)
            print("Статус - ", response.status)
