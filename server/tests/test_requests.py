from ..model import Core

if __name__ == '__main__':
    core = Core()
    user_id = 11
    user_login = "user1"
    user_name = "USER"

    print(("=" * 50))
    print("LOG IN")
    core.log_in_player(user_id, user_login, user_name)
    print("SUCCESS")
    print(("=" * 50))

    print("CREATE GAME")
    status, game_id = core.create_game()
    print(f"status={status}")
    if status == 0:
        print(f"GAME CREATED: game_id={game_id}")
    print(("=" * 50))

    print("JOIN GAME")
    status = core.join_game(game_id, user_id)
    if status == 0:
        print(f"USER JOINED GAME: game_id={game_id} user_id={user_id}")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    print("LEAVE GAME")
    status = core.leave_game(game_id, user_id)
    if status == 0:
        print(f"USER LEFT GAME: game_id={game_id}, user_id={user_id}")
    print(("=" * 50))

    print("TRY JOINING NON-EXISTANT GAME")
    status = core.join_game(game_id, user_id)
    if status == 0:
        print(f"USER JOINED GAME: game_id={game_id} user_id={user_id}")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    print("CREATE GAME")
    status, game_id = core.create_game()
    print(f"status={status}")
    if status == 0:
        print(f"GAME CREATED: game_id={game_id}")
    print(("=" * 50))

    print("JOIN GAME")
    status = core.join_game(game_id, user_id)
    if status == 0:
        print(f"USER JOINED GAME: game_id={game_id} user_id={user_id}")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    print("CHECK READINESS")
    status, is_ready = core.check_readiness(game_id, user_id)
    if status == 0:
        print(f"is_ready={is_ready==1}")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    print("CHANGE READINESS")
    status = core.change_readiness(game_id, user_id)
    if status == 0:
        print("READINESS CHANGED")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    print("CHECK READINESS")
    status, is_ready = core.check_readiness(game_id, user_id)
    if status == 0:
        print(f"is_ready={is_ready==1}")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    print("CHANGE READINESS")
    status = core.change_readiness(game_id, user_id)
    if status == 0:
        print("READINESS CHANGED")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    print("CHECK READINESS")
    status, is_ready = core.check_readiness(game_id, user_id)
    if status == 0:
        print(f"is_ready={is_ready==1}")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    for _ in range(4):
        print("ADD BOT")
        status = core.add_bot(game_id)
        if status == 0:
            print("BOT ADDED")
        else:
            print(f"ERROR: status={status}")
    print(("=" * 50))

    print("TRY ADDING AN EXTRA BOT")
    print("ADD BOT")
    status = core.add_bot(game_id)
    if status == 0:
        print("BOT ADDED")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    print("REMOVE BOT")
    status = core.remove_bot(game_id)
    if status == 0:
        print("BOT REMOVED")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    print("CHECK READINESS")
    status, is_ready = core.check_readiness(game_id, user_id)
    if status == 0:
        print(f"is_ready={is_ready==1}")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    print("CHANGE READINESS")
    status = core.change_readiness(game_id, user_id)
    if status == 0:
        print("READINESS CHANGED")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))

    print("GET STAGE")
    status, stage = core.get_stage(game_id)
    if status == 0:
        print(f"GOT STAGE: stage={stage}")
    else:
        print(f"ERROR: status={status}")
    print(("=" * 50))
