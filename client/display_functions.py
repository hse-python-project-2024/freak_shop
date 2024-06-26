from interface_setup import *


class GameBoardView:
    def __init__(self):
        self.ClickedPlayerCards = [0] * 10
        self.ClickedPlayerCardsDiscounted = [0] * 10
        self.ClickedShopCards = [0] * 10
        self.ClickedShopCardsDiscounted = [0] * 10
        self.ShopIcon = pygame.transform.scale(pygame.image.load("src/img/Other_Icons/Shop_Icon.png").convert_alpha(),
                                                 (1700, 1300))
        self.CardImages = []
        for i in range(10):
            self.CardImages.append([])
            for j in range(2):
                CardName = "src/img/"
                if j == 1:
                    CardName += "Discounted_Cards/Discount_Image_"
                else:
                    CardName += "NonDiscounted_Cards/Non_Discount_Image_"
                CardName += str(i + 1)
                CardName += ".png"
                self.CardImages[i].append(pygame.transform.scale(pygame.image.load(CardName).convert(), (140, 200)))
        self.CardImagesSelected = []
        for i in range(10):
            self.CardImagesSelected.append([])
            for j in range(2):
                CardName = "src/img/"
                if j == 1:
                    CardName += "Discounted_Cards/Discount_Image_"
                else:
                    CardName += "NonDiscounted_Cards/Non_Discount_Image_"
                CardName += str(i + 1)
                CardName += "_Selected.png"
                self.CardImagesSelected[i].append(
                    pygame.transform.scale(pygame.image.load(CardName).convert(), (140, 200)))
        self.TaskImages = []
        for i in range(12):
            TaskName = "src/img/Task_Icons/Task_"
            TaskName += str(i + 1)
            TaskName += ".png"
            self.TaskImages.append(pygame.transform.scale(pygame.image.load(TaskName).convert(), (140, 200)))
        self.PlayerIcon = pygame.transform.scale(pygame.image.load("src/img/Other_Icons/Player_Icon.png").convert_alpha(),
                                                 (140, 140))
        self.PlayerIconActive = pygame.transform.scale(
            pygame.image.load("src/img/Other_Icons/Player_Icon_Active.png").convert_alpha(),
            (140, 140))
        self.EndTurnIcon = pygame.transform.scale(pygame.image.load("src/img/Other_Icons/End_Turn_Icon.png").convert_alpha(),
                                                  (250, 250))
        self.EndTurnIconActivated = pygame.transform.scale(
            pygame.image.load("src/img/Other_Icons/End_Turn_Icon_Activated.png").convert_alpha(),
            (250, 250))
        self.BackIcon = pygame.transform.scale(pygame.image.load("src/img/Other_Icons/BackIcon.png").convert_alpha(),
                                                  (200, 200))

    def display_shop_image(self):
        screen.blit(self.ShopIcon, (50, -520))

    def display_main_player_cards(self, CurrentPlayer):
        for i in range(10):
            DisplayedDiscounted = 0
            DisplayedDiscountedSelected = 0
            DisplayedSeclected = 0
            for j in range(CurrentPlayer.CardsInHand[i]):
                ShowDiscount = False
                ShowSelected = False
                if CurrentPlayer.DiscountedCardsInHand[i] > DisplayedDiscounted:
                    DisplayedDiscounted += 1
                    ShowDiscount = True
                    if self.ClickedPlayerCardsDiscounted[i] > DisplayedDiscountedSelected:
                        DisplayedDiscountedSelected += 1
                        ShowSelected = True
                elif self.ClickedPlayerCards[i] > DisplayedSeclected:
                    DisplayedSeclected += 1
                    ShowSelected = True
                if ShowSelected:
                    screen.blit(self.CardImagesSelected[i][ShowDiscount],
                                (ScreenWidth * (1 / 30 + i / 12),
                                 ScreenHeight * (6 / 10 + j / 50) + 20))
                else:
                    screen.blit(self.CardImages[i][ShowDiscount],
                                (ScreenWidth * (1 / 30 + i / 12),
                                 ScreenHeight * (6 / 10 + j / 50) + 20))

    def display_shop_cards(self, CurrentShop):
        for i in range(10):
            DisplayedDiscounted = 0
            DisplayedDiscountedSelected = 0
            DisplayedSeclected = 0
            for j in range(CurrentShop.CardsInShop[i]):
                WidthAdd = i / 8 + 1 / 100
                HeightAdd = 1 / 100
                if i >= 5:
                    WidthAdd = (i - 5) / 8 - 1 / 25 - 1 / 100
                    HeightAdd += 9 / 30
                ShowDiscount = False
                ShowSelected = False
                if CurrentShop.DiscountedCardsInShop[i] > DisplayedDiscounted:
                    DisplayedDiscounted += 1
                    ShowDiscount = True
                    if self.ClickedShopCardsDiscounted[i] > DisplayedDiscountedSelected:
                        DisplayedDiscountedSelected += 1
                        ShowSelected = True
                elif self.ClickedShopCards[i] > DisplayedSeclected:
                    DisplayedSeclected += 1
                    ShowSelected = True
                if ShowSelected:
                    screen.blit(self.CardImagesSelected[i][ShowDiscount], (ScreenWidth * (2 / 10 + WidthAdd) - 80,
                                                                           ScreenHeight * (HeightAdd + j / 50)))
                else:
                    screen.blit(self.CardImages[i][ShowDiscount], (ScreenWidth * (2 / 10 + WidthAdd) - 80,
                                                                   ScreenHeight * (HeightAdd + j / 50)))

    def display_player_list(self, Game, PlayerPosition, lang, CurrentPlayer):
        for i in range(Game.PlayerAmount):
            if i == CurrentPlayer:
                screen.blit(self.PlayerIconActive, (ScreenWidth * 4 / 5 + 80, ScreenHeight * i / 8))
            else:
                screen.blit(self.PlayerIcon, (ScreenWidth * 4 / 5 + 80, ScreenHeight * i / 8))
            if i != PlayerPosition:
                PlayerNameText = TextFont.render(Game.PlayersNicknames[i], False, (0, 0, 0))
            else:
                PlayerNameText = TextFont.render(YouTexts[lang.value], False, (0, 0, 0))
            screen.blit(PlayerNameText, (ScreenWidth * 4 / 5 + 230, ScreenHeight * i / 8 + 60))

    def display_scores(self, Game):
        for i in range(len(Game.Scores)):
            ScoreText = ScoresFont.render(str(Game.Scores[i]), False, (0, 0, 0))
            screen.blit(ScoreText, (ScreenWidth * 4 / 5, ScreenHeight * i / 8 + 40))

    def display_end_turn_button(self, activated, lang):
        EndTurnText = TextFont.render(EndTurnTexts[lang.value], False, (0, 0, 0))
        screen.blit(EndTurnText, (ScreenWidth * 6 / 7 + 15, ScreenHeight * 3 / 4 - 40))
        if activated:
            screen.blit(self.EndTurnIconActivated,
                        (ScreenWidth * 6 / 7 + 20, ScreenHeight * 3 / 4 - 30))
        else:
            screen.blit(self.EndTurnIcon, (ScreenWidth * 6 / 7 + 20, ScreenHeight * 3 / 4 - 30))

    def display_back_button(self):
        screen.blit(self.BackIcon, (ScreenWidth * 6 / 7 + 20, ScreenHeight * 3 / 4 - 30))

    def display_task_list(self, Game):
        ind = 0
        TaskImagesRects = [Rect(0, 0, 0, 0), Rect(0, 0, 0, 0), Rect(0, 0, 0, 0)]
        for TaskNumber in Game.Tasks:
            TaskImagesRects[ind] = Rect(ScreenWidth / 50, ScreenHeight * ind / 5 + 10, 140,
                                        200)
            screen.blit(self.TaskImages[TaskNumber], (ScreenWidth / 50,
                                                          ScreenHeight * ind / 5 + 10))
            ind += 1
        return TaskImagesRects

    def display_tasks_text(self, Tasks, TaskNumber, lang):
        for j in range(len(Task_Descriptions[lang.value][Tasks[TaskNumber]])):
            TaskDescriptionText = TaskFont.render(Task_Descriptions[lang.value][Tasks[TaskNumber]][j], False,
                                                  (0, 0, 0))
            TaskTextSurface = pygame.Surface(TaskDescriptionText.get_size())
            TaskTextSurface.fill(BackgroundColor)
            TaskTextSurface.blit(TaskDescriptionText, (0, 0))
            screen.blit(TaskTextSurface, (ScreenWidth * 1 / 10, ScreenHeight * TaskNumber / 5 + j * 40 + 40))

    def reset(self):
        self.ClickedPlayerCards = [0] * 10
        self.ClickedShopCards = [0] * 10
        self.ClickedPlayerCardsDiscounted = [0] * 10
        self.ClickedShopCardsDiscounted = [0] * 10

    def display_player_cards(self, CardsInHand, CardsInHandDiscounted):
        CardsSurface = pygame.Surface((1600,400))
        CardsSurface.fill(RegistrationBackgroundColor)
        screen.blit(CardsSurface, (ScreenWidth * 1 / 60, ScreenHeight * 3 / 10 - 100))
        for i in range(10):
            DisplayedDiscounted = 0
            for j in range(CardsInHand[i]):
                ShowDiscount = False
                if CardsInHandDiscounted[i] > DisplayedDiscounted:
                    DisplayedDiscounted += 1
                    ShowDiscount = True
                screen.blit(self.CardImages[i][ShowDiscount],
                            (ScreenWidth * (1 / 30 + i / 12), ScreenHeight * (3 / 10 + j / 50) - 50))
