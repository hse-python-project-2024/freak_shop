from display_functions import GameBoardView
from gameplay_info_classes import GameInfo, PlayerInfo, ShopInfo
from interface_setup import *


class Game:
    def __init__(self, NewGameInfo):
        self.Info = NewGameInfo
        self.EndTurnButtonRect = Rect(ScreenWidth * 6 / 7, ScreenHeight * 3 / 4, 250, 250)

    def StartGame(self):
        # get player and shop info
        Player = PlayerInfo()
        Shop = ShopInfo()
        TaskImagesRects = list()
        UpdateStatus = 1
        GameBoard = GameBoardView()
        while True:
            IsMyTurn = True  # Ask server about this
            # get new Player and Shop Info
            NewPlayer = PlayerInfo()
            NewShop = ShopInfo()

            if NewPlayer != Player or NewShop != Shop:
                UpdateStatus = 1
                Player = NewPlayer
                Shop = NewShop

            if UpdateStatus == 1:
                screen.fill(BackgroundColor)
                GameBoard.display_shop_image()
                GameBoard.display_player_cards(Player)
                GameBoard.display_shop_cards(Shop)
                GameBoard.display_player_list(self.Info)
                GameBoard.display_end_turn_button(False)
                TaskImagesRects = GameBoard.display_task_list(self.Info)
                UpdateStatus = 0

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if IsMyTurn:
                        MousePosition = pygame.mouse.get_pos()
                        if self.EndTurnButtonRect.collidepoint(MousePosition):
                            GameBoard.reset()

                        # Shop card click checks
                        for i in range(10):
                            for j in range(Shop.CardsInShop[i] - 1, -1, -1):
                                WidthAdd = i / 8 + 1 / 100
                                HeightAdd = 1 / 100
                                if i >= 5:
                                    WidthAdd = (i - 5) / 8 - 1 / 25 - 1 / 100
                                    HeightAdd += 9 / 30
                                CardRect = Rect(ScreenWidth * (2 / 10 + WidthAdd),
                                                ScreenHeight * (HeightAdd + j / 50), 140, 200)
                                if CardRect.collidepoint(MousePosition):
                                    if GameBoard.ClickedShopCards[i] > j:
                                        GameBoard.ClickedShopCards[i] -= 1
                                    else:
                                        GameBoard.ClickedShopCards[i] += 1
                                    print(GameBoard.ClickedShopCards)
                                    break

                        # Hand card click checks
                        for i in range(10):
                            for j in range(Player.CardsInHand[i] - 1, -1, -1):
                                CardRect = Rect(ScreenWidth * (1 / 30 + i / 12),
                                                ScreenHeight * (6 / 10 + j / 50) + 20, 140, 200)
                                if CardRect.collidepoint(MousePosition):
                                    if GameBoard.ClickedPlayerCards[i] > j:
                                        GameBoard.ClickedPlayerCards[i] -= 1
                                    else:
                                        GameBoard.ClickedPlayerCards[i] += 1
                                    print(GameBoard.ClickedPlayerCards)
                                    break

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_ESCAPE]:
                sys.exit()

            if self.EndTurnButtonRect.collidepoint(pygame.mouse.get_pos()):
                GameBoard.display_end_turn_button(True)
            else:
                GameBoard.display_end_turn_button(False)
                # Display Tasks text when hovering over them
                for i in range(3):
                    if TaskImagesRects[i].collidepoint(pygame.mouse.get_pos()):
                        for j in range(len(Task_Descriptions[self.Info.Tasks[i] - 1])):
                            TaskDescriptionText = TaskFont.render(Task_Descriptions[self.Info.Tasks[i] - 1][j], False,
                                                                  (0, 0, 0))
                            TaskTextSurface = pygame.Surface(TaskDescriptionText.get_size())
                            TaskTextSurface.fill(BackgroundColor)
                            TaskTextSurface.blit(TaskDescriptionText, (0, 0))
                            screen.blit(TaskTextSurface, (ScreenWidth * 1 / 10, ScreenHeight * i / 5 + j * 40 + 40))
                        break
            pygame.display.update()
