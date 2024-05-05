import sys

from gameplay_interface import GameView
from menu import *
from gameplay_info_classes import GameInfo
from facade import ClientRequests
from view_model import ViewModel
from view_model import ViewWindows
from view_model import Languages
from menu import ReturnStatus
import time

if __name__ == "__main__":
    CurrentGame = GameView(GameInfo(1, [1, 9, 5], 4, ["Pasha", "Sasha", "Nagibator228", "Боб"]))
    # Preparing all needed class objects
    ViewModelEntity = ViewModel()
    DefaultLanguage = Languages.russian  # TODO remove later(or maybe just move)
    Menu = MenuView(DefaultLanguage)
    LastWindow = ViewWindows.initial_menu
    # LastWindow = ViewWindows.waiting_room  # code for windows design testing
    # ViewModelEntity.window = ViewWindows.waiting_room
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
            Return = Menu.show_resgistration_menu()
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
            elif Return[0] == ReturnStatus.join_lobby:
                pass  # TODO add actual lobby join
            elif Return[0] == ReturnStatus.create_lobby:
                ViewModelEntity.window = ViewWindows.waiting_room  # TODO add actual lobby create
            elif Return[0] == ReturnStatus.settings:
                ViewModelEntity.go_to_settings_window()
            elif Return[0] == ReturnStatus.leaderboard:
                ViewModelEntity.go_to_leaderboard_window()

        elif CurrentWindow == ViewWindows.game:
            Return = CurrentGame.ShowMainGameWindow(ViewModelEntity.language)
            if Return[0] == ReturnStatus.quit:
                time.sleep(0.1)
                sys.exit()

        # TODO - remove the pass to replace with real functions

        elif CurrentWindow == ViewWindows.connecting_by_code:
            pass

        elif CurrentWindow == ViewWindows.leaderboard:
            # TODO - we need to get information about leaders and pass it to the function(for now just framework)
            Return = Menu.show_leaderboard()
            if Return[0] == ReturnStatus.quit:
                time.sleep(0.1)
                ViewModelEntity.go_to_main_menu_window()

        elif CurrentWindow == ViewWindows.waiting_room:  # Behaviour in Lobby
            # Here we need to ask about all the player info, which for now is defaulted
            PlayerAmount = 3
            PlayerNicknames = ["Lol", "Kek", "Cheburek"]
            PlayerReadySignes = [0, 0, 1]

            Return = Menu.show_lobby(PlayerAmount, PlayerNicknames, PlayerReadySignes)
            if Return[0] == ReturnStatus.quit:
                time.sleep(0.1)
                ViewModelEntity.go_to_main_menu_window()
            # TODO add actual checking of ready and stuff
        elif CurrentWindow == ViewWindows.game_result:
            pass

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
