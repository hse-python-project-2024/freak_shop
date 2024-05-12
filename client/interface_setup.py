import pygame
import sys
from random import *
from time import *
from pygame.locals import *
from math import *
from view_model import Languages

# Visual settings of Menus and IngameInterface

BackgroundColor = (178, 102, 255)
RegistrationBackgroundColor = (255, 188, 0)
RegistrationButtonColor = (178, 102, 255)
MessageBackgroundColor = (51, 153, 255)
ScreenWidth = 1920
ScreenHeight = 1080
MaxLoginLength = 25
MaxPasswordLength = 25
DefaultWaitTime = 0.2

# For the texts: russian = 0, english = 1, rest are unimplemented yet

Task_Descriptions = [
    [["Игрок получает 5 очков за каждый номинал,",
     "карт которого у него больше, чем у остальных",
     "   (при равенстве - очки получают оба)      "],

    ["Игрок получает 3 очка за каждые 10 очков",
     "в сумме номиналов его карт"],

    ["Игрок получает очки за каждую тройку карт",
     "одного номинала: 3 очка за номиналы 1,2,3",
     "5 очков за 4,5,6 и 7 очков за 7,8,9,10"],

    ["Игрок получает очки за каждую пару карт",
     "одного номинала: 2 очка за номиналы 1,2,3",
     " 4 очка за 4,5,6 и 5 очков за 7,8,9,10"],

    ["         Игрок получает 3 очка   ",
     "за каждый номинал в своём поместье"],

    ["  Игрок получает 3 очка за каждый номинал",
     "в своей самой длинной последовательности",
     "         (например 3-4-5-6-7)           "],

    ["  Игрок получает 3 очка за каждую карту",
     "своего самого многочисленного номинала",
     "(при равенстве выбирается наименьший)"],

    ["Игрок получает очки за каждую последовательность",
     "         длины 3: 3 очка если номиналы меньше 4,     ",
     "                5 если меньше 8, и 7 иначе            "],

    ["       Игрок получает 2 очка за каждый номинал",
     "             который у него есть, если",
     "среди карт этого номинала нет товаров по акции"],

    ["  Игрок получает очки в замисимости от количества",
     "   товаров по акции(от меньшего к большему):10-6-3",
     "(при равенстве количества, оба игрока получают очки)"],

    ["       Игрок получает 2 очка за каждый номинал",
     "              который у него есть, если",
     "среди карт этого номинала есть товары по акции"],

    ["  Игрок получает очки в замисимости от количества",
     "   товаров по акции(от большего к меньшему):10-6-3",
     "(при равенстве количества, оба игрока получают очки)"]
],
    [["A Player receives 5 points for each nominal",
     "that he has more cards of, than other players",
     "(in case 2 players are tied - both get points)"],

     ["A Player receives 3 points for each 10",
      "points in the sum of his cards nominals"],

    ["A Player receuves points for each trio of cards",
     "of same nominal: 3 points for: 1,2,3",
     "5 points for: 4,5,6 and 7 points for: 7,8,9,10"],

    ["A Player receuves points for each pair of cards",
     "of same nominal: 2 points for: 1,2,3",
     " 4 points for: 4,5,6 and 5 points for: 7,8,9,10"],

    ["     A Player receives 3 points    ",
     "  for each nominal in his mansion "],

    ["  A Player receives 3 points for each nominal",
     " in his longest consecutive line of nominals ",
     "               (e.g 3-4-5-6-7)               "],

    ["A Player receives 3 points for each card",
     "       of his most popular nominal      ",
     "      (if tied - pick the smallest)     "],

    [" A player receives points for each consecutive line",
     "   of length 3: 3 points if the nominals are < 4,  ",
     "        5 if nominals are < 8, and 7 otherwise     "],

    [" A Player receives 2 points for each nominal ",
     "              in his mansion                 ",
     "if that nominal DOESN`T have discounted cards"],

    [" A Player receives points for discounted cards:",
     " The one with LEAST such cards gets first:10-6-3",
     "  (if players are tied - both get the points)  "],

     [" A Player receives 2 points for each nominal ",
      "              in his mansion                 ",
      "      if that nominal HAS discounted cards   "],

     [" A Player receives points for discounted cards:",
      " The one with MOST such cards gets first:10-6-3",
      "  (if players are tied - both get the points)  "]
     ]]

EndTurnTexts = ["Совершить обмен","Exchange"]

YouTexts = ["Вы","You"]

LoginTexts = ["Логин :","Login :"]
NicknameTexts = ["Имя :","Name :"]
PasswordTexts = ["Пароль : ","Password :"]
RepeatPasswordTexts = ["Повторите пароль : ","Repeat the password :"]

ConfirmTexts =["Войти","Enter"]
RegistrationTexts = ["Регистрация", "Registration"]
InitialRegistrationTexts = ["Зарегестрироваться", "Register"]

JoinGameTexts = ["Присоединиться к игре", "     Join the new game  "]
CreateGameTexts = ["Создать игру", "Create the game"]
SettingsTexts = ["Настройки", "  Settings"]
LeaderbordTexts = ["Списки лидеров", "    Leaderboard"]

LanguageSettingsTexts = ["      Язык :","Language :"]

GameCodeTexts = ["Код игры :", "Game code :"]

ReadyTexts = ["Готов","Ready"]

RuText = "Ru"
EnText = "En"


pygame.init()
pygame.display.set_caption("Freak Shop")
clock = pygame.time.Clock()
pygame.font.init()
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))

# Fonts
TextFont = pygame.font.SysFont('Comic Sans MS', 40)
TaskFont = pygame.font.SysFont('Comic Sans MS', 25)
PlayerNicknameInLobbyFont = pygame.font.SysFont('Comic Sans MS', 60)
RegistrationFont = pygame.font.SysFont('Comic Sans MS', 80)
CodeFont = pygame.font.SysFont('Comic Sans MS', 120)
