import pygame
import os
import sys
import menu

import datetime
from const import *


def game():
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

    def load_image_dino(name):
        fullname = os.path.join('data/img/NPC', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    other_image = {'kwall': load_image('killer.png'),
                   'wall': load_image('barrier.png'),
                   'sky': load_image('sky.png'),
                   'ground': load_image('ground.png'),
                   'groundblock': load_image('ground_block.png'),
                   'live_yes': load_image('live_yes.png'),
                   'live_no': load_image('live_no.png'),
                   'monster': load_image('monster0.png'),
                   'monster2': load_image('monster1.png')}

    dino = open("data//sprite//main_NPC").readline()
    name_dino, name_dino2 = "Dino/Dino.png", "Dino/Dino2.png"
    if dino == "Dino":
        name_dino, name_dino2 = "Dino/Dino.png", "Dino/Dino2.png"
    if dino == "Dino2":
        name_dino, name_dino2 = "Dino2/Dino2.png", "Dino2/Dino2.2.png"
    if dino == "DinoYellow":
        name_dino, name_dino2 = "DinoYellow/DinoYellow.png", "DinoYellow/DinoYellow2.png"
    if dino == "DinoYellow2":
        name_dino, name_dino2 = "DinoYellow2/DinoYellow2.png", "DinoYellow2/DinoYellow2.2.png"

    money_image = [load_image(f'money{i}.png') for i in range(1, 7)]
    player_image = [load_image_dino(name_dino), load_image_dino(name_dino2)]
    cnt_live_image = [load_image('live_yes.png'), load_image('live_no.png')]

    #ground_group = pygame.sprite.Group()
    #sky_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    move_sprites = pygame.sprite.Group()
    money_group = pygame.sprite.Group()
    killer_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()  # препятствия в виде поленьев и земляные платформы
    monster_group = pygame.sprite.Group()
    hearts_list = []

    def generate_text(cnt, sc):
        font = pygame.font.Font('data/pixel_font.ttf', 20)
        text = font.render(f"Money: {cnt}", True, (40, 40, 40))
        place = text.get_rect()
        place.x = width - 120
        place.y = sprite_height + 10
        sc.blit(text, place)

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
            super().__init__(all_sprites, wall_group)
            self.image = other_image['sky']
            self.rect = self.image.get_rect().move(0, 0)

    class Ground(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(all_sprites, wall_group)
            self.image = other_image['ground']
            self.rect = self.image.get_rect().move(0, height - sprite_height)

    class GroundBlock(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(all_sprites, move_sprites, wall_group)
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
            super().__init__(all_sprites, move_sprites, wall_group)
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
            self.now_image = 0
            self.image = player_image[0]
            self.rect = self.image.get_rect().move((pos_x + 1) * sprite_width,
                                                   (pos_y + 1) * sprite_height)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.prew_x = self.rect.x
            self.cnt_live = 3
            self.cnt_of_money = 0
            self.v = 0
            self.cnt = 0
            self.gravity = 1
            self.jumping = False
            self.kill_this = False
            self.killers = []

        def update(self, *args):
            self.prew_x = self.rect.x
            dx, dy = 0, 0

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

            # проверка столкновений со стенами:
            # блоками, не наносящими урона, землёй и небом, блоками земли
            for tile in wall_group:
                rectangle = tile.rect  # прямоугольник объекта
                # проверка столкновений по x
                if rectangle.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # проверка столкновений в координате y
                if rectangle.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # блок над игроком, игрок двигается вверх
                    if self.v < 0:
                        dy = rectangle.bottom - self.rect.top
                        self.v = 0
                    # блок под игроком, игрок падает на него
                    elif self.v >= 0:
                        dy = rectangle.top - self.rect.bottom
                        self.v = 0

            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > height - sprite_height:
                self.rect.bottom = height - sprite_height
                dy = 0

            # анимация
            if self.cnt == 10:
                self.now_image = (self.now_image + 1) % 2
                self.image = player_image[self.now_image]
                self.cnt = 0
            self.cnt += 1

            # проверка столкновений с монетами
            for money in money_group:
                money_rect = money.rect
                if money_rect.colliderect(self.rect):
                    money.kill()
                    self.cnt_of_money += 1

            # проверка столкновений с "убийцами"
            # один убийца может нанести урон только один раз
            for killer in killer_group:
                killer_rect = killer.rect
                if killer not in self.killers and killer_rect.colliderect(self.rect):
                    self.cnt_live -= 1
                    self.killers.append(killer)

            # проверка столкновений с "монстром"
            for monster in monster_group:
                monster_rect = monster.rect
                if monster_rect.colliderect(self.rect):
                    self.kill_this = True

        def return_live(self):
            return self.cnt_live

        def return_coors(self):
            x, y = self.rect.x, self.rect.y
            return x, y, self.prew_x

        def return_money_cnt(self):
            return self.cnt_of_money

        def return_kill(self):
            return self.kill_this

    class Monster(pygame.sprite.Sprite):
        def __init__(self, k_x, k_y):
            super().__init__(monster_group)
            self.images = [other_image['monster'], other_image['monster2']]
            self.image = self.images[0]
            self.cnt_image = 0
            self.now_image = 0
            self.rect = self.image.get_rect()
            self.rect.x = k_x
            self.rect.y = k_y
            self.delta = 0
            self.delta_move = 5

        def update(self, p_x, p_y, prew_x):
            if self.cnt_image > 10:
                self.cnt_image = 0
                self.now_image = (self.now_image + 1) % 2
                self.image = self.images[self.now_image]
            self.delta = p_x - self.rect.x
            if prew_x != p_x:
                self.rect.x = p_x - self.delta
                self.rect.y = p_y
            else:
                self.rect.x += 5
                self.rect.y = p_y
            self.cnt_image += 1

    class Hearts:
        def __init__(self, k_x, k_y, n):
            self.n = n
            self.k_x = k_x
            self.k_y = k_y
            self.image_1 = pygame.transform.scale(other_image['live_yes'], (30, 30))
            self.image_2 = pygame.transform.scale(other_image['live_no'], (30, 30))
            #self.rect = self.image_1.get_rect().move(k_x + (sprite_width + 10) * (n + 1), k_y)

        def update(self, check_n):
            if self.n == check_n:
                self.image_1 = self.image_2
            screen.blit(self.image_1, (self.k_x + (30 + 10) * (self.n + 1), self.k_y))

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
    monster = Monster(0, 480)
    for i in range(3):
        hearts_list.append(Hearts(width - 160, sprite_height * 1.8, i))

    start = datetime.datetime.now()

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        all_sprites.update()
        px, py, prewx = player.return_coors()
        monster.update(px, py, prewx)
        camera.update(player)
        for sprite in move_sprites:
            camera.apply(sprite)
        #screen.fill((220, 24, 84))
        screen.fill((87, 136, 179))
        all_sprites.draw(screen)
        monster_group.draw(screen)
        generate_text(player.return_money_cnt(), screen)
        cnt_of_live = player.return_live()
        for heart in hearts_list:
            heart.update(cnt_of_live)
        play = bool(cnt_of_live) and not player.return_kill()
        pygame.display.flip()
        clock.tick(FPS)
        finish = datetime.datetime.now()
        time_game = finish - start
        if float(str(time_game).split(":")[-1]) > 31:
            break
    s = player.cnt_of_money
    menu.add_money(s)
    if play:
        return "OK"
    else:
        return "NO"
