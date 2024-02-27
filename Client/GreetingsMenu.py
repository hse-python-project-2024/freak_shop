from Client.FreakShopInterface import *
from Client.RegistrationMenu import *
from Client.EnterMenu import *
while True:
    screen.fill(RegistrationBackgroundColor)
    EnterButton = Rect(ScreenWidth*11/38,ScreenHeight/6,800,250)
    RegistrationButton = Rect(ScreenWidth*11/38, ScreenHeight/2,800,250)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if EnterButton.collidepoint(pygame.mouse.get_pos()):
                ShowEnter()
            if RegistrationButton.collidepoint(pygame.mouse.get_pos()):
                ShowResgistration()

    pygame.draw.rect(screen, RegistrationButtonColor, EnterButton)
    pygame.draw.rect(screen, RegistrationButtonColor, RegistrationButton)
    EnterText = RegistrationFont.render("Войти", False, (0, 0, 0))
    RegistrationText = RegistrationFont.render("Зарегестрироваться", False, (0, 0, 0))
    screen.blit(EnterText, (EnterButton.center[0] - 80, EnterButton.center[1]-40))
    screen.blit(RegistrationText, (RegistrationButton.center[0] - 270, RegistrationButton.center[1] - 40))
    pygame.display.update()