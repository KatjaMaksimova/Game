import pygame


class TextMessage:
    def __init__(self, screen, x=0, y=0, text="1234", font=None, color=(100, 100, 100), size_text=25):
        self.x, self.y, self.font, self.color = x, y, font, color
        self.text = text
        self.size_text = size_text
        self.screen = screen
        self.fon_true = False
        self.fon_color = (100, 100, 100)

    def visible(self):
        if self.fon_true:
            pygame.draw.rect(self.screen, self.fon_color,
                      (self.x, self.y, *self.size()))
        font = pygame.font.Font(None, self.size_text)
        text = font.render(self.text, True, self.color)
        self.screen.blit(text, (self.x, self.y))

    def size(self):
        font = pygame.font.Font(None, self.size_text)
        text = font.render(self.text, True, self.color)
        return text.get_width(), text.get_height()

    def fon(self, color=(100, 100, 100)):
        self.fon_true = True
        self.fon_color = color


class Money:
    def __init__(self, screen, count, x=0, y=0):
        self.screen, self.x, self.y, self.count = screen, x, y, count
        self.image = pygame.image.load("data//menu_data//money.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.count_text = TextMessage(self.screen, text=f"{self.count}", color=(0, 100, 0), size_text=50)
        self.count_text.fon(color=(190, 190, 190))
        self.count_text.x = 50
        self.count_text.y = 10

    def visible(self):
        self.update()
        self.screen.blit(self.image, (self.x, self.y))
        self.count_text.visible()

    def update(self):
        file_money = open("money")
        self.count = str([i.strip() for i in file_money][0])
        file_money.close()
        self.count_text.text = self.count


class Button:
    def __init__(self, screen, color=(100, 50, 50), text="1234", x=50, y=50, length_x=50, length_y=50,
                 color_text=(150, 150, 150), color_button_activ=(150, 100, 150)):
        (self.screen, self.color,
         self.text, self.x, self.y, self.length_x, self.length_y,
         self.color_text, self.color_button_activ) = (
            screen, color, text, x, y, length_x, length_y, color_text, color_button_activ)
        self.activ_button = False
        self.pasiv = False

    def visible(self):
        r, g, b = self.color
        x, y, length_x, length_y = self.x, self.y, self.length_x, self.length_y
        if self.activ_button and not self.pasiv:
            r, g, b = self.color_button_activ
            x, y, length_x, length_y = x - 5, y - 5, length_x + 10, length_y + 10

        pygame.draw.rect(self.screen, (r, g, b),
                         (x, y, length_x, length_y))

        font = pygame.font.Font(None, 25)
        text = font.render(self.text, True, self.color_text)
        text_x = (self.x + self.length_x // 2) - text.get_width() // 2
        text_y = (self.y + self.length_y // 2) - text.get_height() // 2
        self.screen.blit(text, (text_x, text_y))

    def activ(self, x, y):
        self.activ_button = (self.x <= x <= self.x + self.length_x
                             and self.y <= y <= self.y + self.length_y)

    def activ_clicked(self, x, y):
        self.activ(x, y)
        return self.activ_button


class Shop:
    def __init__(self, screen, x=35, y=35, lenx=120, leny=140):
        self.screen = screen
        self.x = x
        self.y = y
        self.lenx = lenx
        self.leny = leny
        self.activ = False
        self.activ_clicked_bool = False

    def visible(self):
        self.npc = pygame.image.load("data//menu_data//shop.png")
        x, y = 0, 0
        if not self.activ:
            self.npc = pygame.transform.scale(self.npc, (self.lenx, self.leny))
        else:
            x, y = -5, -5
            self.npc = pygame.transform.scale(self.npc, (self.lenx + 10, self.leny + 10))
        self.screen.blit(self.npc, (self.x + x, self.y + y))

    def activ_clicked(self) -> bool:
        return self.activ_clicked_bool

    def monitoring(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            if (self.x <= x <= self.x + self.lenx
                    and self.y <= y <= self.y + self.leny):
                self.activ = True
            else:
                self.activ = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if (self.x <= x <= self.x + self.lenx
                    and self.y <= y <= self.y + self.leny):
                self.activ_clicked_bool = True


class Direction:
    def __init__(self, screen, x1=10, y1=125, x2=200, y2=125, length_x=30, length_y=250,
                 length_x2=30, length_y2=250):
        (self.screen, self.x1, self.y1, self.x2, self.y2, self.length_x, self.length_y,
         self.length_x2, self.length_y2) = (screen, x1, y1, x2, y2, length_x, length_y,
                                            length_x2, length_y2)
        self.activ1, self.activ2 = False, False
        self.activ_clicked1, self.activ_clicked2 = False, False
        self.l = pygame.image.load("data//menu_data//-+.png")
        self.r = pygame.image.load("data//menu_data//+-.png")

    def monitoring(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            if self.x1 <= x <= self.x1 + self.length_x and self.y1 <= y <= self.length_y + self.y1:
                self.activ1 = True
            else:
                self.activ1 = False

            if self.x2 <= x <= self.x2 + self.length_x2 and self.y2 <= y <= self.length_y2 + self.y2:
                self.activ2 = True
            else:
                self.activ2 = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.activ_clicked1 = int(self.activ1)
            self.activ_clicked2 = int(self.activ2)

    def activ_clicked(self):
        return "<--" * int(self.activ_clicked1) + int(self.activ_clicked2) * "-->"

    def restart(self):
        self.activ_clicked1, self.activ_clicked2 = False, False

    def visible(self):
        rr = pygame.transform.scale(self.r, (self.length_x, self.length_y))
        ll = pygame.transform.scale(self.l, (self.length_x2, self.length_y2))
        self.screen.blit(rr, (self.x1, self.y1))
        self.screen.blit(ll, (self.x2, self.y2))
