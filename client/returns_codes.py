code_description_ru = {0: "Успешно", 1: "Игра не найдена", 2: "Игрок не найден", 3: "Игрок уже в этой игре",
                       4: "Игрока нет в этой игре", 5: "Игра ещё не началась", 6: "Игра уже началась",
                       7: "Игра уже закончилась", 8: "В игре максимальное число игроков",
                       9: "Сервер не может поддерживать больше игр", 10: "Ошибка со стороны сервера, попробуйте позже",
                       11: "Некорректные входные данные", 12: "Пользователь с таким логином уже существует",
                       13: "Пароли не совпали", 14: "Пароль неверный",
                       15: "Пользователя с таким индексом не существует",
                       16: "Пользователя с таким логином не существует",
                       17: "Пользователь успешно добавлен",
                       18: "Не выбраны карты игрока", 19: "Не выбраны карты в магазине", 20: "Ход не по правилам",
                       21: "Некорректный тип данных", 22: "Некорректные данные",
                       23: "Ошибка при чтении таблицы резульатов"}

code_description_en = {0: "Ok", 1: "Game not found", 2: "player not found", 3: "player is already in this game",
                       4: "player isn’t in this game", 5: "the game hasn’t started yet",
                       6: "the game has already started",
                       7: "the game is already over", 8: "maximum number of players is already in the game",
                       9: "server can’t host more games", 10: "Internal server error. try again later",
                       11: "Wrong data", 12: "Login already taken",
                       13: "Passwords do not match", 14: "Wrong password",
                       15: "user_id already taken",
                       16: "Login not found",
                       17: "User successfully added",
                       18: "No cards chosen from player", 19: "No cards chosen from shop",
                       20: "This move is against the rules",
                       21: "Wrong data type", 22: "Wrong data", 23: "Error when reading the leaderboard"}


def get_description_ru(code: int) -> str:
    return code_description_ru.get(code, str(code))


def get_description_en(code: int) -> str:
    return code_description_en.get(code, str(code))
