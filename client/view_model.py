import threading
import time
from facade import ClientRequests

import enum
from logs.logger import get_logger
from returns_codes import get_description_ru


class User:
    def __init__(self, _id, _name):
        self.id = _id
        self.name = _name
        self.readiness = False
        self.cards = []
        self.point_count = 0


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
        self._LOGGER = get_logger(__name__)
        self.req = ClientRequests()
        self.window = ViewWindows.initial_menu
        self.info_window = None
        self.user_name = None
        self.user_id = None
        self.user_login = None
        self._LOGGER.info("View model is initialized correctly")

        self.game_id = None
        self.my_card = []
        self.shop_card = []
        self.goals = dict()  # key = id of goal, val = point of this player this person
        self.language = language
        self.users = []  # list[User]
        self.whose_move = None  # user_id whose move
        self.mutex = threading.Lock()

    def my_pos_in_users(self):
        self.mutex.acquire()
        for i in range(len(self.users)):
            if self.users[i].id == self.user_id:
                self.mutex.release()
                return i
        self.mutex.release()
        return -1

    def reset_all_info(self):
        self.user_id, self.user_name, self.game_id, self.user_login, self.whose_move = None, None, None, None, None
        self.goals = dict()
        self.users = []
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
        self.game_id = None
        self.users = []
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
        self.window = ViewWindows.settings

    def go_to_leaderboard_window(self):
        self.window = ViewWindows.leaderboard

    def go_to_jbc_window(self):  # jbc = Join by code
        self.window = ViewWindows.connecting_by_code

    def go_to_game_menu(self):  # Testing only, not needed in real game
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
        if response.status != 0:
            self.put_info_window(_info=response.status)
        else:
            self.users[self.my_pos_in_users()].readiness = not self.users[self.my_pos_in_users()].readiness

    def join_game(self, _game_id: int):
        response = self.req.join_game(_game_id=_game_id, _user_id=self.user_id)
        if response.status == 0:
            self.go_to_waiting_room(_game_id=_game_id)
        else:
            self.put_info_window(_info=response.status)

    def create_game(self):
        response = self.req.creat_game(_user_id=self.user_id)
        if response.status == 0:
            response2 = self.req.join_game(_game_id=response.id, _user_id=self.user_id)
            if response2.status == 0:
                self.go_to_waiting_room(_game_id=response.id)
            else:
                self.put_info_window(_info=response2.status)
        else:
            self.put_info_window(_info=response.status)

    def leave_game(self):
        response = self.req.leave_game(_game_id=self.game_id, _user_id=self.user_id)
        if response.status == 0:
            self.go_to_main_menu_window()
        else:
            self.put_info_window(_info=response.status)

    def make_move(self, my_cards: tuple[int], shop_cards: tuple[int]):
        self._LOGGER.info(f"make move with player cards:  {my_cards} and shop cards: {shop_cards}")
        response = self.req.make_move(_game_id=self.game_id, _user_id=self.user_id, hand_cards=my_cards,
                                      shop_cards=shop_cards)
        if response.status != 0:
            self.put_info_window(_info=response.status)

    def start_game(self):
        self.order_user()
        self.window = ViewWindows.game
        self.run_all_game_requests()

    def order_user(self):
        response = self.req.get_user_in_session(_game_id=self.game_id)
        if response.status == 0:
            self.users = []
            for my_user in response.users_info:
                self.users.append(User(_id=my_user.id, _name=my_user.name))
        else:
            self.put_info_window(_info=response.status, _time=1)

    def go_to_waiting_room(self, _game_id: int):
        self.window = ViewWindows.waiting_room
        self.game_id = _game_id
        self.users.append(User(_id=self.user_id, _name=self.user_name))
        threading.Thread(target=self.get_users_in_session, args=(0.4, True,), daemon=True).start()
        threading.Thread(target=self.check_user_readiness, args=(0.2,), daemon=True).start()

    def run_all_game_requests(self):
        threading.Thread(target=self.get_users_in_session, args=(1,), daemon=True).start()
        threading.Thread(target=self.get_shop_cards, args=(0.2,), daemon=True).start()
        threading.Thread(target=self.get_whose_move, args=(0.2,), daemon=True).start()
        for user in self.users:
            threading.Thread(target=self.get_goal_points, args=(0.5, user.id,), daemon=True).start()
            threading.Thread(target=self.get_user_cards, args=(0.2, user.id,), daemon=True).start()

    def check_user_readiness(self, sleep_time):
        self._LOGGER.info(
            f"start asking users readiness, sleep time = {sleep_time}")
        while True:
            self.mutex.acquire()
            try:
                if self.window != ViewWindows.waiting_room:
                    break
                start_game = len(self.users) > 1
                for user in self.users:
                    self._LOGGER.info(f"make request is_user_ready with id = {user.id}")
                    response = self.req.is_user_ready(_game_id=self.game_id, _user_id=user.id)
                    if response.status == 0:
                        user.readiness = response.is_true
                        start_game &= user.readiness
                    else:
                        self.put_info_window(_info=response.status)
                        start_game = False
                if start_game:
                    self._LOGGER.info(f"Start game with id = {self.game_id}")
                    self.start_game()
            except Exception as e:
                self._LOGGER.error(f"Exception in check_user_readiness with error {e}")
            finally:
                self.mutex.release()
                time.sleep(sleep_time)

    def get_goal_points(self, sleep_time: float, _user_id: int):
        self._LOGGER.info(
            f"start asking users goal points, sleep time = {sleep_time}, user id = {_user_id}")
        while True:
            self.mutex.acquire()
            try:
                if self.game_id is None:
                    break
                #self._LOGGER.info(f"make request get_goals game_id = {self.game_id}, user_id = {_user_id}")
                response = self.req.get_goals(_game_id=self.game_id, _user_id=_user_id)
                if response.status == 0:
                    for my_goal in response.goals:
                        self.goals[my_goal.goal] = response.goals[my_goal.point]
                else:
                    self.put_info_window(_info=response.status, _time=1)
            except Exception as e:
                self._LOGGER.error(f"Exception in get_goal_points with error {e}")
            finally:
                self.mutex.release()
                time.sleep(sleep_time)

    def get_users_in_session(self, sleep_time: float, in_waiting_room=False):
        self._LOGGER.info(
            f"start asking users in session, sleep time = {sleep_time}, in waiting room = {in_waiting_room}")
        while True:
            self.mutex.acquire()
            try:
                if self.game_id is None or (in_waiting_room and self.window != ViewWindows.waiting_room):
                    break
                #self._LOGGER.info("make request get_user_in_session")
                response = self.req.get_user_in_session(_game_id=self.game_id)
                if response.status == 0:
                    need_erase = []
                    for user in self.users:
                        need_erase.append(user.id)
                    for my_user in response.users_info:
                        if my_user.id in need_erase:
                            need_erase.remove(my_user.id)

                        added = False
                        for user in self.users:
                            if user.id == my_user.id:
                                added = True
                                break
                        if not added:
                            self.users.append(User(_id=my_user.id, _name=my_user.name))

                    for user_id in need_erase:
                        for i in range(len(self.users)):
                            if user_id == self.users[i].id:
                                del self.users[i]
                                break
                else:
                    self.put_info_window(_info=response.status, _time=1)
            except Exception as e:
                self._LOGGER.error(f"Exception in get_users_in_session with error {e}")
            finally:
                self.mutex.release()
                time.sleep(sleep_time)

    def get_user_cards(self, sleep_time: float, _user_id: int):
        self._LOGGER.info(
            f"start asking users cards, sleep time = {sleep_time}, user id = {_user_id}")
        while True:
            self.mutex.acquire()
            try:
                if self.game_id is None:
                    break
                # self._LOGGER.info(f"make request get_user_cards game_id = {self.game_id}, user_id = {_user_id}")
                response = self.req.get_user_cards(_game_id=self.game_id, _user_id=_user_id)
                if response.status == 0:
                    self.my_card = list(response.card_id)
                else:
                    self.put_info_window(_info=response.status, _time=1)
            except Exception as e:
                self._LOGGER.error(f"Exception in get_user_cards with error {e}")
            finally:
                self.mutex.release()
                time.sleep(sleep_time)

    def get_shop_cards(self, sleep_time: float):
        self._LOGGER.info(
            f"start asking shop cards readiness, sleep time = {sleep_time}, game id = {self.game_id}")
        while True:
            self.mutex.acquire()
            try:
                if self.game_id is None:
                    break
                # self._LOGGER.info(f"make request get_shop_cards, game_id = {self.game_id}")
                response = self.req.get_shop_cards(_game_id=self.game_id)
                if response.status == 0:
                    self.shop_card = list(response.card_id)
                else:
                    self.put_info_window(_info=response.status, _time=1)
            except Exception as e:
                self._LOGGER.error(f"Exception in get_shop_cards with error {e}")
            finally:
                self.mutex.release()
                time.sleep(sleep_time)

    def get_whose_move(self, sleep_time: float):
        self._LOGGER.info(
            f"start asking shop cards readiness, sleep time = {sleep_time}, game id = {self.game_id}")
        while True:
            self.mutex.acquire()
            try:
                if self.game_id is None:
                    break
                # self._LOGGER.info(f"make request whose_move, game_id = {self.game_id}")
                response = self.req.whose_move(_game_id=self.game_id)
                if response.status == 0:
                    for i in range(len(self.users)):
                        if self.users[i].id == response.id:
                            self.whose_move = i
                            break
                else:
                    self.put_info_window(_info=response.status, _time=1)
            except Exception as e:
                self._LOGGER.error(f"Exception in get_whose_move with error {e}")
            finally:
                self.mutex.release()
                time.sleep(sleep_time)
