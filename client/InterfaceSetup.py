import pygame, sys
from random import *
from time import *
from pygame.locals import *
from math import *
BackgroundColor = (178, 102, 255)
RegistrationBackgroundColor = (255,188,0)
RegistrationButtonColor = (178,102,255)
ScreenWidth = 1920
ScreenHeight = 1080
MaxLoginLength = 15
MaxPasswordLength = 15
pygame.init()
pygame.display.set_caption("Freak Shop")
clock = pygame.time.Clock()
pygame.font.init()
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))

TextFont = pygame.font.SysFont('Comic Sans MS', 30)
TaskFont = pygame.font.SysFont('Comic Sans MS', 25)
RegistrationFont = pygame.font.SysFont('Comic Sans MS', 60)
