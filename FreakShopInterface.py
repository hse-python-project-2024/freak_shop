from LibrariesForInterface import*
from SettingsValues import*
from GameplayRelatedValues import*
screen = pygame.display.set_mode((ScreenWidth, ScreenHieght))
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]:
        sys.exit()
    screen.fill(BackgroundColor)
    ShopNameImage = pygame.image.load("src\\img\\ShopPicture.jpg").convert()

    screen.blit(ShopNameImage, (ScreenWidth/2-100 , ScreenHieght/10))

    CardImage = pygame.image.load("src\\img\\Discount_Image_1.png").convert()
    for i in range(1, AmountOfCardsInHand + 1):
        screen.blit(pygame.transform.scale(CardImage, (160, 225)), (ScreenWidth*i/10, ScreenHieght*7/10))

    pygame.display.update()