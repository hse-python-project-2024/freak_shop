from Client.SettingsValues import*
from Client.GameplayRelatedClasses import*
from Client.LibrariesForInterface import *
screen = pygame.display.set_mode((ScreenWidth, ScreenHieght))
# get global info about the game
GameEntity = GameInfo(1,1,[5,2,4],4,["Pasha", "Sasha", "Nagibator228", "Боб"])
Player = PlayerInfo()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]:
        sys.exit()
    screen.fill(BackgroundColor)
    ShopNameImage = pygame.image.load("../src/img/ShopPicture.jpg").convert()

    screen.blit(ShopNameImage, (ScreenWidth/2-100 , ScreenHieght/10))
    # if ShopNameImage.get_rect().collidepoint(pygame.mouse.get_pos()):
    #    screen.blit(ShopNameImage, (ScreenWidth/2-100 , ScreenHieght/5)) Junk code for now

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
                                                                        ScreenHieght*6/10 + j*ScreenHieght/50))
    my_font = pygame.font.SysFont('Comic Sans MS', 30)

    # Display other players
    for i in range(GameEntity.PlayerAmount):
        PlayerIcon = pygame.image.load("../src/img/Player_Icon.png").convert_alpha()
        screen.blit(pygame.transform.scale(PlayerIcon, (140, 140)), (ScreenWidth * 4 / 5, ScreenHieght * i/ 8))
        PlayerNameText = my_font.render(GameEntity.PlayersNicknames[i], False, (0, 0, 0))
        screen.blit(PlayerNameText, (ScreenWidth * 4 / 5 + 150, ScreenHieght * i/ 8 + 40))

    # Display EndTurnButton
    EndTurnText = my_font.render("Завершить  ход", False, (0, 0, 0))
    screen.blit(EndTurnText, (ScreenWidth * 6 / 7 + 15, ScreenHieght * 3 / 4 - 40))
    EndTurnIcon = pygame.image.load("../src/img/End_Turn_Icon.png").convert_alpha()
    screen.blit(pygame.transform.scale(EndTurnIcon, (250, 250)), (ScreenWidth * 6 / 7, ScreenHieght * 3 / 4))

    # Display tasks
    ind = 0
    for TaskNumber in GameEntity.Tasks:
        TaskName = "../src/img/Task_"
        TaskName += str(TaskNumber)
        TaskName += ".png"
        TaskImage = pygame.image.load(TaskName).convert()
        screen.blit(pygame.transform.scale(TaskImage, (140, 200)), (ScreenWidth * 1 / 50,
                                                                    ScreenHieght * ind / 5 + 10))
        ind += 1
    pygame.display.update()

