import threading
import time
from facade import ClientRequests
import enum
from returns_codes import get_description_ru


class ViewWindows(enum.Enum):
    initial_menu = 1  # окно, в котором мы предлагаем войти/зарегистрироваться
    registration = 2
    login = 3
    main_menu = 4  # окно, в котором предлагаем войти в игру
    connecting_by_code = 5
    waiting_room = 6
    game = 7
    game_result = 8
    leaderboard = 9
    settings = 10


class Languages(enum.Enum):
    russian = 0
    english = 1


class ViewModel:
    def __init__(self, language=Languages.russian):  # нужно добавить поле готовности игрока
        self.req = ClientRequests()
        self.window = ViewWindows.initial_menu
        self.info_window = None
        self.user_name = None
        self.user_id = None
        self.user_login = None

        self.user_readiness = False  # True if user ready else False
        self.game_id = None
        self.my_card = []
        self.shop_card = []
        self.goals = dict()  # key = name of goal, val = point of this player this person
        self.language = language
        self.users_in_session = dict()  # key = users id, val = their name
        self.whose_move = None  # user_id whose move

    def reset_all_info(self):
        self.user_id, self.user_name, self.game_id, self.user_login, self.whose_move = None, None, None, None, None
        self.goals = dict()
        self.users_in_session = dict()
        self.my_card = []
        self.shop_card = []

    def put_and_sleep(self, _info: int, _time: float = 2) -> None:
        while self.info_window is not None:
            time.sleep(0.1)
        if self.language == Languages.russian:
            self.info_window = get_description_ru(_info)
        elif self.language == Languages.english:
            self.info_window = str(_info)  # TODO: add english language
        else:
            self.info_window = str(_info)
        time.sleep(_time)
        self.info_window = None

    def put_info_window(self, _info: int, _time: float = 2) -> None:
        threading.Thread(target=self.put_and_sleep, args=(_info, _time), daemon=True).start()

    def go_to_main_menu_window(self):
        self.my_card = []
        self.shop_card = []
        self.goals = dict()
        self.users_in_session = dict()
        self.game_id = None
        self.user_readiness = False
        self.whose_move = None
        self.window = ViewWindows.main_menu

    def go_to_login_window(self):
        self.my_card = []
        self.shop_card = []
        self.game_id = None
        self.window = ViewWindows.login

    def go_to_registration_window(self):
        self.reset_all_info()
        self.window = ViewWindows.registration

    def go_to_initial_window(self):
        self.reset_all_info()
        self.window = ViewWindows.initial_menu

    def go_to_settings_window(self):
        self.reset_all_info()
        self.window = ViewWindows.settings

    def go_to_leaderboard_window(self):
        self.reset_all_info()
        self.window = ViewWindows.leaderboard

    def go_to_game_menu(self):
        self.window = ViewWindows.game

    def sign_out(self):
        self.reset_all_info()
        self.window = ViewWindows.initial_menu

    def login_user(self, _user_login: str, _user_password: str):
        response = self.req.login_user(_user_login=_user_login, _password=_user_password)
        if response.status == 0:
            self.user_id = response.user_info.id
            self.user_name = response.user_info.name
            self.user_login = response.user_info.login
            self.go_to_main_menu_window()
        else:
            self.put_info_window(_info=response.status)

    def register_user(self, _user_login: str, _user_name: str, _user_password1: str, _user_password2: str):
        response = self.req.register_user(_user_login=_user_login, _user_name=_user_name, _password1=_user_password1,
                                          _password2=_user_password2)
        if response.status == 0:
            self.put_info_window(_info=17, _time=1)
            self.window = ViewWindows.initial_menu
        else:
            self.put_info_window(_info=response.status)

    def change_language(self, new_language: Languages):
        self.language = new_language

    def change_user_readiness(self):
        response = self.req.change_readiness(_game_id=self.game_id, _user_id=self.user_id)
        if response.status == 0:
            self.user_readiness = not self.user_readiness
        else:
            self.put_info_window(_info=response.status)

    def join_game(self, _game_id: int):
        response = self.req.join_game(_game_id=_game_id, _user_id=self.user_id)
        if response.status == 0:
            self.start_game(_game_id=_game_id)
        else:
            self.put_info_window(_info=response.status)

    def create_game(self):
        response = self.req.creat_game(_user_id=self.user_id)
        if response.status == 0:
            self.start_game(_game_id=response.id)
        else:
            self.put_info_window(_info=response.status)

    def leave_game(self):
        response = self.req.leave_game(_game_id=self.game_id, _user_id=self.user_id)
        if response.status == 0:
            self.go_to_main_menu_window()
        else:
            self.put_info_window(_info=response.status)

    def make_move(self, my_cards: tuple[int], shop_cards: tuple[int]):
        response = self.req.make_move(_game_id=self.game_id, _user_id=self.user_id, hand_cards=my_cards, shop_cards=shop_cards)
        if response.status != 0:
            self.put_info_window(_info=response.status)

    def start_game(self, _game_id: int):
        self.game_id = _game_id
        self.run_all_game_requests()

    def run_all_game_requests(self):
        threading.Thread(target=self.get_goal_points, args=(self, 0.5), daemon=True).start()
        threading.Thread(target=self.get_users_in_session, args=(self, 0.5), daemon=True).start()
        threading.Thread(target=self.get_user_cards, args=(self, 0.1), daemon=True).start()
        threading.Thread(target=self.get_shop_cards, args=(self, 0.1), daemon=True).start()
        threading.Thread(target=self.get_whose_move, args=(self, 0.1), daemon=True).start()

    def get_goal_points(self, sleep_time: float):
        while True:
            if self.game_id is None:
                break
            response = self.req.get_goals(_game_id=self.game_id, _user_id=self.user_id)
            if response.status == 0:
                for my_goal in response.goals:
                    self.goals[my_goal.goal] = response.goals[my_goal.point]
            else:
                self.put_info_window(_info=response.status, _time=1)
            time.sleep(sleep_time)

    def get_users_in_session(self, sleep_time: float):
        while True:
            if self.game_id is None:
                break
            response = self.req.get_user_in_session(_game_id=self.game_id)
            if response.status == 0:
                for my_user in response.users_info:
                    self.users_in_session[my_user.id] = my_user.name
            else:
                self.put_info_window(_info=response.status, _time=1)
            time.sleep(sleep_time)

    def get_user_cards(self, sleep_time: float):
        while True:
            if self.game_id is None:
                break
            response = self.req.get_user_cards(_user_id=self.user_id)
            if response.status == 0:
                self.my_card = list(response.card_id)
            else:
                self.put_info_window(_info=response.status, _time=1)
            time.sleep(sleep_time)

    def get_shop_cards(self, sleep_time: float):
        while True:
            if self.game_id is None:
                break
            response = self.req.get_shop_cards(_game_id=self.game_id)
            if response.status == 0:
                self.shop_card = list(response.card_id)
            else:
                self.put_info_window(_info=response.status, _time=1)
            time.sleep(sleep_time)

    def get_whose_move(self, sleep_time: float):
        while True:
            if self.game_id is None:
                break
            response = self.req.whose_move(_game_id=self.game_id)
            if response.status == 0:
                self.whose_move = response.id
            else:
                self.put_info_window(_info=response.status, _time=1)
            time.sleep(sleep_time)