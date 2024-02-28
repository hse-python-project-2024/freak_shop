from client.InterfaceSetup import *
from client.GameplayRelatedClasses import *

def DisplayShopImage():
    ShopImage = pygame.image.load("../src/img/Shop_Image.jpg").convert()
    screen.blit(pygame.transform.scale(ShopImage, (800, 400)), (ScreenWidth / 4,
                                                                ScreenHeight / 10))

def DisplayPlayerCards(CurrentPlayer):
    for i in range(10):
        DisplayedDiscounted = 0
        for j in range(CurrentPlayer.CardsInHand[i]):
            CardName = "../src/img/"
            if CurrentPlayer.DiscountedCardsInHand[i] > DisplayedDiscounted:
                DisplayedDiscounted += 1
                CardName += "Discount_Image_"
            else:
                CardName += "Non_Discount_Image_"
            CardName += str(i + 1)
            CardName += ".png"
            CardImage = pygame.image.load(CardName).convert()
            screen.blit(pygame.transform.scale(CardImage, (140, 200)), (ScreenWidth * (1 / 30 + i / 12),
                                                                        ScreenHeight * (6 / 10 + j / 50) + 20))

def DisplayShopCards(CurrentShop):
    for i in range(10):
        DisplayedDiscounted = 0
        for j in range(CurrentShop.CardsInShop[i]):
            CardName = "../src/img/"
            if CurrentShop.DiscountedCardsInShop[i] > DisplayedDiscounted:
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
                                                                        ScreenHeight * (HeightAdd + j / 50)))

def DisplayPlayerList(Game):
    for i in range(Game.PlayerAmount):
        PlayerIcon = pygame.image.load("../src/img/Player_Icon.png").convert_alpha()
        screen.blit(pygame.transform.scale(PlayerIcon, (140, 140)), (ScreenWidth * 4 / 5, ScreenHeight * i / 8))
        PlayerNameText = TextFont.render(Game.PlayersNicknames[i], False, (0, 0, 0))
        screen.blit(PlayerNameText, (ScreenWidth * 4 / 5 + 150, ScreenHeight * i / 8 + 40))

def DisplayEndTurnButton():
    EndTurnText = TextFont.render("Совершить обмен", False, (0, 0, 0))
    screen.blit(EndTurnText, (ScreenWidth * 6 / 7 + 15, ScreenHeight * 3 / 4 - 40))
    EndTurnIcon = pygame.image.load("../src/img/End_Turn_Icon.png").convert_alpha()
    screen.blit(pygame.transform.scale(EndTurnIcon, (250, 250)), (ScreenWidth * 6 / 7, ScreenHeight * 3 / 4))

def DisplayTaskList(Game):
    ind = 0
    TaskImagesRects = [Rect(0, 0, 0, 0), Rect(0, 0, 0, 0), Rect(0, 0, 0, 0)]
    for TaskNumber in Game.Tasks:
        TaskName = "../src/img/Task_"
        TaskName += str(TaskNumber)
        TaskName += ".png"
        TaskImage = pygame.image.load(TaskName).convert()
        TaskImagesRects[ind] = Rect(ScreenWidth / 50, ScreenHeight * ind / 5 + 10, 140,
                                    200)
        screen.blit(pygame.transform.scale(TaskImage, (140, 200)), (ScreenWidth / 50,
                                                                    ScreenHeight * ind / 5 + 10))
        ind += 1
    return TaskImagesRects