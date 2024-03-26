import threading
import time
from facade import ClientRequests

import enum


class ViewWindows(enum.Enum):
    initial_menu = 1  # окно, в котором мы предлагаем войти/зарегистрироваться
    registration = 2
    login = 3
    main_menu = 4  # окно, в котором предлагаем войти в игру
    connecting_by_code = 5
    waiting_room = 6
    game = 7
    game_result = 8


class ViewModel:
    def __init__(self):
        self.req = ClientRequests()
        self.window = ViewWindows.initial_menu
        self.info_window = None
        self.user_name = None
        self.user_id = None
        self.game_id = None
        self.card = []

    def put_info_window(self, info: str):
        self.info_window = info
        time.sleep(2)
        self.info_window = None

    def go_to_main_menu_window(self):
        self.card = []
        self.game_id = None
        self.window = ViewWindows.main_menu

    def go_to_login_window(self):
        self.card = []
        self.game_id = None
        self.window = ViewWindows.login

    def go_to_registration_window(self):
        self.user_id, self.user_name, self.game_id = None, None, None
        self.window = ViewWindows.registration

    def sign_out(self):
        self.user_id, self.user_name = None, None
        self.window = ViewWindows.initial_menu

    def login_user(self, _user_login: str, _user_password: str):
        response = self.req.login_user(_user_login=_user_login, _password=_user_password)
        if response.status.is_done:
            self.user_id = response.id
            self.user_name = response.name
            self.go_to_main_menu_window()
        else:
            self.put_info_window(response.status.info)

    def register_user(self, _user_login: str, _user_name: str, _user_password1: str, _user_password2: str):
        response = self.req.register_user(_user_login=_user_login, _user_name=_user_name, _password1=_user_password1,
                                          _password2=_user_password2)
        if response.is_done:
            self.put_info_window(response.info)

    def run(self):
        threading.Thread(target=self.current_status, args=(0.1), daemon=True).start()
        threading.Thread(target=self.all_cards, args=(0.2), daemon=True).start()

    def current_status(self, sleep_time: float):
        while True:
            # self.status = req.
            time.sleep(sleep_time)

    def all_cards(self, sleep_time: float):
        while True:
            if self.status == 0:  # если мы играем
                # response = req
                # parse args
                pass
            time.sleep(sleep_time)
