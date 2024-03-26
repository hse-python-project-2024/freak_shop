from display_functions import GameBoardView
from gameplay_info_classes import GameInfo, PlayerInfo, ShopInfo
from interface_setup import *


class Game:
    def __init__(self, NewGameInfo):
        self.Info = NewGameInfo

    def StartGame(self):
        # get player and shop info
        Player = PlayerInfo()
        Shop = ShopInfo()
        ClickedPlayerCards = [0] * 10
        ClickedPlayerCardsDiscounted = [0] * 10
        ClickedShopCards = [0] * 10
        ClickedShopCardsDiscounted = [0] * 10
        TaskImagesRects = list()
        UpdateStatus = 1
        GameBoard = GameBoardView()
        while True:
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
                    MousePosition = pygame.mouse.get_pos()

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_ESCAPE]:
                sys.exit()

            if Rect(ScreenWidth * 6 / 7, ScreenHeight * 3 / 4, 250, 250).collidepoint(pygame.mouse.get_pos()):
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
