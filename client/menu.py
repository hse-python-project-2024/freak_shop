from interface_setup import *
import enum


class ReturnStatus(enum.Enum):
    stay = 0
    quit = 1
    register = 2
    login = 3
    go_to_login = 4
    go_to_register = 5
    start_game = 6
    settings = 7
    leaderboard = 8
    change_lang = 9
    join_lobby = 10
    create_lobby = 11
    go_to_join_lobby = 12
    change_readiness = 13


class MenuView:
    def __init__(self, language):
        self.CodeText = None
        self.ReadyText = None
        self.LanguageSettingText = None
        self.RegistrationTextInitial = None
        self.BackButton = None
        self.JoinGameText = None
        self.CreateGameText = None
        self.SettingsText = None
        self.RankingsText = None
        self.LoginTextInitial = None
        self.ConfirmTextRegistration = None
        self.ConfirmTextLogin = None
        self.PasswordText = None
        self.NicknameText = None
        self.LoginText = None
        self.RepeatPasswordText = None

        self.RuText = RegistrationFont.render(RuText, False, (0, 0, 0))
        self.EnText = RegistrationFont.render(EnText, False, (0, 0, 0))

        self.lang = language
        self.change_menu_language(self.lang)

        # Buttons for Initial Menu
        self.EnterButtonInitial = Rect(ScreenWidth * 11 / 38, ScreenHeight / 6, 800, 250)
        self.RegistrationButtonInitial = Rect(ScreenWidth * 11 / 38, ScreenHeight / 2, 800, 250)
        self.BackButtonInitial = Rect(ScreenWidth * 6 / 7, ScreenHeight * 1 / 30, 180, 180)

        # Buttons for Login Menu
        self.LoginButtonLogin = Rect(ScreenWidth * 5 / 38, ScreenHeight / 5, 1000, 150)
        self.PasswordButtonLogin = Rect(ScreenWidth * 5 / 38, ScreenHeight * 6 / 10, 1000, 150)
        self.ConfirmButtonLogin = Rect(ScreenWidth * 27 / 38, ScreenHeight / 3 - 40, 400, 400)
        self.EyeIconButtonLogin = Rect(ScreenWidth / 80, ScreenHeight * 6 / 10 - 20, 220, 180)

        # Buttons for Registration Menu
        self.LoginButtonRegistration = Rect(ScreenWidth * 5 / 38, ScreenHeight / 12 + 20, 1000, 150)
        self.NicknameButtonRegistration = Rect(ScreenWidth * 5 / 38, ScreenHeight / 4 + 60, 1000, 150)
        self.PasswordButtonRegistration = Rect(ScreenWidth * 5 / 38, ScreenHeight / 2 + 20, 1000, 150)
        self.RepeatPasswordButtonRegistration = Rect(ScreenWidth * 5 / 38, ScreenHeight * 7 / 10 + 40, 1000, 150)
        self.ConfirmButtonRegistration = Rect(ScreenWidth * 27 / 38, ScreenHeight / 3 - 40, 400, 400)
        self.EyeIconButton1 = Rect(ScreenWidth / 80, ScreenHeight / 2 - 20, 220, 180)
        self.EyeIconButton2 = Rect(ScreenWidth / 80, ScreenHeight * 7 / 10 - 20, 220, 180)

        # Buttons for Main Menu
        self.JoinGameButton = Rect(ScreenWidth * 10 / 38, ScreenHeight / 20 + 40, 850, 200)
        self.CreateGameButton = Rect(ScreenWidth * 10 / 38, ScreenHeight / 4 + 40, 850, 200)
        self.SettingsButton = Rect(ScreenWidth * 10 / 38, ScreenHeight * 4 / 9 + 45, 850, 200)
        self.RankingsButton = Rect(ScreenWidth * 10 / 38, ScreenHeight * 2 / 3 + 25, 850, 200)

        # Buttons for Settings Menu
        self.RuButton = Rect(ScreenWidth * 10 / 38, ScreenHeight * 1 / 5, 350, 200)
        self.EnButton = Rect(ScreenWidth * 20 / 38, ScreenHeight * 1 / 5, 350, 200)

        # Buttons for Lobby
        self.ReadyButton = Rect(ScreenWidth * 14 / 38, ScreenHeight * 4 / 5 + 50, 450, 100)

        # Buttons for Join_By_Code
        self.CodeConfirmButton = Rect(ScreenWidth * 14 / 38, ScreenHeight * 3 / 5 - 50, 450, 100)
        self.CodeButton = Rect(ScreenWidth * 10 / 38, ScreenHeight / 4 + 40, 850, 200)

        # Images of password show|hide
        self.BackIconImage = pygame.image.load("src/img/BackIcon.png").convert_alpha()
        self.EyeIconImage = pygame.image.load("src/img/EyeIcon.png").convert_alpha()
        self.EyeIconImageCrossed = pygame.image.load("src/img/EyeIconCrossed.png").convert_alpha()

        # Icons for the Lobby
        self.PlayerIcon = pygame.transform.scale(pygame.image.load("src/img/Player_Icon.png").convert_alpha(),
                                                 (180, 180))
        self.JoinedPlayerCard = (pygame.transform.scale(pygame.image.load("src/img/Joined_Player_Icon.png").convert(),
                                                        (240, 320)))
        self.ReadiedUpIconDeactivated = pygame.transform.scale(
            pygame.image.load("src/img/End_Turn_Icon.png").convert_alpha(),
            (200, 200))
        self.ReadiedUpIconActivated = pygame.transform.scale(
            pygame.image.load("src/img/End_Turn_Icon_Activated.png").convert_alpha(),
            (200, 200))

        # Variables for registration/login
        self.LoginInput = ""
        self.PasswordInput = ""
        self.RepeatPasswordInput = ""
        self.NicknameInput = ""
        self.password_show = False
        self.repeat_password_show = False

        # Variables for joining by code
        self.CodeInput = ""
        self.active = 0

    def reset_menu_info(self):
        self.LoginInput = ""
        self.PasswordInput = ""
        self.RepeatPasswordInput = ""
        self.NicknameInput = ""
        self.active = 0
        self.password_show = False
        self.repeat_password_show = False
        self.CodeInput = ""

        # Changing the language of all menus

    def change_menu_language(self, new_language):
        new_lang = new_language.value  # We actually need the value to iterate through strings
        self.lang = new_language
        self.LoginText = RegistrationFont.render(LoginTexts[new_lang], False, (0, 0, 0))
        self.NicknameText = RegistrationFont.render(NicknameTexts[new_lang], False, (0, 0, 0))
        self.PasswordText = RegistrationFont.render(PasswordTexts[new_lang], False, (0, 0, 0))
        self.RepeatPasswordText = RegistrationFont.render(RepeatPasswordTexts[new_lang], False, (0, 0, 0))
        self.ConfirmTextLogin = RegistrationFont.render(ConfirmTexts[new_lang], False, (0, 0, 0))
        self.ConfirmTextRegistration = RegistrationFont.render(RegistrationTexts[new_lang], False, (0, 0, 0))

        self.LoginTextInitial = RegistrationFont.render(ConfirmTexts[new_lang], False, (0, 0, 0))
        self.RegistrationTextInitial = RegistrationFont.render(InitialRegistrationTexts[new_lang], False, (0, 0, 0))
        self.BackButton = Rect(ScreenWidth * 6 / 7, ScreenHeight * 1 / 30, 180, 180)

        self.JoinGameText = RegistrationFont.render(JoinGameTexts[new_lang], False, (0, 0, 0))
        self.CreateGameText = RegistrationFont.render(CreateGameTexts[new_lang], False, (0, 0, 0))
        self.SettingsText = RegistrationFont.render(SettingsTexts[new_lang], False, (0, 0, 0))
        self.RankingsText = RegistrationFont.render(LeaderbordTexts[new_lang], False, (0, 0, 0))

        self.CodeText = RegistrationFont.render(GameCodeTexts[new_lang], False, (0, 0, 0))

        self.LanguageSettingText = RegistrationFont.render(LanguageSettingsTexts[new_lang], False, (0, 0, 0))

        self.ReadyText = RegistrationFont.render(ReadyTexts[new_lang], False, (0, 0, 0))

    def show_login_menu(self):
        screen.fill(RegistrationBackgroundColor)
        for event in pygame.event.get():
            if event.type == QUIT:
                Returnee = [ReturnStatus.quit, [""]]
                return Returnee
            if event.type == MOUSEBUTTONDOWN:
                MousePosition = pygame.mouse.get_pos()
                if self.LoginButtonLogin.collidepoint(MousePosition):
                    self.active = 1
                elif self.PasswordButtonLogin.collidepoint(MousePosition):
                    self.active = 2
                elif self.ConfirmButtonLogin.collidepoint(MousePosition):
                    self.active = 0
                    Returnee = [ReturnStatus.login, [self.LoginInput, self.PasswordInput]]
                    return Returnee
                elif self.EyeIconButtonLogin.collidepoint(MousePosition):
                    self.password_show = not self.password_show
                elif self.BackButton.collidepoint(MousePosition):
                    Returnee = [ReturnStatus.quit, [""]]
                    return Returnee
                else:
                    self.active = 0
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Returnee = [ReturnStatus.quit, [""]]
                    return Returnee
                elif event.key == K_DOWN:
                    self.active += 1 * (self.active < 2)
                elif event.key == K_UP:
                    self.active -= 1 * (self.active > 1)
                else:
                    if self.active == 1:
                        if event.key == K_BACKSPACE:
                            self.LoginInput = self.LoginInput[:-1]
                        elif event.key == K_RETURN:
                            self.active = 2
                        elif len(self.LoginInput) < MaxLoginLength:
                            self.LoginInput += event.unicode
                    elif self.active == 2:
                        if event.key == K_BACKSPACE:
                            self.PasswordInput = self.PasswordInput[:-1]
                        elif event.key == K_RETURN:
                            self.active = 0
                        elif len(self.PasswordInput) < MaxPasswordLength:
                            self.PasswordInput += event.unicode
                    if self.active == 0:
                        if event.key == K_RETURN:
                            Returnee = [ReturnStatus.login, [self.LoginInput, self.PasswordInput]]
                            return Returnee

        pygame.draw.rect(screen, RegistrationButtonColor, self.LoginButtonLogin)
        pygame.draw.rect(screen, RegistrationButtonColor, self.PasswordButtonLogin)
        pygame.draw.rect(screen, RegistrationButtonColor, self.ConfirmButtonLogin)
        screen.blit(self.LoginText, (self.LoginButtonLogin.midtop[0] - 100, self.LoginButtonLogin.midtop[1] - 80))
        screen.blit(self.PasswordText,
                    (self.PasswordButtonLogin.midtop[0] - 120, self.PasswordButtonLogin.midtop[1] - 80))
        screen.blit(self.ConfirmTextLogin,
                    (self.ConfirmButtonLogin.center[0] - 85, self.ConfirmButtonLogin.center[1] - 30))

        LoginInputText = RegistrationFont.render(self.LoginInput + (self.active == 1) * '|', False, (0, 0, 0))
        screen.blit(LoginInputText, (self.LoginButtonLogin.left, self.LoginButtonLogin.center[1] - 35))

        if self.password_show:
            screen.blit(pygame.transform.scale(self.EyeIconImage, (220, 180)),
                        (ScreenWidth / 80, ScreenHeight * 6 / 10 - 20))
            PasswordInputText = RegistrationFont.render(self.PasswordInput + (self.active == 2) * '|', False, (0, 0, 0))
            screen.blit(PasswordInputText, (self.PasswordButtonLogin.left, self.PasswordButtonLogin.center[1] - 35))
        else:
            screen.blit(pygame.transform.scale(self.EyeIconImageCrossed, (250, 160)),
                        (ScreenWidth / 80 - 10, ScreenHeight * 6 / 10 - 10))
            PasswordInputText = RegistrationFont.render('*' * len(self.PasswordInput) + (self.active == 2) * '|', False,
                                                        (0, 0, 0))
            screen.blit(PasswordInputText, (self.PasswordButtonLogin.left, self.PasswordButtonLogin.center[1] - 10))
        screen.blit(pygame.transform.scale(self.BackIconImage, (180, 180)),
                    (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))

        Returnee = [ReturnStatus.stay, [""]]
        return Returnee

    def show_registration_menu(self):
        screen.fill(RegistrationBackgroundColor)
        for event in pygame.event.get():
            if event.type == QUIT:
                Returnee = [ReturnStatus.quit, [""]]
                return Returnee
            if event.type == MOUSEBUTTONDOWN:
                MousePosition = pygame.mouse.get_pos()
                if self.LoginButtonRegistration.collidepoint(MousePosition):
                    self.active = 1
                elif self.NicknameButtonRegistration.collidepoint(MousePosition):
                    self.active = 2
                elif self.PasswordButtonRegistration.collidepoint(MousePosition):
                    self.active = 3
                elif self.RepeatPasswordButtonRegistration.collidepoint(MousePosition):
                    self.active = 4
                elif self.ConfirmButtonRegistration.collidepoint(MousePosition):
                    Returnee = [ReturnStatus.register, [self.LoginInput, self.NicknameInput, self.PasswordInput,
                                                        self.RepeatPasswordInput]]
                    return Returnee
                elif self.EyeIconButton1.collidepoint(MousePosition):
                    self.password_show = not self.password_show
                elif self.EyeIconButton2.collidepoint(MousePosition):
                    self.repeat_password_show = not self.repeat_password_show
                elif self.BackButton.collidepoint(MousePosition):
                    Returnee = [ReturnStatus.quit, [""]]
                    return Returnee
                else:
                    self.active = 0
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Returnee = [ReturnStatus.quit, [""]]
                    return Returnee
                elif event.key == K_DOWN:
                    self.active += 1 * (self.active < 4)
                elif event.key == K_UP:
                    self.active -= 1 * (self.active > 1)
                else:
                    if self.active == 1:
                        if event.key == K_BACKSPACE:
                            self.LoginInput = self.LoginInput[:-1]
                        elif event.key == K_RETURN:
                            self.active = 2
                        elif len(self.LoginInput) < MaxLoginLength:
                            self.LoginInput += event.unicode
                    elif self.active == 2:
                        if event.key == K_BACKSPACE:
                            self.NicknameInput = self.NicknameInput[:-1]
                        elif event.key == K_RETURN:
                            self.active = 3
                        elif len(self.NicknameInput) < MaxPasswordLength:
                            self.NicknameInput += event.unicode
                    elif self.active == 3:
                        if event.key == K_BACKSPACE:
                            self.PasswordInput = self.PasswordInput[:-1]
                        elif event.key == K_RETURN:
                            self.active = 4
                        elif len(self.PasswordInput) < MaxPasswordLength:
                            self.PasswordInput += event.unicode
                    elif self.active == 4:
                        if event.key == K_BACKSPACE:
                            self.RepeatPasswordInput = self.RepeatPasswordInput[:-1]
                        elif event.key == K_RETURN:
                            self.active = 0
                        elif len(self.RepeatPasswordInput) < MaxPasswordLength:
                            self.RepeatPasswordInput += event.unicode
                    if self.active == 0:
                        if event.key == K_RETURN:
                            Returnee = [ReturnStatus.register,
                                        [self.LoginInput, self.NicknameInput, self.PasswordInput,
                                         self.RepeatPasswordInput]]
                            return Returnee

        pygame.draw.rect(screen, RegistrationButtonColor, self.LoginButtonRegistration)
        pygame.draw.rect(screen, RegistrationButtonColor, self.NicknameButtonRegistration)
        pygame.draw.rect(screen, RegistrationButtonColor, self.PasswordButtonRegistration)
        pygame.draw.rect(screen, RegistrationButtonColor, self.RepeatPasswordButtonRegistration)
        pygame.draw.rect(screen, RegistrationButtonColor, self.ConfirmButtonRegistration)
        screen.blit(self.LoginText,
                    (self.LoginButtonRegistration.midtop[0] - 100, self.LoginButtonRegistration.midtop[1] - 80))
        screen.blit(self.NicknameText,
                    (self.NicknameButtonRegistration.midtop[0] - 80, self.NicknameButtonRegistration.midtop[1] - 60))
        screen.blit(self.PasswordText,
                    (self.PasswordButtonRegistration.midtop[0] - 120, self.PasswordButtonRegistration.midtop[1] - 60))
        screen.blit(self.RepeatPasswordText, (
            self.RepeatPasswordButtonRegistration.midtop[0] - 220,
            self.RepeatPasswordButtonRegistration.midtop[1] - 60))
        screen.blit(self.ConfirmTextRegistration,
                    (self.ConfirmButtonRegistration.center[0] - 180, self.ConfirmButtonRegistration.center[1] - 20))

        LoginInputText = RegistrationFont.render(self.LoginInput + (self.active == 1) * '|', False, (0, 0, 0))
        NicknameInputText = RegistrationFont.render(self.NicknameInput + (self.active == 2) * '|', False, (0, 0, 0))
        screen.blit(LoginInputText, (self.LoginButtonRegistration.left, self.LoginButtonRegistration.center[1] - 35))
        screen.blit(NicknameInputText,
                    (self.NicknameButtonRegistration.left, self.NicknameButtonRegistration.center[1] - 35))

        if self.password_show:
            screen.blit(pygame.transform.scale(self.EyeIconImage, (220, 180)),
                        (ScreenWidth / 80, ScreenHeight / 2 + 10))
            PasswordInputText = RegistrationFont.render(self.PasswordInput + (self.active == 3) * '|', False, (0, 0, 0))
            screen.blit(PasswordInputText,
                        (self.PasswordButtonRegistration.left, self.PasswordButtonRegistration.center[1] - 35))
        else:
            screen.blit(pygame.transform.scale(self.EyeIconImageCrossed, (250, 160)),
                        (ScreenWidth / 80 - 10, ScreenHeight / 2 + 20))
            PasswordInputText = RegistrationFont.render('*' * len(self.PasswordInput) + (self.active == 3) * '|', False,
                                                        (0, 0, 0))
            screen.blit(PasswordInputText,
                        (self.PasswordButtonRegistration.left, self.PasswordButtonRegistration.center[1] - 10))

        if self.repeat_password_show:
            screen.blit(pygame.transform.scale(self.EyeIconImage, (220, 180)),
                        (ScreenWidth / 80, ScreenHeight * 7 / 10 + 20))
            RepeatPasswordInputText = RegistrationFont.render(self.RepeatPasswordInput + (self.active == 4) * '|',
                                                              False,
                                                              (0, 0, 0))
            screen.blit(RepeatPasswordInputText, (
                self.RepeatPasswordButtonRegistration.left, self.RepeatPasswordButtonRegistration.center[1] - 35))
        else:
            screen.blit(pygame.transform.scale(self.EyeIconImageCrossed, (250, 160)),
                        (ScreenWidth / 80 - 10, ScreenHeight * 7 / 10 + 30))
            RepeatPasswordInputText = RegistrationFont.render(
                '*' * len(self.RepeatPasswordInput) + (self.active == 4) * '|',
                False, (0, 0, 0))
            screen.blit(RepeatPasswordInputText, (
                self.RepeatPasswordButtonRegistration.left, self.RepeatPasswordButtonRegistration.center[1] - 10))
        screen.blit(pygame.transform.scale(self.BackIconImage, (180, 180)),
                    (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))

        Returnee = [ReturnStatus.stay, [""]]
        return Returnee

    def show_initial_menu(self):
        screen.fill(RegistrationBackgroundColor)
        for event in pygame.event.get():
            if event.type == QUIT:
                Returnee = [ReturnStatus.quit, [""]]
                return Returnee
            if event.type == MOUSEBUTTONDOWN:
                if self.EnterButtonInitial.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.go_to_login, [""]]
                    return Returnee
                elif self.RegistrationButtonInitial.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.go_to_register, [""]]
                    return Returnee
                elif self.BackButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.quit, [""]]
                    return Returnee
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            Returnee = [ReturnStatus.quit, [""]]
            return Returnee
        pygame.draw.rect(screen, RegistrationButtonColor, self.EnterButtonInitial)
        pygame.draw.rect(screen, RegistrationButtonColor, self.RegistrationButtonInitial)
        screen.blit(pygame.transform.scale(self.BackIconImage, (180, 180)),
                    (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))
        screen.blit(self.LoginTextInitial,
                    (self.EnterButtonInitial.center[0] - 85, self.EnterButtonInitial.center[1] - 40))
        screen.blit(self.RegistrationTextInitial,
                    (self.RegistrationButtonInitial.center[0] - 285, self.RegistrationButtonInitial.center[1] - 40))

        Returnee = [ReturnStatus.stay, [""]]
        return Returnee

    def show_main_menu(self):
        screen.fill(RegistrationBackgroundColor)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.JoinGameButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.go_to_join_lobby, [""]]
                    return Returnee
                elif self.CreateGameButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.create_lobby, [""]]
                    return Returnee
                elif self.BackButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.quit, [""]]
                    return Returnee
                elif self.SettingsButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.settings, [""]]
                    return Returnee
                elif self.RankingsButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.leaderboard, [""]]
                    return Returnee
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            sys.exit()
        pygame.draw.rect(screen, RegistrationButtonColor, self.JoinGameButton)
        pygame.draw.rect(screen, RegistrationButtonColor, self.CreateGameButton)
        pygame.draw.rect(screen, RegistrationButtonColor, self.SettingsButton)
        pygame.draw.rect(screen, RegistrationButtonColor, self.RankingsButton)
        screen.blit(self.JoinGameText, (self.JoinGameButton.center[0] - 325, self.JoinGameButton.center[1] - 35))
        screen.blit(self.CreateGameText, (self.CreateGameButton.center[0] - 185, self.CreateGameButton.center[1] - 35))
        screen.blit(self.SettingsText, (self.SettingsButton.center[0] - 150, self.SettingsButton.center[1] - 35))
        screen.blit(self.RankingsText, (self.RankingsButton.center[0] - 230, self.RankingsButton.center[1] - 35))
        screen.blit(pygame.transform.scale(self.BackIconImage, (180, 180)),
                    (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))
        Returnee = [ReturnStatus.stay, [""]]
        return Returnee

    def show_settings_menu(self):
        screen.fill(RegistrationBackgroundColor)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.RuButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.change_lang, ["ru"]]
                    return Returnee
                elif self.EnButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.change_lang, ["en"]]
                    return Returnee
                elif self.BackButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.quit, [""]]
                    return Returnee
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            Returnee = [ReturnStatus.quit, [""]]
            return Returnee
        pygame.draw.rect(screen, RegistrationButtonColor, self.RuButton)
        pygame.draw.rect(screen, RegistrationButtonColor, self.EnButton)
        screen.blit(self.RuText, (self.RuButton.center[0] - 35, self.RuButton.center[1] - 25))
        screen.blit(self.EnText, (self.EnButton.center[0] - 35, self.EnButton.center[1] - 25))
        screen.blit(self.LanguageSettingText, (self.RuButton.center[0] + 110, self.RuButton.center[1] - 200))
        screen.blit(pygame.transform.scale(self.BackIconImage, (180, 180)),
                    (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))
        Returnee = [ReturnStatus.stay, [""]]
        return Returnee

    def show_join_by_code_menu(self):
        screen.fill(RegistrationBackgroundColor)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                MousePosition = pygame.mouse.get_pos()
                if self.CodeButton.collidepoint(MousePosition):
                    self.active = 1
                elif self.CodeConfirmButton.collidepoint(MousePosition):
                    self.active = 0
                    Returnee = [ReturnStatus.join_lobby, [int(self.CodeInput)]]
                    return Returnee
                elif self.BackButton.collidepoint(MousePosition):
                    Returnee = [ReturnStatus.quit, [""]]
                    return Returnee
                elif self.CodeConfirmButton.collidepoint(MousePosition):
                    Returnee = [ReturnStatus.join_lobby, [int(self.CodeInput)]]
                    return Returnee
                else:
                    self.active = 0
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Returnee = [ReturnStatus.quit, [""]]
                    return Returnee
                else:
                    if self.active == 1:
                        if event.key == K_BACKSPACE:
                            self.CodeInput = self.CodeInput[:-1]
                        elif event.key == K_RETURN:
                            Returnee = [ReturnStatus.join_lobby, [int(self.CodeInput)]]
                            return Returnee
                        elif len(self.CodeInput) < MaxLoginLength:
                            if event.unicode.isnumeric():
                                self.CodeInput += event.unicode
                    if self.active == 0:
                        if event.key == K_RETURN:
                            Returnee = [ReturnStatus.join_lobby, [int(self.CodeInput)]]
                            return Returnee
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            Returnee = [ReturnStatus.quit, [""]]
            return Returnee
        screen.blit(self.CodeText, (ScreenWidth / 2 - 150, ScreenHeight/10))
        screen.blit(pygame.transform.scale(self.BackIconImage, (180, 180)),
                    (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))
        pygame.draw.rect(screen, RegistrationButtonColor, self.CodeButton)
        CodeInputText = CodeFont.render(self.CodeInput + (self.active == 1) * '|', False, (0, 0, 0))
        screen.blit(CodeInputText, (self.CodeButton.left, self.CodeButton.center[1] - 35))
        pygame.draw.rect(screen, RegistrationButtonColor, self.CodeConfirmButton)
        screen.blit(self.ConfirmTextLogin,
                    (self.CodeConfirmButton.midtop[0] - 100, self.CodeConfirmButton.midtop[1] + 10))
        Returnee = [ReturnStatus.stay, [""]]
        return Returnee

    # TODO display people who are ready
    def show_lobby(self, player_amount, player_nicknames, player_ready_signes,lobby_code):
        screen.fill(RegistrationBackgroundColor)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.BackButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.quit, [""]]
                    return Returnee
                elif self.ReadyButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.change_readiness, [""]]
                    return Returnee
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            Returnee = [ReturnStatus.quit, [""]]
            return Returnee
        for j in range(5):
            screen.blit(self.PlayerIcon, (50 + ScreenWidth * j / 6, ScreenHeight * 1 / 8))
        for i in range(player_amount):
            PlayerNameText = PlayerNicknameInLobbyFont.render(player_nicknames[i], False, (0, 0, 0))
            screen.blit(PlayerNameText,
                        (ScreenWidth * i / 6 + 139 - len(player_nicknames[i]) * 13, ScreenHeight * 1 / 8 + 180))
            screen.blit(self.JoinedPlayerCard,
                        (ScreenWidth * i / 6 + 30, ScreenHeight * 3 / 7 - 70))
            if (player_ready_signes[i]):
                screen.blit(self.ReadiedUpIconActivated,
                            (ScreenWidth * i / 6 + 50, ScreenHeight * 3 / 5 + 50))
            else:
                screen.blit(self.ReadiedUpIconDeactivated,
                            (ScreenWidth * i / 6 + 50, ScreenHeight * 3 / 5 + 50))
            screen.blit(pygame.transform.scale(self.BackIconImage, (180, 180)),
                        (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))
        pygame.draw.rect(screen, RegistrationButtonColor, self.ReadyButton)
        screen.blit(self.ReadyText,
                    (ScreenWidth * 17 / 38, ScreenHeight * 4 / 5 + 80))
        LobbyCodeText = CodeFont.render(str(lobby_code), False, (0, 0, 0))
        screen.blit(LobbyCodeText,
                    (ScreenWidth * 1 / 2 - 95, ScreenHeight * 1 / 19))
        screen.blit(pygame.transform.scale(self.BackIconImage, (180, 180)),
                    (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))
        Returnee = [ReturnStatus.stay, [""]]
        return Returnee

    def show_leaderboard(self):
        # TODO add the actual leaderboard
        screen.fill(RegistrationBackgroundColor)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.BackButton.collidepoint(pygame.mouse.get_pos()):
                    Returnee = [ReturnStatus.quit, [""]]
                    return Returnee
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            Returnee = [ReturnStatus.quit, [""]]
            return Returnee

        screen.blit(pygame.transform.scale(self.BackIconImage, (180, 180)),
                    (ScreenWidth * 6 / 7, ScreenHeight * 1 / 30))
        Returnee = [ReturnStatus.stay, [""]]
        return Returnee

    def show_message(self, message):
        MessageRect = Rect(ScreenWidth / 2 - (100 + len(message) * 15), ScreenHeight / 4 + 50,
                           220 + len(message) * 30, 350)
        pygame.draw.rect(screen, MessageBackgroundColor, MessageRect)
        MessageText = RegistrationFont.render(message, False, (0, 0, 0))
        screen.blit(MessageText,
                    (MessageRect.center[0] - (10 + len(message) * 15), MessageRect.center[1] - 40))
