import enum


class ModelFields(enum.Enum):
    window = 1
    info_window = 2
    user_name = 3
    user_id = 4
    user_login = 5
    game_id = 7
    my_card = 8
    shop_card = 9
    goals = 10
    language = 11
    whose_move = 13


def check_fields(model1, model2, not_take: list[ModelFields]):
    if ModelFields.window not in not_take:
        assert model1.window == model2.window

    if ModelFields.info_window not in not_take:
        assert model1.info_window == model2.info_window

    if ModelFields.user_name not in not_take:
        assert model1.user_name == model2.user_name

    if ModelFields.user_id not in not_take:
        assert model1.user_id == model2.user_id

    if ModelFields.user_login not in not_take:
        assert model1.user_login == model2.user_login

    if ModelFields.game_id not in not_take:
        assert model1.game_id == model2.game_id

    if ModelFields.my_card not in not_take:
        assert sorted(model1.my_card) == sorted(model2.my_card)

    if ModelFields.shop_card not in not_take:
        assert sorted(model1.shop_card) == sorted(model2.shop_card)

    if ModelFields.goals not in not_take:
        for key in model1.goals:
            assert key in model2.goals.keys()
            assert model1.goals[key] == model2.goals[key]

    if ModelFields.language not in not_take:
        assert model1.language == model2.language

    if ModelFields.whose_move not in not_take:
        assert model1.whose_move == model2.whose_move
