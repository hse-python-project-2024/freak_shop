from ..facade import ClientRequests

if __name__ == '__main__':
    client = ClientRequests()

    print("Get leaderboard")
    response = client.get_leaderboard()
    print(f"status = {response.status}\n")
    for user in response.users:
        print(f"login = {user.login}, game_count = {user.game_count}, wins_count = {user.wins_count}")

    print("Create Game:")
    response = client.creat_game(0)
    print(f"status = {response.status}, Game id = {response.id}\n")

    print("Join Game")
    response = client.join_game(_game_id=1, _user_id=1)
    print(f"status = {response.status}\n")

    print("Leave Game")
    response = client.leave_game(_game_id=1, _user_id=1)
    print(f"status = {response.status}\n")

    print("Change Readiness")
    response = client.change_readiness(_game_id=1, _user_id=1)
    print(f"status = {response.status}\n")

    print("Is user ready")
    response = client.is_user_ready(_game_id=1, _user_id=1)
    print(f"status = {response.status}, user ready = {response.is_true}\n")

    print("Get goals")
    response = client.get_goals(_game_id=1, _user_id=50)
    print(response.status)
    for my_goal in response.goals:
        print(f"goal = {my_goal.goal}, point = {my_goal.point}")
    print()

    print("Get users in Session")
    response = client.get_user_in_session(_game_id=1)
    print(f"status = {response.status}")
    i = 1
    for user in response.users_info:
        print(f"user {i}: user id = {user.id}, user login = {user.login}, user name = {user.name}")
        i += 1
    print()

    print("Get shop cards")
    response = client.get_shop_cards(_game_id=1)
    print(f"status = {response.status}")
    for card in response.card_id:
        print(f"card id = {card}")
    print()

    print("Get user card")
    response = client.get_user_cards(_game_id=0, _user_id=1)
    print(f"status = {response.status}")
    for card in response.card_id:
        print(f"card id = {card}")
    print()

    print("Get point count")
    response = client.get_points_count(_game_id=1, _user_id=1)
    print(f"status = {response.status}, count = {response.count}\n")

    print("Whose move")
    response = client.whose_move(_game_id=1)
    print(f"status = {response.status}, move user_id = {response.id}\n")

    print("Make Move")
    response = client.make_move(_game_id=0, _user_id=1, hand_cards=(1, 2, 3), shop_cards=(4, 5, 6))
    print(f"status = {response.status}\n")

    print("Get game stage:")
    response = client.get_game_stage(_game_id=27)
    print(f"status = {response.status}\n")
    if response.status == 0:
        print(f"Game id = {response.game_stage}")

    while True:
        n = int(input("Enter 1 to add user, 2 to ask user by id, 3 to try log in\n"))
        if n == 1:
            s1 = input("Enter user login:\n")
            s2 = input("Enter user name:\n")
            s3 = input("Enter password\n")
            s4 = input("Confirm password:\n")
            response = client.register_user(s1, s2, s3, s4)
            print(response.status)
            print(response)
        elif n == 2:
            _id = int(input("Enter user id:\n"))
            response = client.get_user_by_id(_id)
            if response.status == 0:
                print(response.status, response.user_info.id, response.user_info.login, response.user_info.name)
            else:
                print(response.status)
        elif n == 3:
            _login = input("Enter login:\n")
            _password = input("Enter password:\n")
            response = client.login_user(_login, _password)
            if response.status == 0:
                print(response.status, response.user_info.id, response.user_info.login, response.user_info.name)
            else:
                print(response.status)
