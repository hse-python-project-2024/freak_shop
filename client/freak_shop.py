import sys

from gameplay_interface import GameView
from menu import *
from gameplay_info_classes import GameInfo
from facade import ClientRequests
from view_model import ViewModel
from view_model import ViewWindows
from view_model import Languages
from menu import ReturnStatus
from logs.logger import get_logger
import time

if __name__ == "__main__":
    # Preparing all needed class objects
    _LOGGER = get_logger(__name__)
    CurrentGame = GameView()
    ViewModelEntity = ViewModel()
    DefaultLanguage = Languages.russian  # TODO remove later(or maybe just move)
    Menu = MenuView(DefaultLanguage)
    LastWindow = ViewWindows.initial_menu
    IsGameStarted = False
    # LastWindow = ViewWindows.game  # code for windows design testing
    # ViewModelEntity.window = ViewWindows.game
    while True:
        CurrentWindow = ViewModelEntity.window  # Check what window to display right now
        if CurrentWindow != LastWindow:
            LastWindow = CurrentWindow
            Menu.reset_menu_info()

        # TODO add settings window to registration as well(for language change)
        if CurrentWindow == ViewWindows.initial_menu:  # Behaviour in Initial Menu
            Return = Menu.show_initial_menu()
            if Return[0] == ReturnStatus.quit:
                sys.exit()
            elif Return[0] == ReturnStatus.go_to_login:
                ViewModelEntity.go_to_login_window()
            elif Return[0] == ReturnStatus.go_to_register:
                ViewModelEntity.go_to_registration_window()

        elif CurrentWindow == ViewWindows.login:  # Behaviour in Login Menu
            Return = Menu.show_login_menu()
            if Return[0] == ReturnStatus.login:
                ViewModelEntity.login_user(Return[1][0], Return[1][1])
                if ViewModelEntity.info_window is None:
                    Menu.reset_menu_info()
                    ViewModelEntity.go_to_main_menu_window()
            elif Return[0] == ReturnStatus.quit:
                time.sleep(0.1)
                ViewModelEntity.go_to_initial_window()

        elif CurrentWindow == ViewWindows.registration:  # Behaviour in Registration Menu
            Return = Menu.show_registration_menu()
            if Return[0] == ReturnStatus.register:
                ViewModelEntity.register_user(Return[1][0], Return[1][1], Return[1][2], Return[1][3])
                if ViewModelEntity.info_window is None:
                    Menu.reset_menu_info()
            elif Return[0] == ReturnStatus.quit:
                time.sleep(0.1)
                ViewModelEntity.go_to_initial_window()

        elif CurrentWindow == ViewWindows.main_menu:  # Behaviour in Main Menu
            Return = Menu.show_main_menu()
            if Return[0] == ReturnStatus.quit:
                sys.exit()
            elif Return[0] == ReturnStatus.go_to_join_lobby:
                ViewModelEntity.go_to_jbc_window()
            elif Return[0] == ReturnStatus.create_lobby:
                ViewModelEntity.create_game()
                time.sleep(0.1)
            elif Return[0] == ReturnStatus.settings:
                ViewModelEntity.go_to_settings_window()
            elif Return[0] == ReturnStatus.leaderboard:
                ViewModelEntity.go_to_leaderboard_window()

        elif CurrentWindow == ViewWindows.game:
            if not IsGameStarted:
                time.sleep(1)
                IsGameStarted = True
                PlayerNicknames = []
                for user in ViewModelEntity.users:
                    PlayerNicknames.append(user.name)
                NewGameInfo = GameInfo(list(ViewModelEntity.goals.keys()), len(ViewModelEntity.users), PlayerNicknames,
                                       ViewModelEntity.my_pos_in_users())
                _LOGGER.info(f"Started game with players:  {PlayerNicknames} on position {ViewModelEntity.my_pos_in_users()}")
                CurrentGame.update_start_game_status(NewGameInfo)
            CurrentGame.update_game_info(ViewModelEntity.my_card,ViewModelEntity.shop_card
                                         ,ViewModelEntity.whose_move)
            Return = CurrentGame.ShowMainGameWindow(ViewModelEntity.language)
            if Return[0] == ReturnStatus.quit:
                time.sleep(0.1)
                IsGameStarted = False
                ViewModelEntity.leave_game()
            elif Return[0] == ReturnStatus.trade:
                ViewModelEntity.make_move(Return[1][0],Return[1][1])

        elif CurrentWindow == ViewWindows.connecting_by_code:
            Return = Menu.show_join_by_code_menu()
            if Return[0] == ReturnStatus.join_lobby:
                ViewModelEntity.join_game(Return[1][0])
                time.sleep(1)
            elif Return[0] == ReturnStatus.quit:
                time.sleep(0.1)
                ViewModelEntity.go_to_main_menu_window()

        elif CurrentWindow == ViewWindows.leaderboard:
            # TODO - we need to get information about leaders and pass it to the function(for now just framework)
            Return = Menu.show_leaderboard()
            if Return[0] == ReturnStatus.quit:
                time.sleep(0.1)
                ViewModelEntity.go_to_main_menu_window()

        elif CurrentWindow == ViewWindows.waiting_room:  # Behaviour in Lobby
            PlayerAmount = len(ViewModelEntity.users)
            PlayerNicknames = []
            PlayerReadySinges = []
            for i in range(PlayerAmount):
                PlayerNicknames.append(ViewModelEntity.users[i].name)
                PlayerReadySinges.append(ViewModelEntity.users[i].readiness)
            Return = Menu.show_lobby(PlayerAmount, PlayerNicknames, PlayerReadySinges,ViewModelEntity.game_id)
            if Return[0] == ReturnStatus.change_readiness:
                ViewModelEntity.change_user_readiness()
            elif Return[0] == ReturnStatus.quit:
                time.sleep(0.1)
                ViewModelEntity.leave_game()

        elif CurrentWindow == ViewWindows.game_result:
            pass  # TODO - remove the pass to replace with real functions

        elif CurrentWindow == ViewWindows.settings:  # Behaviour in Settings Menu
            Return = Menu.show_settings_menu()
            if Return[0] == ReturnStatus.quit:
                time.sleep(0.1)
                ViewModelEntity.go_to_main_menu_window()
            if Return[0] == ReturnStatus.change_lang:
                new_lang_str = Return[1][0]
                new_lang = None
                if new_lang_str == "ru":  # Changing str into Language type object
                    new_lang = Languages.russian
                elif new_lang_str == "en":
                    new_lang = Languages.english
                Menu.change_menu_language(new_lang)
                ViewModelEntity.change_language(new_lang)
        # TODO fix all the indents of strings that change from languages (if there will be time and will)

        # Show messages
        Message = ViewModelEntity.info_window
        if Message is not None:
            Menu.show_message(Message)
        pygame.display.update()
