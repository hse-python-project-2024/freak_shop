import threading
import time
from facade import ClientRequests
import enum
from logs.logger import get_logger


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
        self._LOGGER = get_logger(__name__)
        self.req = ClientRequests()
        self.window = ViewWindows.initial_menu
        self.info_window = None
        self.user_name = None
        self.user_id = None
        self.user_login = None
        self.game_id = None
        self.card = []
        self._LOGGER.info("View model is initialized correctly")

    def put_and_sleep(self, _info: str, _time: float = 2) -> None:
        self.info_window = _info
        time.sleep(_time)
        self.info_window = None

    def put_info_window(self, _info: str, _time: float = 2) -> None:
        threading.Thread(target=self.put_and_sleep, args=(_info, _time), daemon=True).start()

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
        if response.status == 0:
            self.user_id = response.user_info.id
            self.user_name = response.user_info.name
            self.user_login = response.user_info.login
            self.go_to_main_menu_window()
        else:
            self.put_info_window(str(response.status))

    def register_user(self, _user_login: str, _user_name: str, _user_password1: str, _user_password2: str):
        response = self.req.register_user(_user_login=_user_login, _user_name=_user_name, _password1=_user_password1,
                                          _password2=_user_password2)
        if response.status == 0:
            self.put_info_window("Пользователь успешно добавлен")
        else:
            self.put_info_window(str(response.status))

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
