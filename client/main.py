from facade import ClientRequests

if __name__ == '__main__':
    client = ClientRequests()
    while True:
        n = int(input("Enter 1 to add user, 2 to ask user by id, 3 to try log in\n"))
        if n == 1:
            s1 = input("Enter user login:\n")
            s2 = input("Enter user name:\n")
            s3 = input("Enter password\n")
            s4 = input("Confirm password:\n")
            response = client.register_user(s1, s2, s3, s4)
            print(response.is_done, response.info)
            print(response)
        elif n == 2:
            _id = int(input("Enter user id:\n"))
            response = client.get_user_by_id(_id)
            print(response.status.is_done, response.status.info)
            print(response)
        else:
            _login = input("Enter login:\n")
            _password = input("Enter password:\n")
            response = client.login_user(_login, _password)
            print(response.status.is_done, response.status.info)
            print(response)
