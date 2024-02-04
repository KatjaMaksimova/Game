import pygame
import os
import sys

pygame.init()
width, height = size = 1200, 600
screen = pygame.display.set_mode(size)

FPS = 60


def load_level(num_of_level):
    with open(f"data/levels/{num_of_level}.txt", 'r') as file:
        level_map = [line.strip() for line in file]
    return level_map


def load_image(name):
    fullname = os.path.join('data/sprites/', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


other_image = {'kwall': load_image('killer_wall.png'),
               'wall': load_image('wall.png'),
               'money': load_image('money.png')}

player_image = pygame.transform.scale(load_image('Dino.png'), (75, 75))


sprite_width = sprite_height = 75

all_sprites = pygame.sprite.Group()
money_group = pygame.sprite.Group()
killer_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                Player(x, y)
            elif level[y][x] == '*':
                Money(x, y)
            elif level[y][x] == 'w':
                Wall(x, y)
            elif level[y][x] == 'k':
                KillerWall(x, y)


class KillerWall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, killer_group)
        self.image = other_image['kwall']
        self.rect = self.image.get_rect().move((pos_x + 1) * sprite_width, (pos_y + 1) * sprite_height)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = other_image['wall']
        self.rect = self.image.get_rect().move((pos_x + 1) * sprite_width, (pos_y + 1) * sprite_height)


class Money(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, money_group)
        self.image = other_image['money']
        self.rect = self.image.get_rect().move((pos_x + 1) * sprite_width, (pos_y + 1) * sprite_height)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move((pos_x + 1) * sprite_width, (pos_y + 1) * sprite_height)


play = True
clock = pygame.time.Clock()
generate_level(load_level(0))
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((130, 181, 232))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

