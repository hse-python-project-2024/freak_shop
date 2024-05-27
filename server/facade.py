from concurrent import futures
import db_connection
from logs.loggers import get_logger

import grpc
import requests_pb2_grpc
import requests_pb2

from model import Core

from goal_ids import GOAL_ID


class Facade(requests_pb2_grpc.DbServiceServicer):
    def __init__(self):
        self._LOGGER = get_logger(__name__)
        super().__init__()
        self.db = db_connection.DBConnection()
        self._LOGGER.info("Корректное подлючение фасада")

        self.core = Core()

    def RegisterUser(self, request, context):
        result = self.db.add_user(_user_login=request.login, _user_name=request.name, _password_1=request.password1,
                                  _password_2=request.password2)
        return requests_pb2.IsDone(status=result)

    def LoginUser(self, request, context):
        user = self.db.login_user(_user_login=request.login, _password=request.password1)
        if user[0] != 0:
            return requests_pb2.ResponseUser(status=user[0])
        self.core.log_in_player(player_id=user[1], login=user[2], name=user[3])
        return requests_pb2.ResponseUser(status=0,
                                         user_info=requests_pb2.UserInfo(id=user[1], login=user[2], name=user[3]))

    def GetUserById(self, request, context):
        user = self.db.get_user_by_id(_user_id=request.id)
        if user[0] != 0:
            return requests_pb2.ResponseUser(status=user[0])
        _user_info = requests_pb2.UserInfo(id=user[1], login=user[2], name=user[3])
        return requests_pb2.ResponseUser(status=0, user_info=_user_info)

    def CreateGame(self, request, context):
        self._LOGGER.info(f"CREATE GAME")

        res = self.core.create_game()

        if res[0]:
            self._LOGGER.info(f"ERROR (GAME NOT CREATED): status={res[0]}")
        else:
            self._LOGGER.info(f"GAME CREATED: game_id={res[1]}")
        return requests_pb2.IdResponse(status=res[0], id=res[1])

    def JoinGame(self, request, context):
        game_id = request.game_id
        user_id = request.user_id
        self._LOGGER.info(f"JOIN GAME: game_id={game_id} player_id={user_id}")

        code = self.core.join_game(game_id, user_id)

        self._LOGGER.info(f"RESULT: {code}")
        return requests_pb2.IsDone(status=code)

    def LeaveGame(self, request, context):
        code = self.core.leave_game(request.game_id, request.user_id)
        return requests_pb2.IsDone(status=code)

    def ChangeReadiness(self, request, context):
        game_id = request.game_id
        user_id = request.user_id
        self._LOGGER.info(f"CHANGE READINESS: game_id={game_id} player_id={user_id}")

        code = self.core.change_readiness(game_id=game_id, player_id=user_id)

        self._LOGGER.info(f"RESULT: {code}")
        return requests_pb2.IsDone(status=code)

    def IsUserReady(self, request, context):
        game_id = request.game_id
        user_id = request.user_id
        # self._LOGGER.info(f"CHECK READINESS: game_id={game_id} player_id={user_id}")

        res = self.core.check_readiness(request.game_id, request.user_id)

        # self._LOGGER.info(f"RESULT: status={res[0]} ready={res[1]}")
        return requests_pb2.Bool(status=res[0], is_true=res[1])

    def GetGoals(self, request, context):
        game_id = request.game_id
        user_id = request.user_id
        self._LOGGER.info(f"GET GOALS: game_id={game_id} player_id={user_id}")

        result = requests_pb2.GoalList()
        res = self.core.get_goals(game_id, user_id)
        result.status = res[0]
        if not res[0]:
            for goal_name in res[1].keys():
                goal = result.goals.add()
                goal.goal = GOAL_ID[goal_name]
                goal.point = res[1][goal_name]

        self._LOGGER.info(f"RESULT: status={res[0]} goals={res[1]}")
        return result

    def GetUsersInSession(self, request, context):
        result = requests_pb2.UsersInSession()
        res = self.core.get_players(request.id)
        result.status = res[0]
        if not res[0]:
            for user_id in res[1]:
                user = result.users_info.add()
                user.id = user_id
                user.login = res[1][user_id]["login"]
                user.name = res[1][user_id]["name"]
        return result

    def GetShopCards(self, request, context):
        game_id = request.id
        # self._LOGGER.info(f"GET SHOP CARDS: game_id={game_id}")
        res = self.core.get_shop_cards(game_id)
        result = requests_pb2.CardsResponse()
        result.status = res[0]
        result.card_id.extend(res[1])

        # self._LOGGER.info(f"RESULT: {res}")
        return result

    def GetUserCards(self, request, context):
        game_id = request.game_id
        user_id = request.user_id
        # self._LOGGER.info(f"GET USER CARDS: game_id={game_id} player_id={user_id}")

        res = self.core.get_player_cards(game_id, user_id)
        result = requests_pb2.CardsResponse()
        result.status = res[0]
        result.card_id.extend(res[1])

        # self._LOGGER.info(f"RESULT: {res}")
        return result

    def GetPointsCount(self, request, context):
        res = self.core.get_points(request.game_id, request.user_id)
        return requests_pb2.PointsCount(status=res[0], count=res[1])

    def WhoseMove(self, request, context):
        res = self.core.current_player(request.id)
        return requests_pb2.IdResponse(status=res[0], id=res[1])

    def MakeMove(self, request, context):
        game_id = request.game_id
        user_id = request.user_id
        card_in_hand = request.card_in_hand
        card_in_shop = request.card_in_shop
        self._LOGGER.info(
            f"MAKE MOVE: game_id={game_id} player_id={user_id} player_cards={card_in_hand} shop_cards={card_in_shop}")

        code = self.core.make_move(game_id, user_id, card_in_hand,
                                   card_in_shop)
        self._LOGGER.info(f"RESULT: {code}")
        return requests_pb2.IsDone(status=code)

    def GameStage(self, request, context):
        game_id = request.id
        self._LOGGER.info(f"GAME STAGE: game_id={game_id}")

        code, stage = self.core.get_stage(game_id)
        if code:
            self._LOGGER.info(f"RESULT: status={code}")
        else:
            self._LOGGER.info(f"RESULT: status={code} game_stage={['WAITING', 'RUNNING', 'RESULTS'][stage]}")
        res = requests_pb2.Stage(status=code, game_stage=stage)
        return res

    def GetLeaderboard(self, request, context):
        res = requests_pb2.BestPlayers()
        self._LOGGER.info(f"GET LEADERBOARD")
        try:
            best_pl = self.db.get_best_player(count=5)
            res.status = 0
            for login, game_count, game_win in best_pl:
                user = res.users.add()
                user.login = login
                user.game_count = game_count
                user.wins_count = game_win
            return res
        except Exception as e:
            self._LOGGER.error(f"Error request to database leaderboard. Exception: {e}")
            res.status = 23
            return res
