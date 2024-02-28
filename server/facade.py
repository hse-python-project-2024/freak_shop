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
        if not user[0]:
            return requests_pb2.ResponseUser(status=False, info=user[1])
        return requests_pb2.ResponseUser(status=user[0], id=user[1], login=user[2], name=user[3])

    def AddUser(self, request, context):
        result = self.db.add_user(_user_login=request.login, _user_name=request.name, _password_1=request.password1, _password_2=request.password1)
        return requests_pb2.MessageInfo(status=result[0], info=result[1])

#_______________________________________________________
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
            return requests_pb2.JoinGameRespose(status=False, info="Game not found")
        game = md.GAMES[request.game_id]
        result_info = game.add_player(request.player_id)
        return requests_pb2.JoinGameRespose(status=(result_info == "ok"), info=result_info)

    def LeaveGame(self, request, context):
        if requests_pb2.game_id not in md.GAMES:
            return requests_pb2.LeaveGameRespose(status=False, info="Game not found")
        game = md.GAMES[request.game_id]
        result_info = game.kick_player(request.player_id)
        return requests_pb2.LeaveGameRespose(status=(result_info == "ok"), info=result_info)

    def ChangeReadiness(self, request, context):
        if requests_pb2.game_id not in md.GAMES:
            return requests_pb2.ChangeReadinessRespose(status=False, info="Game not found")
        game = md.GAMES[request.game_id]
        result_info = game.change_player_readiness(request.player_id)
        return requests_pb2.ChangeReadinessRespose(status=(result_info == "ok"), info=result_info)

    def GetState(self, request, context):
        if request.game_id not in md.GAMES:
            return requests_pb2.State(status=False, info="Game not found")
        game = md.GAMES[request.game_id]
        stage = game.get_current_stage()
