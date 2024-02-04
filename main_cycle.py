import pygame
import os
import sys

pygame.init()
width, height = size = 1200, 600
screen = pygame.display.set_mode(size)
sprite_width = sprite_height = 60  # last 75

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


other_image = {'kwall': load_image('killer.png'),
               'wall': load_image('barrier.png'),
               'sky': load_image('sky.png'),
               'ground': load_image('ground.png'),
               'groundblock': load_image('ground_block.png')}

money_image = [load_image(f'money{i}.png') for i in range(1, 7)]
player_image = pygame.transform.scale(load_image('Dino.png'), (60, 60))
cnt_live_image = [load_image('live_yes.png'), load_image('live_no.png')]

ground_group = pygame.sprite.Group()
sky_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
move_sprites = pygame.sprite.Group()
money_group = pygame.sprite.Group()
killer_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    Sky()
    Ground()
    px, py = 0, 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                px, py = x, y
            elif level[y][x] == '*':
                Money(x, y)
            elif level[y][x] == 'w':
                Wall(x, y)
            elif level[y][x] == 'k':
                KillerWall(x, y)
            elif level[y][x] == 'g':
                GroundBlock(x, y)
    return Player(px, py)


class Sky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, sky_group)
        self.image = other_image['sky']
        self.rect = self.image.get_rect().move(0, 0)


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, ground_group)
        self.image = other_image['ground']
        self.rect = self.image.get_rect().move(0, height - sprite_height)


class GroundBlock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, ground_group, move_sprites)
        self.image = other_image['groundblock']
        self.rect = self.image.get_rect().move((pos_x + 1) * sprite_width, (pos_y + 1) * sprite_height + 40)

    def update(self, *args):
        if self.rect.x <= - self.rect.w:
            self.kill()


class KillerWall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, killer_group, move_sprites)
        self.image = other_image['kwall']
        self.rect = self.image.get_rect().move((pos_x + 1) * sprite_width, (pos_y + 1) * sprite_height)

    def update(self, *args):
        if self.rect.x <= - self.rect.w:
            self.kill()


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, move_sprites)
        self.image = other_image['wall']
        self.rect = self.image.get_rect().move((pos_x + 1) * sprite_width, (pos_y + 1) * sprite_height)

    def update(self, *args):
        if self.rect.x <= - self.rect.w:
            self.kill()


class Money(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, money_group, move_sprites)
        # счётчик итераций для анимации
        self.cnt = 0
        self.now_image_idx = 0
        self.image = money_image[self.now_image_idx]
        self.rect = self.image.get_rect().move((pos_x + 1) * sprite_width, (pos_y + 1) * sprite_height)

    def update(self, *args):
        self.cnt += 1
        if self.rect.x <= - self.rect.w:
            self.kill()
        if self.cnt == 10:
            self.now_image_idx = (self.now_image_idx + 1) % 6
            self.image = money_image[self.now_image_idx]
            self.cnt = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_group, move_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move((pos_x + 1) * sprite_width,
                                               (pos_y + 1) * sprite_height)
        self.cnt_live = 3
        self.v = 0
        self.gravity = 1
        self.jumping = False

    def update(self, *args):
        dx, dy = 0, 0
        # check collision in future
        dx = 5
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumping:
            self.v = -20
            self.jumping = True
        if not key[pygame.K_SPACE]:
            self.jumping = False
        # "притяжение" персонажа к земле при прыжке
        self.v += self.gravity
        if self.v > 10:
            self.v = 10
        dy += self.v

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > height - sprite_height:
            self.rect.bottom = height - sprite_height
            dy = 0

    def check_event(self):
        key = pygame.key.get_pressed()
        if key[0] == pygame.K_SPACE:
            self.jumping = True


# класс камеры будет управлять объектами, отслеживая игрока по координате x
class Camera:
    def __init__(self):
        self.dx = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)


play = True
clock = pygame.time.Clock()
player = generate_level(load_level(0))
camera = Camera()
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    all_sprites.update()
    camera.update(player)
    for sprite in move_sprites:
        camera.apply(sprite)
    screen.fill((130, 181, 232))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
