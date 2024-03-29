from interface_setup import *
import time
from facade import ClientRequests


class MenuView:
    def show_enter_menu(self, DataBaseRequester):
        ReturnToMenu = 0
        LoginText = RegistrationFont.render("Логин :", False, (0, 0, 0))
        PassowrdText = RegistrationFont.render("Пароль : ", False, (0, 0, 0))
        ConfirmText = RegistrationFont.render("Войти", False, (0, 0, 0))
        LoginButton = Rect(ScreenWidth * 5 / 38, ScreenHeight / 5, 1000, 150)
        PasswordButton = Rect(ScreenWidth * 5 / 38, ScreenHeight * 6 / 10, 1000, 150)
        ConfirmButton = Rect(ScreenWidth * 27 / 38, ScreenHeight / 3 - 40, 400, 400)
        EyeIconButton = Rect(ScreenWidth / 80, ScreenHeight * 6 / 10 - 20, 220, 180)
        BackButton = Rect(ScreenWidth * 6 / 7, ScreenHeight * 1 / 30, 180, 180)
        LoginInput = ""
        PasswordInput = ""
        active = 0
        password_show = False
        while True:
            ErrorMessage = ''
            error_message_show = False
            screen.fill(RegistrationBackgroundColor)
            for event in pygame.event.get():
                if event.type == QUIT:
                    ReturnToMenu = 1
                if event.type == MOUSEBUTTONDOWN:
                    MousePosition = pygame.mouse.get_pos()
                    if LoginButton.collidepoint(MousePosition):
                        active = 1
                    elif PasswordButton.collidepoint(MousePosition):
                        active = 2
                    elif ConfirmButton.collidepoint(MousePosition):
                        active = 0
                        LoginSuccess = DataBaseRequester.login_user(LoginInput, PasswordInput)
                        print(LoginSuccess)
                        if LoginSuccess.status.info == "OK":
                            ReturnToMenu = 2
                        else:
                            ErrorMessage = LoginSuccess.status.info
                            error_message_show = True
                    elif EyeIconButton.collidepoint(MousePosition):
                        password_show = not password_show
                    elif BackButton.collidepoint(MousePosition):
                        active = 0
                        ReturnToMenu = 1
                    else:
                        active = 0
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        active += 1 * (active < 2)
                    elif event.key == K_UP:
                        active -= 1 * (active > 1)
                    else:
                        if active == 1:
                            if event.key == K_BACKSPACE:
                                LoginInput = LoginInput[:-1]
                            elif event.key == K_RETURN:
                                active = 2
                            elif len(LoginInput) < MaxLoginLength:
                                LoginInput += event.unicode
                        elif active == 2:
                            if event.key == K_BACKSPACE:
                                PasswordInput = PasswordInput[:-1]
                            elif event.key == K_RETURN:
                                active = 0
                            elif len(PasswordInput) < MaxPasswordLength:
                                PasswordInput += event.unicode
                        if active == 0:
                            if event.key == K_RETURN:
                                LoginSuccess = DataBaseRequester.login_user(LoginInput, PasswordInput)
                                print(LoginSuccess)
                                if LoginSuccess.status.info == "OK":
                                    ReturnToMenu = 2
                                else:
                                    ErrorMessage = LoginSuccess.status.info
                                    error_message_show = True

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_ESCAPE]:
                ReturnToMenu = 1

            pygame.draw.rect(screen, RegistrationButtonColor, LoginButton)
            pygame.draw.rect(screen, RegistrationButtonColor, PasswordButton)
            pygame.draw.rect(screen, RegistrationButtonColor, ConfirmButton)
            screen.blit(LoginText, (LoginButton.midtop[0] - 100, LoginButton.midtop[1] - 80))
            screen.blit(PassowrdText, (PasswordButton.midtop[0] - 120, PasswordButton.midtop[1] - 80))
            screen.blit(ConfirmText, (ConfirmButton.center[0] - 85, ConfirmButton.center[1] - 30))

            LoginInputText = RegistrationFont.render(LoginInput + (active == 1) * '|', False, (0, 0, 0))
            screen.blit(LoginInputText, (LoginButton.left, LoginButton.center[1] - 35))

            if password_show:
                EyeIconImage = pygame.image.load("src/img/EyeIcon.png").convert_alpha()
                screen.blit(pygame.transform.scale(EyeIconImage, (220, 180)),
                            (ScreenWidth / 80, ScreenHeight * 6 / 10 - 20))
                PassowrdInputText = RegistrationFont.render(PasswordInput + (active == 2) * '|', False, (0, 0, 0))
                screen.blit(PassowrdInputText, (PasswordButton.left, PasswordButton.center[1] - 35))
            else:
                EyeIconImage = pygame.image.load("src/img/EyeIconCrossed.png").convert_alpha()
                screen.blit(pygame.transform.scale(EyeIconImage, (250, 160)),
                            (ScreenWidth / 80 - 10, ScreenHeight * 6 / 10 - 10))
                PassowrdInputText = RegistrationFont.render('*' * len(PasswordInput) + (active == 2) * '|', False,
                                                            (0, 0, 0))
                screen.blit(PassowrdInputText, (PasswordButton.left, PasswordButton.center[1] - 10))

            BackIconImage = pygame.image.load("src/img/BackIcon.png").convert_alpha()
            screen.blit(pygame.transform.scale(BackIconImage, (180, 180)),
                        (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))
            if error_message_show:
                self.message_show(ErrorMessage)
                pygame.display.update()
                time.sleep(2)
            else:
                pygame.display.update()
            if ReturnToMenu == 1:
                return "menu"
            elif ReturnToMenu == 2:
                return self.show_ingame_menu(DataBaseRequester)

    def show_resgistration_menu(self, DataBaseRequester):
        ReturnToMenu = 0
        LoginText = RegistrationFont.render("Логин :", False, (0, 0, 0))
        NicknameText = RegistrationFont.render("Имя :", False, (0, 0, 0))
        PassowrdText = RegistrationFont.render("Пароль : ", False, (0, 0, 0))
        RepeatPasswordText = RegistrationFont.render("Повторите пароль : ", False, (0, 0, 0))
        ConfirmText = RegistrationFont.render("Регистрация", False, (0, 0, 0))
        LoginButton = Rect(ScreenWidth * 5 / 38, ScreenHeight / 12 + 20, 1000, 150)
        NicknameButton = Rect(ScreenWidth * 5 / 38, ScreenHeight / 4 + 60, 1000, 150)
        PasswordButton = Rect(ScreenWidth * 5 / 38, ScreenHeight / 2 + 20, 1000, 150)
        RepeatPasswordButton = Rect(ScreenWidth * 5 / 38, ScreenHeight * 7 / 10 + 40, 1000, 150)
        ConfirmButton = Rect(ScreenWidth * 27 / 38, ScreenHeight / 3 - 40, 400, 400)
        EyeIconButton1 = Rect(ScreenWidth / 80, ScreenHeight / 2 - 20, 220, 180)
        EyeIconButton2 = Rect(ScreenWidth / 80, ScreenHeight * 7 / 10 - 20, 220, 180)
        BackButton = Rect(ScreenWidth * 6 / 7, ScreenHeight * 1 / 30, 180, 180)
        LoginInput = ""
        PasswordInput = ""
        RepeatPasswordInput = ""
        NicknameInput = ""
        password_show = False
        repeat_password_show = False
        active = 0
        while True:
            ErrorMessage = ''
            error_message_show = False
            SuccessMessage = ''
            success_message_show = False
            screen.fill(RegistrationBackgroundColor)
            for event in pygame.event.get():
                if event.type == QUIT:
                    ReturnToMenu = 1
                if event.type == MOUSEBUTTONDOWN:
                    MousePosition = pygame.mouse.get_pos()
                    if LoginButton.collidepoint(MousePosition):
                        active = 1
                    elif NicknameButton.collidepoint(MousePosition):
                        active = 2
                    elif PasswordButton.collidepoint(MousePosition):
                        active = 3
                    elif RepeatPasswordButton.collidepoint(MousePosition):
                        active = 4
                    elif ConfirmButton.collidepoint(MousePosition):
                        RegisterSuccess = DataBaseRequester.register_user(LoginInput, NicknameInput, PasswordInput,
                                                                          RepeatPasswordInput)
                        print(RegisterSuccess)
                        if RegisterSuccess.info == "Пользователь добавлен":
                            SuccessMessage = RegisterSuccess.info
                            success_message_show = True
                        else:
                            ErrorMessage = RegisterSuccess.info
                            error_message_show = True
                        active = 0
                    elif EyeIconButton1.collidepoint(MousePosition):
                        password_show = not password_show
                    elif EyeIconButton2.collidepoint(MousePosition):
                        repeat_password_show = not repeat_password_show
                    elif BackButton.collidepoint(MousePosition):
                        ReturnToMenu = 1
                        active = 0
                    else:
                        active = 0
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        active += 1 * (active < 4)
                    elif event.key == K_UP:
                        active -= 1 * (active > 1)
                    else:
                        if active == 1:
                            if event.key == K_BACKSPACE:
                                LoginInput = LoginInput[:-1]
                            elif event.key == K_RETURN:
                                active = 2
                            elif len(LoginInput) < MaxLoginLength:
                                LoginInput += event.unicode
                        elif active == 2:
                            if event.key == K_BACKSPACE:
                                NicknameInput = NicknameInput[:-1]
                            elif event.key == K_RETURN:
                                active = 3
                            elif len(NicknameInput) < MaxPasswordLength:
                                NicknameInput += event.unicode
                        elif active == 3:
                            if event.key == K_BACKSPACE:
                                PasswordInput = PasswordInput[:-1]
                            elif event.key == K_RETURN:
                                active = 4
                            elif len(PasswordInput) < MaxPasswordLength:
                                PasswordInput += event.unicode
                        elif active == 4:
                            if event.key == K_BACKSPACE:
                                RepeatPasswordInput = RepeatPasswordInput[:-1]
                            elif event.key == K_RETURN:
                                active = 0
                            elif len(RepeatPasswordInput) < MaxPasswordLength:
                                RepeatPasswordInput += event.unicode
                        if active == 0:
                            if event.key == K_RETURN:
                                RegisterSuccess = DataBaseRequester.register_user(LoginInput, NicknameInput,
                                                                                  PasswordInput,
                                                                                  RepeatPasswordInput)
                                print(RegisterSuccess)
                                if RegisterSuccess.info == "Пользователь добавлен":
                                    SuccessMessage = RegisterSuccess.info
                                    success_message_show = True
                                else:
                                    ErrorMessage = RegisterSuccess.info
                                    error_message_show = True

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_ESCAPE]:
                ReturnToMenu = 1

            pygame.draw.rect(screen, RegistrationButtonColor, LoginButton)
            pygame.draw.rect(screen, RegistrationButtonColor, NicknameButton)
            pygame.draw.rect(screen, RegistrationButtonColor, PasswordButton)
            pygame.draw.rect(screen, RegistrationButtonColor, RepeatPasswordButton)
            pygame.draw.rect(screen, RegistrationButtonColor, ConfirmButton)
            screen.blit(LoginText, (LoginButton.midtop[0] - 100, LoginButton.midtop[1] - 80))
            screen.blit(NicknameText, (NicknameButton.midtop[0] - 80, NicknameButton.midtop[1] - 60))
            screen.blit(PassowrdText, (PasswordButton.midtop[0] - 120, PasswordButton.midtop[1] - 60))
            screen.blit(RepeatPasswordText, (RepeatPasswordButton.midtop[0] - 220, RepeatPasswordButton.midtop[1] - 60))
            screen.blit(ConfirmText, (ConfirmButton.center[0] - 180, ConfirmButton.center[1] - 20))

            LoginInputText = RegistrationFont.render(LoginInput + (active == 1) * '|', False, (0, 0, 0))
            NicknameInputText = RegistrationFont.render(NicknameInput + (active == 2) * '|', False, (0, 0, 0))
            screen.blit(LoginInputText, (LoginButton.left, LoginButton.center[1] - 35))
            screen.blit(NicknameInputText, (NicknameButton.left, NicknameButton.center[1] - 35))

            if password_show:
                EyeIconImage = pygame.image.load("src/img/EyeIcon.png").convert_alpha()
                screen.blit(pygame.transform.scale(EyeIconImage, (220, 180)),
                            (ScreenWidth / 80, ScreenHeight / 2 + 10))
                PassowrdInputText = RegistrationFont.render(PasswordInput + (active == 3) * '|', False, (0, 0, 0))
                screen.blit(PassowrdInputText, (PasswordButton.left, PasswordButton.center[1] - 35))
            else:
                EyeIconImage = pygame.image.load("src/img/EyeIconCrossed.png").convert_alpha()
                screen.blit(pygame.transform.scale(EyeIconImage, (250, 160)),
                            (ScreenWidth / 80 - 10, ScreenHeight / 2 + 20))
                PassowrdInputText = RegistrationFont.render('*' * len(PasswordInput) + (active == 3) * '|', False,
                                                            (0, 0, 0))
                screen.blit(PassowrdInputText, (PasswordButton.left, PasswordButton.center[1] - 10))

            if repeat_password_show:
                EyeIconImage = pygame.image.load("src/img/EyeIcon.png").convert_alpha()
                screen.blit(pygame.transform.scale(EyeIconImage, (220, 180)),
                            (ScreenWidth / 80, ScreenHeight * 7 / 10 + 20))
                RepeatPassowrdInputText = RegistrationFont.render(RepeatPasswordInput + (active == 4) * '|', False,
                                                                  (0, 0, 0))
                screen.blit(RepeatPassowrdInputText, (RepeatPasswordButton.left, RepeatPasswordButton.center[1] - 35))
            else:
                EyeIconImage = pygame.image.load("src/img/EyeIconCrossed.png").convert_alpha()
                screen.blit(pygame.transform.scale(EyeIconImage, (250, 160)),
                            (ScreenWidth / 80 - 10, ScreenHeight * 7 / 10 + 30))
                RepeatPassowrdInputText = RegistrationFont.render('*' * len(RepeatPasswordInput) + (active == 4) * '|',
                                                                  False, (0, 0, 0))
                screen.blit(RepeatPassowrdInputText, (RepeatPasswordButton.left, RepeatPasswordButton.center[1] - 10))

            BackIconImage = pygame.image.load("src/img/BackIcon.png").convert_alpha()
            screen.blit(pygame.transform.scale(BackIconImage, (180, 180)),
                        (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))
            if error_message_show:
                self.message_show(ErrorMessage)
                pygame.display.update()
                time.sleep(2.5)
            elif success_message_show:
                self.message_show(SuccessMessage)
                ReturnToMenu = 1
                pygame.display.update()
                time.sleep(2)
            else:
                pygame.display.update()

            if ReturnToMenu == 1:
                return "menu"

    def show_start_menu(self, DataBaseRequester):
        while True:
            screen.fill(RegistrationBackgroundColor)
            EnterButton = Rect(ScreenWidth * 11 / 38, ScreenHeight / 6, 800, 250)
            RegistrationButton = Rect(ScreenWidth * 11 / 38, ScreenHeight / 2, 800, 250)
            BackButton = Rect(ScreenWidth * 6 / 7, ScreenHeight * 1 / 30, 180, 180)
            ReturnType = "empty"
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if EnterButton.collidepoint(pygame.mouse.get_pos()):
                        ReturnType = self.show_enter_menu(DataBaseRequester)
                    elif RegistrationButton.collidepoint(pygame.mouse.get_pos()):
                        ReturnType = self.show_resgistration_menu(DataBaseRequester)
                    elif BackButton.collidepoint(pygame.mouse.get_pos()):
                        sys.exit()

            if ReturnType == "menu":
                time.sleep(0.08)
                continue
            elif ReturnType != "empty":
                return ReturnType
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_ESCAPE]:
                sys.exit()
            pygame.draw.rect(screen, RegistrationButtonColor, EnterButton)
            pygame.draw.rect(screen, RegistrationButtonColor, RegistrationButton)
            BackIconImage = pygame.image.load("src/img/BackIcon.png").convert_alpha()
            screen.blit(pygame.transform.scale(BackIconImage, (180, 180)),
                        (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))
            EnterText = RegistrationFont.render("Войти", False, (0, 0, 0))
            RegistrationText = RegistrationFont.render("Зарегестрироваться", False, (0, 0, 0))
            screen.blit(EnterText, (EnterButton.center[0] - 85, EnterButton.center[1] - 40))
            screen.blit(RegistrationText, (RegistrationButton.center[0] - 285, RegistrationButton.center[1] - 40))
            pygame.display.update()

    def show_ingame_menu(self, DataBaseRequester):
        JoinGameButton = Rect(ScreenWidth * 10 / 38, ScreenHeight / 20 + 40, 850, 200)
        CreateGameButton = Rect(ScreenWidth * 10 / 38, ScreenHeight / 4 + 40, 850, 200)
        SettingsButton = Rect(ScreenWidth * 10 / 38, ScreenHeight * 4 / 9 + 45, 850, 200)
        RankingsButton = Rect(ScreenWidth * 10 / 38, ScreenHeight * 2 / 3 + 25, 850, 200)
        BackButton = Rect(ScreenWidth * 6 / 7, ScreenHeight * 1 / 30, 180, 180)
        GameStart = False
        while True:
            screen.fill(RegistrationBackgroundColor)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if JoinGameButton.collidepoint(pygame.mouse.get_pos()):
                        GameStart = True
                    elif BackButton.collidepoint(pygame.mouse.get_pos()):
                        sys.exit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_ESCAPE]:
                sys.exit()
            pygame.draw.rect(screen, RegistrationButtonColor, JoinGameButton)
            pygame.draw.rect(screen, RegistrationButtonColor, CreateGameButton)
            pygame.draw.rect(screen, RegistrationButtonColor, SettingsButton)
            pygame.draw.rect(screen, RegistrationButtonColor, RankingsButton)
            JoinGameText = RegistrationFont.render("Присоединиться к игре", False, (0, 0, 0))
            CreateGameText = RegistrationFont.render("Создать игру", False, (0, 0, 0))
            SettingsText = RegistrationFont.render("Настройки", False, (0, 0, 0))
            RankingsText = RegistrationFont.render("Списки лидеров", False, (0, 0, 0))
            screen.blit(JoinGameText, (JoinGameButton.center[0] - 325, JoinGameButton.center[1] - 35))
            screen.blit(CreateGameText, (CreateGameButton.center[0] - 185, CreateGameButton.center[1] - 35))
            screen.blit(SettingsText, (SettingsButton.center[0] - 150, SettingsButton.center[1] - 35))
            screen.blit(RankingsText, (RankingsButton.center[0] - 230, RankingsButton.center[1] - 35))
            BackIconImage = pygame.image.load("src/img/BackIcon.png").convert_alpha()
            screen.blit(pygame.transform.scale(BackIconImage, (180, 180)),
                        (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))
            pygame.display.update()
            if GameStart:
                return "gameplay"

    def message_show(self, message):
        MessageRect = Rect(ScreenWidth / 2 - (100 + len(message) * 15), ScreenHeight / 4 + 50,
                           220 + len(message) * 30, 350)
        pygame.draw.rect(screen, MessageBackgroundColor, MessageRect)
        MessageText = RegistrationFont.render(message, False, (0, 0, 0))
        screen.blit(MessageText,
                    (MessageRect.center[0] - (10 + len(message) * 15), MessageRect.center[1] - 40))
