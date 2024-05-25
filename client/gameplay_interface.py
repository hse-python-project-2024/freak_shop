from display_functions import GameBoardView
from gameplay_info_classes import GameInfo, PlayerInfo, ShopInfo
from interface_setup import *
from menu import ReturnStatus


class GameView:
    def __init__(self, NewGameInfo):
        self.Info = NewGameInfo
        self.EndTurnButtonRect = Rect(ScreenWidth * 6 / 7, ScreenHeight * 3 / 4, 250, 250)

        self.TaskImagesRects = list()
        self.GameBoard = GameBoardView()

        self.Player = PlayerInfo()
        self.Shop = ShopInfo()
        self.IsMyTurn = True
        self.CurrentPlayerPosition = 0

    def update_game_info(self, PlayerCardList, ShopCardList, NewCurPlayer):
        NewPlayer = PlayerInfo()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(PlayerCardList)
        NewPlayer.CardsInHand = PlayerCardList[0]
        NewPlayer.DiscountedCardsInHand = PlayerCardList[1]
        NewShop = ShopInfo()
        NewShop.CardsInShop = ShopCardList[0]
        NewShop.DiscountedCardsInShop = ShopCardList[1]
        self.Player = NewPlayer
        self.Shop = NewShop
        self.CurrentPlayerPosition = NewCurPlayer
        if NewCurPlayer == self.Info.MyPosition:
            self.IsMyTurn = True
        else:
            self.IsMyTurn = False

    def update_start_game_status(self, NewGameInfo):
        self.Info = NewGameInfo

    def ShowMainGameWindow(self,lang):
        screen.fill(BackgroundColor)
        self.GameBoard.display_shop_image()
        self.GameBoard.display_player_cards(self.Player)
        self.GameBoard.display_shop_cards(self.Shop)
        self.GameBoard.display_player_list(self.Info, self.Info.MyPosition,lang,self.CurrentPlayerPosition)
        self.GameBoard.display_end_turn_button(False,lang)
        self.GameBoard.display_scores(self.Info)
        TaskImagesRects = self.GameBoard.display_task_list(self.Info)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.IsMyTurn:
                    MousePosition = pygame.mouse.get_pos()
                    if self.EndTurnButtonRect.collidepoint(MousePosition):
                        self.GameBoard.reset()

                    # Shop card click checks
                    for i in range(10):
                        AlreadyClicked = False
                        for j in range(self.Shop.CardsInShop[i] - 1, self.Shop.DiscountedCardsInShop[i] - 1, -1):
                            WidthAdd = i / 8 + 1 / 100
                            HeightAdd = 1 / 100
                            if i >= 5:
                                WidthAdd = (i - 5) / 8 - 1 / 25 - 1 / 100
                                HeightAdd += 9 / 30
                            CardRect = Rect(ScreenWidth * (2 / 10 + WidthAdd) - 80,
                                            ScreenHeight * (HeightAdd + j / 50), 140, 200)
                            if CardRect.collidepoint(MousePosition):
                                if self.GameBoard.ClickedShopCards[i] + self.Shop.DiscountedCardsInShop[i] > j:
                                    self.GameBoard.ClickedShopCards[i] -= 1
                                else:
                                    self.GameBoard.ClickedShopCards[i] += 1
                                AlreadyClicked = True
                                break
                        if not AlreadyClicked:
                            for j in range(self.Shop.DiscountedCardsInShop[i] - 1, -1, -1):
                                WidthAdd = i / 8 + 1 / 100
                                HeightAdd = 1 / 100
                                if i >= 5:
                                    WidthAdd = (i - 5) / 8 - 1 / 25 - 1 / 100
                                    HeightAdd += 9 / 30
                                CardRect = Rect(ScreenWidth * (2 / 10 + WidthAdd) - 80,
                                                ScreenHeight * (HeightAdd + j / 50), 140, 200)
                                if CardRect.collidepoint(MousePosition):
                                    if self.GameBoard.ClickedShopCardsDiscounted[i] > j:
                                        self.GameBoard.ClickedShopCardsDiscounted[i] -= 1
                                    else:
                                        self.GameBoard.ClickedShopCardsDiscounted[i] += 1
                                    break

                    # Hand card click checks
                    for i in range(10):
                        AlreadyClicked = False
                        for j in range(self.Player.CardsInHand[i] - 1, self.Player.DiscountedCardsInHand[i] - 1, -1):
                            CardRect = Rect(ScreenWidth * (1 / 30 + i / 12),
                                            ScreenHeight * (6 / 10 + j / 50) + 20, 140, 200)
                            if CardRect.collidepoint(MousePosition):
                                if self.GameBoard.ClickedPlayerCards[i] + self.Player.DiscountedCardsInHand[i] > j:
                                    self.GameBoard.ClickedPlayerCards[i] -= 1
                                else:
                                    self.GameBoard.ClickedPlayerCards[i] += 1
                                AlreadyClicked = True
                                break
                        if not AlreadyClicked:
                            for j in range(self.Player.DiscountedCardsInHand[i] - 1, -1, -1):
                                CardRect = Rect(ScreenWidth * (1 / 30 + i / 12),
                                                ScreenHeight * (6 / 10 + j / 50) + 20, 140, 200)
                                if CardRect.collidepoint(MousePosition):
                                    if self.GameBoard.ClickedPlayerCardsDiscounted[i] > j:
                                        self.GameBoard.ClickedPlayerCardsDiscounted[i] -= 1
                                    else:
                                        self.GameBoard.ClickedPlayerCardsDiscounted[i] += 1
                                    break

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            Returnee = [ReturnStatus.quit,[""]]
            return Returnee

        if self.EndTurnButtonRect.collidepoint(pygame.mouse.get_pos()):
            self.GameBoard.display_end_turn_button(True,lang)
        else:
            self.GameBoard.display_end_turn_button(False,lang)
            # Display Tasks text when hovering over them
            for i in range(3):
                if TaskImagesRects[i].collidepoint(pygame.mouse.get_pos()):
                    self.GameBoard.display_tasks_text(self.Info.Tasks,i,lang)
                    break

        Returnee = [ReturnStatus.stay, [""]]
        return Returnee

