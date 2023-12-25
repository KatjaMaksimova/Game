import pygame


class Wall:
    def __init__(self, screen, x, y, x2, y2, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.screen = screen
        self.x2, self.y2 = x2, y2

    def visible(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.x2, self.y2), 5)
