from concurrent import futures
import db_connection
from logs.loggers import get_logger

import grpc
import requests_pb2_grpc
import requests_pb2

from model import Core


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
        return requests_pb2.ResponseUser(status=0,
                                         user_info=requests_pb2.UserInfo(id=user[1], login=user[2], name=user[3]))

    def GetUserById(self, request, context):
        user = self.db.get_user_by_id(_user_id=request.id)
        if user[0] != 0:
            return requests_pb2.ResponseUser(status=user[0])
        _user_info = requests_pb2.UserInfo(id=user[1], login=user[2], name=user[3])
        return requests_pb2.ResponseUser(status=0, user_info=_user_info)

    def CreateGame(self, request, context):
        res = self.core.create_game()
        return requests_pb2.IdResponse(status=res[0], id=res[1])

    def JoinGame(self, request, context):
        code = self.core.join_game(request.game_id, request.user_id)
        return requests_pb2.IsDone(status=code)

    def LeaveGame(self, request, context):
        code = self.core.leave_game(request.game_id, request.user_id)
        return requests_pb2.IsDone(status=code)

    def ChangeReadiness(self, request, context):
        code = self.core.change_readiness(request.game_id, request.user_id)
        return requests_pb2.IsDone(status=code)

    def IsUserReady(self, request, context):
        res = self.core.check_readiness(request.game_id, request.user_id)
        return requests_pb2.Bool(status=res[0], is_true=res[1])

    def GetGoals(self, request, context):
        game_id, user_id = request.game_id, request.user_id
        res = requests_pb2.GoalList()
        res.status = 0
        g1, g2, g3 = res.goals.add(), res.goals.add(), res.goals.add()
        g1.goal, g1.point = 1, user_id  # wtf?
        g2.goal, g2.point = 2, 300
        g3.goal, g3.point = 3, 400
        return res

    def GetUsersInSession(self, request, context):
        res = requests_pb2.UsersInSession()
        res.status = 0
        user_1 = res.users_info.add()
        user_2 = res.users_info.add()
        user_1.id, user_1.login, user_1.name = 1, "gabik", "Kamil"
        user_2.id, user_2.login, user_2.name = 2, "petrovich", "Petya"
        return res

    def GetShopCards(self, request, context):
        res = self.core.get_shop_cards(request.game_id, request.user_id)
        result = requests_pb2.CardsResponse()
        result.status = res[0]
        result.card_id.extend(res[1])
        return result

    def GetUserCards(self, request, context):
        res = self.core.get_player_cards(request.game_id, request.user_id)
        result = requests_pb2.CardsResponse()
        result.status = res[0]
        result.card_id.extend(res[1])
        return result

    def GetPointsCount(self, request, context):
        res = self.core.get_points(request.game_id, request.user_id)
        return requests_pb2.PointsCount(status=res[0], count=res[1])

    def WhoseMove(self, request, context):
        res = self.core.current_player(request.id)
        return requests_pb2.IdResponse(status=res[0], id=res[1])

    def MakeMove(self, request, context):
        code = self.core.make_move(request.game_id, request.user_id, request.card_in_hand,
                                   request.card_in_shop)
        return requests_pb2.IsDone(status=code)
