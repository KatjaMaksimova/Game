import pygame
from const import *


class NPC:
    def __init__(self, screen, x=120, y=300, name="Dino", widch=150, hengt=150):
        self.x, self.y = x, y
        self.widch, self.hengt = widch, hengt
        self.screen = screen
        self.npc = pygame.image.load(NPC_FOTO["Dino"]["foto"])
        self.npc = pygame.transform.scale(self.npc, (widch, hengt))

        self.fotoBreath_list = NPC_FOTO[name]["fotoBreath_list"]
        self.foto = NPC_FOTO[name]["foto"]
        self.count_fotoBreath = len(self.fotoBreath_list)
        self.index_fotoBreath = 0

    def breath(self):
        self.index_fotoBreath += 1
        self.index_fotoBreath %= self.count_fotoBreath
        self.npc = pygame.image.load(self.fotoBreath_list[self.index_fotoBreath])
        self.npc = pygame.transform.scale(self.npc, (self.widch, self.hengt))
        self.screen.blit(self.npc, (self.x, self.y))

