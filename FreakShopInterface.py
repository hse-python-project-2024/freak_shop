from Client.SettingsValues import*
from Client.GameplayRelatedClasses import*
from Client.LibrariesForInterface import *
screen = pygame.display.set_mode((ScreenWidth, ScreenHieght))
# get global info about the game
GameEntity = GameInfo(1,1,[1,9,5],4,["Pasha", "Sasha", "Nagibator228", "Боб"])
Player = PlayerInfo()
Shop = ShopInfo()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]:
        sys.exit()
    screen.fill(BackgroundColor)

    # Display Shop_Image 
    ShopImage = pygame.image.load("../src/img/Shop_Image.jpg").convert()
    screen.blit(pygame.transform.scale(ShopImage, (800, 400)), (ScreenWidth/4,
                                                                ScreenHieght/10))

    # Display players cards
    for i in range(10):
        DisplayedDiscounted = 0
        for j in range(Player.CardsInHand[i]):
            CardName = "../src/img/"
            if Player.DiscountedCardsInHand[i] > DisplayedDiscounted:
                DisplayedDiscounted += 1
                CardName += "Discount_Image_"
            else:
                CardName += "Non_Discount_Image_"
            CardName += str(i+1)
            CardName += ".png"
            CardImage = pygame.image.load(CardName).convert()
            screen.blit(pygame.transform.scale(CardImage, (140, 200)), (ScreenWidth*(1/30+i/12),
                                                                        ScreenHieght*(6/10 + j/50)+20))
    # Display shop cards
    for i in range(10):
        DisplayedDiscounted = 0
        for j in range(Shop.CardsInShop[i]):
            CardName = "../src/img/"
            if Shop.DiscountedCardsInShop[i] > DisplayedDiscounted:
                DisplayedDiscounted += 1
                CardName += "Discount_Image_"
            else:
                CardName += "Non_Discount_Image_"
            CardName += str(i + 1)
            CardName += ".png"
            CardImage = pygame.image.load(CardName).convert()
            WidthAdd = i / 8 + 1 / 100
            HeightAdd = 1 / 100
            if i >= 5:
                WidthAdd = (i - 5) / 8 - 1 / 25 - 1 / 100
                HeightAdd += 9 / 30
            screen.blit(pygame.transform.scale(CardImage, (140, 200)), (ScreenWidth * (2 / 10 + WidthAdd),
                                                                        ScreenHieght * (HeightAdd + j / 50)))

    # Display other players
    for i in range(GameEntity.PlayerAmount):
        PlayerIcon = pygame.image.load("../src/img/Player_Icon.png").convert_alpha()
        screen.blit(pygame.transform.scale(PlayerIcon, (140, 140)), (ScreenWidth * 4 / 5, ScreenHieght * i/ 8))
        PlayerNameText = TextFont.render(GameEntity.PlayersNicknames[i], False, (0, 0, 0))
        screen.blit(PlayerNameText, (ScreenWidth * 4 / 5 + 150, ScreenHieght * i/ 8 + 40))

    # Display EndTurnButton
    EndTurnText = TextFont.render("Завершить  ход", False, (0, 0, 0))
    screen.blit(EndTurnText, (ScreenWidth * 6 / 7 + 15, ScreenHieght * 3 / 4 - 40))
    EndTurnIcon = pygame.image.load("../src/img/End_Turn_Icon.png").convert_alpha()
    screen.blit(pygame.transform.scale(EndTurnIcon, (250, 250)), (ScreenWidth * 6 / 7, ScreenHieght * 3 / 4))

    # Display tasks
    ind = 0
    TaskImagesRects = [Rect(0,0,0,0),Rect(0,0,0,0),Rect(0,0,0,0)]
    for TaskNumber in GameEntity.Tasks:
        TaskName = "../src/img/Task_"
        TaskName += str(TaskNumber)
        TaskName += ".png"
        TaskImage = pygame.image.load(TaskName).convert()
        TaskImagesRects[ind] = Rect(ScreenWidth/ 50,ScreenHieght * ind / 5 + 10,140,
                                    200)
        screen.blit(pygame.transform.scale(TaskImage, (140, 200)), (ScreenWidth/ 50,
                                                                    ScreenHieght * ind / 5 + 10))
        ind += 1

    # Display Tasks text when hovering over them
    for i in range (3):
        if TaskImagesRects[i].collidepoint(pygame.mouse.get_pos()):
            for j in range(len(Task_Descriptions[GameEntity.Tasks[i]-1])):
                TaskDescriptionText = TaskFont.render(Task_Descriptions[GameEntity.Tasks[i]-1][j], False, (0, 0, 0))
                TaskTextSurface = pygame.Surface(TaskDescriptionText.get_size())
                TaskTextSurface.fill(BackgroundColor)
                TaskTextSurface.blit(TaskDescriptionText, (0, 0))
                screen.blit(TaskTextSurface, (ScreenWidth * 1 / 10, ScreenHieght * i/5 + j*40 + 40))

    pygame.display.update()

