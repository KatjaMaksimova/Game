import pygame


class TextMessage:
    def __init__(self, screen, x=0, y=0, text="1234", font=None, color=(100, 100, 100), size_text=25):
        self.x, self.y, self.font, self.color = x, y, font, color
        self.text = text
        self.size_text = 25
        self.screen = screen

    def visible(self):
        font = pygame.font.Font(None, self.size_text)
        text = font.render(self.text, True, self.color)
        self.screen.blit(text, (self.x, self.y))

    def size(self):
        font = pygame.font.Font(None, self.size_text)
        text = font.render(self.text, True, self.color)
        return text.get_width(), text.get_height()


class Button:
    def __init__(self, screen, color=(100, 50, 50), text="1234", x=50, y=50, length_x=50, length_y=50,
                 color_text=(150, 150, 150), color_button_activ=(150, 100, 150)):
        (self.screen, self.color,
         self.text, self.x, self.y, self.length_x, self.length_y,
         self.color_text, self.color_button_activ) = (
            screen, color, text, x, y, length_x, length_y, color_text, color_button_activ)
        self.activ_button = False

    def visible(self):
        r, g, b = self.color
        x, y, length_x, length_y = self.x, self.y, self.length_x, self.length_y
        if self.activ_button:
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
