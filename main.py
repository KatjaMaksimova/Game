from const import *
from data.sprite.NPC import NPC
from data.sprite.WALL import Wall
import pygame

pygame.init()
screen = pygame.display.set_mode((WIDCH, HENGT))

nps = NPC(screen=screen)

wall = Wall(screen=screen, x=0, y=nps.y + nps.hengt + 2, x2=WIDCH, y2=HENGT)

while True:
    screen.fill((0, 0, 0))
    pygame.time.delay(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    nps.breath()
    wall.visible()
    pygame.display.update()
