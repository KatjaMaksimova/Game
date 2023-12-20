from const import *
import pygame
import time

pygame.init()
screen = pygame.display.set_mode((WIDCH, HENGT))

mouse = pygame.image.load(NPC_FOTO["Dino"]["foto"])
mouse = pygame.transform.scale(mouse, (120, 120))
mouseX = 0
mouseY = 200
idx_foto = 0
list_foto = NPC_FOTO["Dino"]["fotoBreath_list"]
while True:
    screen.fill((0, 0, 0))
    pygame.time.delay(30)
    time.sleep(0.1)
    idx_foto += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    idx_foto %= 6
    mouse = pygame.image.load(list_foto[idx_foto])
    mouse = pygame.transform.scale(mouse, (120, 120))
    screen.blit(mouse, (mouseX, mouseY))
    pygame.display.update()
