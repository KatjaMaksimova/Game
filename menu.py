from const import *
import pygame
from data.menu_data.component import *
from data.sprite.NPC import *


def super_int(x):
    s = x[::-1]
    mass = []
    if len(s) < 4:
        return s
    while s:
        mass.append(s[:3])
        s = s[3::]
    return " ".join(i[::-1] for i in mass[::-1])


def shopping(name):
    file = open("data//menu_data//all_Dino")
    data = list(i.strip() for i in file)
    file.close()

    if name in data:
        return

    file_money = open("money")
    money = int([i.strip() for i in file_money][0])
    file_money.close()

    if NPC_FOTO[name]["price"] <= money:
        money -= NPC_FOTO[name]["price"]
        data.append(name)
    with open("data//menu_data//all_Dino", "w") as f:
        f.write("\n".join(data))
    with open("money", "w") as f:
        f.write(str(money))


def add_money(x: int):
    file_money = open("money")
    money = int([i.strip() for i in file_money][0])
    file_money.close()

    money += x
    with open("money", "w") as f:
        f.write(str(money))


class Menu:
    pygame.init()

    def __init__(self, screen):
        self.screen = screen
        self.fon_strasse = pygame.image.load("data//menu_data//fon.jpg")
        self.fon_strasse = pygame.transform.scale(self.fon_strasse, (WIDCH + 350, HENGT + 250))

        self.shop_hause = pygame.image.load("data//menu_data//shop_hause.jpg")
        self.shop_hause = pygame.transform.scale(self.shop_hause, (WIDCH, HENGT))

        self.hause = pygame.image.load("data//menu_data//hause.jpg")
        self.hause = pygame.transform.scale(self.hause, (WIDCH + 100, HENGT + 100))
        self.money_info = Money(screen=self.screen, count="100")

    def one_window(self):
        text = TextMessage(self.screen, text="GameDino", color=(0, 10, 200), size_text=50)
        text.x = (WIDCH - text.size()[0]) // 2
        text.y = (HENGT - text.size()[1]) // 2
        btn = Button(self.screen, color=(100, 250, 100), text="Начать", length_x=100,
                     length_y=50,
                     x=(WIDCH - 100) // 2, y=(HENGT - 50) // 2 + text.size()[1] + 100,
                     color_text=(0, 0, 0),
                     color_button_activ=(100, 200, 100))
        text.fon(color=(190, 190, 190))

        self.money_info = Money(screen=self.screen, count="100")


        run = True
        while run:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.fon_strasse, (0, -100))
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
                  x=WIDCH // 2 - 10, y=HENGT // 2 - 70)
        shop = Shop(screen=self.screen)
        shop.x = WIDCH - 50 - shop.lenx
        shop.y = 40

        btn_types_dino = Button(self.screen, color=(20, 150, 20),
                                color_text=(240, 240, 240),
                                color_button_activ=(100, 200, 100),
                                text="Выбрать персонажа",
                                length_x=500, length_y=80,
                                x=0, y=HENGT - 80)
        btn_game = Button(
                        self.screen, color=(20, 150, 20),
                        color_text=(240, 240, 240),
                        color_button_activ=(100, 200, 100),
                        text="Начать игру",
                        length_x=200, length_y=80,
                        x=WIDCH - 250, y=HENGT - 80
        )

        while run:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.fon_strasse, (0, -250))
            pygame.time.delay(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    btn_types_dino.activ(*event.pos)
                    btn_game.activ(*event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_types_dino.activ_clicked(*event.pos):
                        return "typesDino"
                    if btn_game.activ_clicked(*event.pos):
                        return "game"
                if shop.activ_clicked():
                    return "shop"

                shop.monitoring(event)
            shop.visible()
            self.money_info.visible()
            btn_types_dino.visible()
            btn_game.visible()
            npc.breath()
            pygame.display.update()

    def shop(self):
        file = open("data//menu_data//all_Dino")

        data = [i.strip() for i in file]

        file.close()
        back = Button(self.screen, color=(20, 150, 20),
                      color_text=(240, 240, 240),
                      color_button_activ=(100, 200, 100),
                      text="Назад",
                      length_x=200, length_y=80,
                      x=0, y=HENGT - 80)

        price = Button(self.screen, color=(20, 150, 20),
                       color_text=(240, 240, 240),
                       color_button_activ=(100, 200, 100),
                       text="Назад",
                       length_x=250, length_y=80,
                       x=450, y=HENGT - 80)

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
            self.screen.blit(self.shop_hause, (0, 0))
            pygame.time.delay(60)
            price.pasiv = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                direction.monitoring(event)
                if event.type == pygame.MOUSEMOTION:
                    back.activ(*event.pos)
                    price.activ(*event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.activ_clicked(*event.pos):
                        return
                    if price.activ_clicked(*event.pos):
                        if price.text != "Куплен":
                            shopping(list_nps[index_show].name)
                            file = open("data//menu_data//all_Dino")
                            data = [i.strip() for i in file]
                            file.close()

            if direction.activ_clicked() == "-->":
                direction.restart()
                index_show = (index_show + 1) % len(list_nps)
            elif direction.activ_clicked() == "<--":
                direction.restart()
                index_show = (index_show - 1) % len(list_nps)

            direction.visible()
            list_nps[index_show].breath()

            back.visible()
            if list_nps[index_show].name not in data:
                price.text = super_int(str(NPC_FOTO[str(list_nps[index_show].name)]["price"]))
                price.color = (20, 150, 20)
            else:
                price.text = "Куплен"
                price.color = (100, 100, 100)
                price.pasiv = True
            price.visible()
            self.money_info.visible()
            pygame.display.update()

    def typesDino(self):
        file = open("data//menu_data//all_Dino")

        data_all_Dino = [i.strip() for i in file]

        file.close()
        back = Button(self.screen, color=(20, 150, 20),
                      color_text=(240, 240, 240),
                      color_button_activ=(100, 200, 100),
                      text="Назад",
                      length_x=200, length_y=80,
                      x=0, y=HENGT - 80)

        active_NPC = Button(
                       self.screen, color=(20, 150, 20),
                       color_text=(240, 240, 240),
                       color_button_activ=(100, 200, 100),
                       text="Выбрать",
                       length_x=250, length_y=80,
                       x=450, y=HENGT - 80)

        direction = Direction(
            screen=self.screen,
            x2=WIDCH - 50,

        )
        list_nps = [NPC(
            screen=self.screen, name=name, widch=230, hengt=230,
            x=WIDCH // 2 - 180, y=HENGT // 2 - 70
        ) for name in data_all_Dino]
        index_show = 0

        active_NPC_temp = None
        with open("data//sprite//main_NPC", "r") as f:
            active_NPC_temp = f.read().strip()

        if active_NPC_temp in {"", None}:
            active_NPC_temp = "Dino"
            with open("data//sprite//main_NPC", "w") as f:
                f.write(active_NPC_temp)

        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.hause, (0, -80))
            pygame.time.delay(60)
            if active_NPC_temp == list_nps[index_show].name:
                active_NPC.pasiv = True
                active_NPC.text = "Выбран"
                active_NPC.color = (100, 100, 100)
            else:
                active_NPC.pasiv = False
                active_NPC.text = "Выбрать"
                active_NPC.color = (20, 150, 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                direction.monitoring(event)
                if event.type == pygame.MOUSEMOTION:
                    back.activ(*event.pos)
                    active_NPC.activ(*event.pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.activ_clicked(*event.pos):
                        return

                    if active_NPC.activ_clicked(*event.pos):
                        temp_name = list_nps[index_show].name
                        if active_NPC_temp != temp_name:
                            active_NPC_temp = temp_name
                            with open("data//sprite//main_NPC", "w") as f:
                                f.write(active_NPC_temp)

            if direction.activ_clicked() == "-->":
                direction.restart()
                index_show = (index_show + 1) % len(list_nps)
            elif direction.activ_clicked() == "<--":
                direction.restart()
                index_show = (index_show - 1) % len(list_nps)

            direction.visible()
            list_nps[index_show].breath()

            back.visible()
            active_NPC.visible()
            self.money_info.visible()

            pygame.display.update()

    def vector_window(self, answer):
        if answer == "OK":
            text = TextMessage(self.screen, text="Победа!!!", color=(0, 200, 100), size_text=150)
        else:
            text = TextMessage(self.screen, text="Поражение:(", color=(200, 100, 100), size_text=150)
        text.x = (WIDCH - text.size()[0]) // 2
        text.y = (HENGT - text.size()[1]) // 2
        btn = Button(self.screen, color=(100, 250, 100), text="Далее", length_x=100,
                     length_y=50,
                     x=100 + (WIDCH - 100) // 2, y=(HENGT - 50) // 2 + text.size()[1] + 100,
                     color_text=(0, 0, 0),
                     color_button_activ=(100, 200, 100))

        btn2 = Button(self.screen, color=(100, 250, 100), text="Ещё", length_x=100,
                     length_y=50,
                     x=-100 + (WIDCH - 100) // 2, y=(HENGT - 50) // 2 + text.size()[1] + 100,
                     color_text=(0, 0, 0),
                     color_button_activ=(100, 200, 100))

        text.fon(color=(220, 220, 220))

        self.money_info = Money(screen=self.screen, count="100")

        run = True
        while run:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.fon_strasse, (0, -100))
            pygame.time.delay(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    btn.activ(*event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn.activ_clicked(*event.pos):
                        return False
                if event.type == pygame.MOUSEMOTION:
                    btn2.activ(*event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn2.activ_clicked(*event.pos):
                        return True

            btn.visible()
            btn2.visible()
            text.visible()
            pygame.display.update()
