from concurrent import futures
import db_connection

import grpc
import requests_pb2_grpc
import requests_pb2

import server.model as md

from random import randint


class Facade(requests_pb2_grpc.DbServiceServicer):
    def __init__(self):
        super().__init__()
        self.db = db_connection.DBConnection()

    def GetUserById(self, request, context):
        user = self.db.get_user_by_id(_user_id=request.id)
        status = requests_pb2.Status()
        if not user[0]:
            status.is_done = False
            status.info = user[1]
            return requests_pb2.ResponseUser(status=status)
        status.is_done = True
        return requests_pb2.ResponseUser(status=status, id=user[1], login=user[2], name=user[3])

    def RegisterUser(self, request, context):
        result = self.db.add_user(_user_login=request.login, _user_name=request.name, _password_1=request.password1,
                                  _password_2=request.password2)
        return requests_pb2.Status(is_done=result[0], info=result[1])

    def LoginUser(self, request, context):
        user = self.db.login_user(_user_login=request.login, _password=request.password1)
        status = requests_pb2.Status(is_done=True, info="OK")
        if not user[0]:
            status.is_done, status.info = False, user[1]
            return requests_pb2.ResponseUser(status=status)
        return requests_pb2.ResponseUser(status=status, id=user[1], login=user[2], name=user[3])

    # _______________________________________________________
    def CreateGame(self):
        if len(md.GAMES) == md.MX_GAME_ID:
            return requests_pb2.NewGameResponse(status=False, info="Server cannot host more games", game_id=-1)
        new_game_id = randint(1, md.MX_GAME_ID)
        while new_game_id in md.GAMES.keys():
            new_game_id = randint(1, md.MX_GAME_ID)
        new_game = md.Game(new_game_id)
        md.GAMES[new_game_id] = new_game
        return requests_pb2.NewGameResponse(status=True, info="ok", game_id=new_game_id)

    def JoinGame(self, request, context):
        if requests_pb2.game_id not in md.GAMES:
            return requests_pb2.Status(is_done=False, info="Game not found")
        game = md.GAMES[request.game_id]
        result_info = game.add_player(request.player_id)
        return requests_pb2.Status(is_done=(result_info == "ok"), info=result_info)

    def LeaveGame(self, request, context):
        if requests_pb2.game_id not in md.GAMES:
            return requests_pb2.Status(is_done=False, info="Game not found")
        game = md.GAMES[request.game_id]
        result_info = game.kick_player(request.player_id)
        return requests_pb2.Status(is_done=(result_info == "ok"), info=result_info)

    def ChangeReadiness(self, request, context):
        if requests_pb2.game_id not in md.GAMES:
            return requests_pb2.Status(is_done=False, info="Game not found")
        game = md.GAMES[request.game_id]
        result_info = game.change_player_readiness(request.player_id)
        return requests_pb2.Status(is_done=(result_info == "ok"), info=result_info)

    def GetState(self, request, context):
        if request.game_id not in md.GAMES:
            return requests_pb2.State(status=False, info="Game not found")
        game = md.GAMES[request.game_id]
        stage = game.get_current_stage()
