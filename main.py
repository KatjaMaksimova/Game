from data.menu_data.component import *
from const import *
import pygame
from menu import *
import main_cycle

pygame.init()
screen = pygame.display.set_mode((WIDCH, HENGT))
menu = Menu(screen)

music_menu = pygame.mixer.Sound('music/fon_musik.ogg')
music_menu.play(-1)
with open("data//sprite//main_NPC", "r") as f:
    name_NPC = f.readline().strip()
if not name_NPC:
    name_NPC = "Dino"

if menu.one_window():
    while True:
        answer = menu.main_window(name=name_NPC)
        if answer == "shop":
            menu.shop()
        elif answer == "typesDino":
            menu.typesDino()
        elif answer == "game":
            answer = main_cycle.game()
            while menu.vector_window(answer):
                answer = main_cycle.game()
        with open("data//sprite//main_NPC", "r") as f:
            name_NPC = f.readline().strip()
        if not name_NPC:
            with open("data//sprite//main_NPC", "w") as f:
                f.write("Dino")
            name_NPC = "Dino"
