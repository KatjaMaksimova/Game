import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.image = image
        self.rect = self.image.rect()
        self.rect.x = x
        self.rect.y = y
        self.in_jump = False
        self.y_jump = 0
        self.max_height_jump = 150

    def jump(self, sprite_group):
        if self.in_jump:
            if self.y_jump < self.max_height_jump and self.rect.y - 25 <= 75:
                self.y_jump += 25
                self.rect.y -= 25
            elif not pygame.sprite.spritecollideany(self, sprite_group):
                self.rect.y += 25
            else:
                self.in_jump = False
                self.y_jump = 0
