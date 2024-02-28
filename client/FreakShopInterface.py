from client.DisplayFunctions import *


def StartGame():
    # get global info about the game
    # get player ID

    GameEntity = GameInfo(1, 1, [1, 9, 5], 4, ["Pasha", "Sasha", "Nagibator228", "Боб"])
    Player = PlayerInfo()
    Shop = ShopInfo()
    TaskImagesRects = list()
    UpdateStatus = 1
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
            DisplayShopImage()
            DisplayPlayerCards(Player)
            DisplayShopCards(Shop)
            DisplayPlayerList(GameEntity)
            DisplayEndTurnButton()
            TaskImagesRects = DisplayTaskList(GameEntity)
            UpdateStatus = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            sys.exit()


        if Rect(ScreenWidth * 6 / 7, ScreenHeight * 3 / 4, 250, 250).collidepoint(pygame.mouse.get_pos()):
            EndTurnIconActivated = pygame.image.load("../src/img/End_Turn_Icon_Activated.png").convert_alpha()
            screen.blit(pygame.transform.scale(EndTurnIconActivated, (250, 250)), (ScreenWidth * 6 / 7, ScreenHeight * 3 / 4))
        else:
            DisplayEndTurnButton()
            # Display Tasks text when hovering over them
            for i in range(3):
                if TaskImagesRects[i].collidepoint(pygame.mouse.get_pos()):
                    for j in range(len(Task_Descriptions[GameEntity.Tasks[i] - 1])):
                        TaskDescriptionText = TaskFont.render(Task_Descriptions[GameEntity.Tasks[i] - 1][j], False,
                                                              (0, 0, 0))
                        TaskTextSurface = pygame.Surface(TaskDescriptionText.get_size())
                        TaskTextSurface.fill(BackgroundColor)
                        TaskTextSurface.blit(TaskDescriptionText, (0, 0))
                        screen.blit(TaskTextSurface, (ScreenWidth * 1 / 10, ScreenHeight * i / 5 + j * 40 + 40))
                    break

        pygame.display.update()
