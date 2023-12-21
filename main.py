from const import *
from data.sprite.NPC import NPC
import pygame

pygame.init()
screen = pygame.display.set_mode((WIDCH, HENGT))

nps = NPC(screen=screen)

while True:
    screen.fill((0, 0, 0))
    pygame.time.delay(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    nps.breath()
    pygame.display.update()
