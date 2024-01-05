from const import *
import pygame
from data.menu_data.component import *


class Menu:
    pygame.init()

    def __init__(self, screen):
        self.screen = screen

    def one_window(self):
        while True:
            self.screen.fill((0, 0, 0))
            pygame.time.delay(60)
            text = TextMessage(self.screen, text="GameDino", color=(200, 200, 200), size_text=50)
            text.x = (WIDCH - text.size()[0]) // 2
            text.y = (HENGT - text.size()[1]) // 2
            btn = Button(self.screen, color=(100, 250, 100), text="Начать", length_x=100,
                         length_y=50,
                         x=(WIDCH - 100) // 2, y=(HENGT - 50) // 2 + text.size()[1] + 100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            btn.visible()
            text.visible()



            pygame.display.update()


