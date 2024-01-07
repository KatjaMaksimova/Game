from const import *
import pygame
from data.menu_data.component import *
from data.sprite.NPC import *


class Menu:
    pygame.init()

    def __init__(self, screen):
        self.screen = screen

    def one_window(self):
        text = TextMessage(self.screen, text="GameDino", color=(200, 200, 200), size_text=50)
        text.x = (WIDCH - text.size()[0]) // 2
        text.y = (HENGT - text.size()[1]) // 2
        btn = Button(self.screen, color=(100, 250, 100), text="Начать", length_x=100,
                     length_y=50,
                     x=(WIDCH - 100) // 2, y=(HENGT - 50) // 2 + text.size()[1] + 100,
                     color_text=(0, 0, 0),
                     color_button_activ=(200, 200, 200))
        run = True
        while run:
            self.screen.fill((0, 0, 0))
            pygame.time.delay(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    btn.activ(*event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn.activ_clicked(*event.pos):
                        return True

            btn.visible()
            text.visible()
            pygame.display.update()

    def main_window(self, name) -> str:
        run = True
        npc = NPC(screen=self.screen, name=name, widch=230, hengt=230,
                  x=WIDCH // 2 - 180, y=HENGT // 2 - 70)
        shop = Shop(screen=self.screen)
        shop.x = WIDCH - 50 - shop.lenx
        shop.y = 40

        btn_types_dino = Button(self.screen, color=(20, 150, 20),
                                color_text=(240, 240, 240),
                                color_button_activ=(100, 200, 100),
                                text="Выбрать персонажа",
                                length_x=500, length_y=80,
                                x=0, y=HENGT - 80)

        while run:
            self.screen.fill((0, 0, 0))
            pygame.time.delay(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    btn_types_dino.activ(*event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_types_dino.activ_clicked(*event.pos):
                        return "typesDino"
                if shop.activ_clicked():
                    return "shop"

                shop.monitoring(event)
            shop.visible()
            btn_types_dino.visible()
            npc.breath()
            pygame.display.update()

    def shop(self):
        back = Button(self.screen, color=(20, 150, 20),
                      color_text=(240, 240, 240),
                      color_button_activ=(100, 200, 100),
                      text="Назад",
                      length_x=200, length_y=80,
                      x=0, y=HENGT - 80)

        direction = Direction(
            screen=self.screen,
            x2=WIDCH - 50,

        )
        list_nps = [NPC(
            screen=self.screen, name=name, widch=230, hengt=230,
            x=WIDCH // 2 - 180, y=HENGT // 2 - 70
        ) for name in NPC_FOTO]
        index_show = 0

        while True:
            self.screen.fill((0, 0, 0))
            pygame.time.delay(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                direction.monitoring(event)
                if event.type == pygame.MOUSEMOTION:
                    back.activ(*event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.activ_clicked(*event.pos):
                        return

            if direction.activ_clicked() == "-->":
                direction.restart()
                index_show = (index_show + 1) % len(list_nps)
            elif direction.activ_clicked() == "<--":
                direction.restart()
                index_show = (index_show - 1) % len(list_nps)

            direction.visible()
            list_nps[index_show].breath()

            back.visible()

            pygame.display.update()
