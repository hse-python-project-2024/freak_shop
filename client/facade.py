import requests_pb2_grpc
import requests_pb2
import grpc

from config import host, port


class ClientRequests:
    def __init__(self):
        channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = requests_pb2_grpc.DbServiceStub(channel)

    def register_user(self, _user_login: str, _user_name: str, _password1: str, _password2: str):
        requests = requests_pb2.NewUser(login=_user_login, name=_user_name, password1=_password1, password2=_password2)
        return self.stub.RegisterUser(requests)

    def login_user(self, _user_login: str, _password: str):
        requests = requests_pb2.NewUser(login=_user_login, password1=_password, password2=_password)
        return self.stub.LoginUser(requests)

    def get_user_by_id(self, _user_id: int):
        request = requests_pb2.Id(id=_user_id)
        return self.stub.GetUserById(request)

    def creat_game(self, _user_id: int):
        request = requests_pb2.Id(id=_user_id)
        return self.stub.CreateGame(request)

    def join_game(self, _game_id: int, _user_id: int):
        request = requests_pb2.GameUserId(game_id=_game_id, user_id=_user_id)
        return self.stub.JoinGame(request)

    def leave_game(self, _game_id: int, _user_id: int):
        request = requests_pb2.GameUserId(game_id=_game_id, user_id=_user_id)
        return self.stub.LeaveGame(request)

    def change_readiness(self, _game_id: int, _user_id: int):
        request = requests_pb2.GameUserId(game_id=_game_id, user_id=_user_id)
        return self.stub.ChangeReadiness(request)

    def is_user_ready(self, _game_id: int, _user_id: int):
        request = requests_pb2.GameUserId(game_id=_game_id, user_id=_user_id)
        return self.stub.IsUserReady(request)

    def get_goals(self, _game_id: int, _user_id: int):
        request = requests_pb2.GameUserId(game_id=_game_id, user_id=_user_id)
        return self.stub.GetGoals(request)

    def get_user_in_session(self, _game_id: int):
        request = requests_pb2.Id(id=_game_id)
        return self.stub.GetUsersInSession(request)

    def get_shop_cards(self, _game_id: int):
        request = requests_pb2.Id(id=_game_id)
        return self.stub.GetShopCards(request)

    def get_user_cards(self, _game_id: int, _user_id: int):
        request = requests_pb2.GameUserId(user_id=_user_id, game_id=_game_id)
        return self.stub.GetUserCards(request)

    def get_points_count(self, _game_id: int, _user_id: int):
        request = requests_pb2.GameUserId(game_id=_game_id, user_id=_user_id)
        return self.stub.GetPointsCount(request)

    def whose_move(self, _game_id: int):
        request = requests_pb2.Id(id=_game_id)
        return self.stub.WhoseMove(request)

    def make_move(self, _game_id: int, _user_id, hand_cards=tuple[int], shop_cards=tuple[int]):
        request = requests_pb2.PickedCards(user_id=_user_id, game_id=_game_id, card_in_hand=hand_cards,
                                           card_in_shop=shop_cards)
        return self.stub.MakeMove(request)

    def get_game_stage(self, _game_id: int):
        request = requests_pb2.Id(id=_game_id)
        return self.stub.GameStage(request)

    def get_leaderboard(self):
        request = requests_pb2.Empty()
        return self.stub.GetLeaderboard(request)
