import sqlite3
import sys

import pygame
from Frame import Game_process

run, kto = True, 1
tool_color, tool_message = "blue", ''
need_input1, input_text1, need_input2, input_text2, need_input3, input_text3 = False, '', False, '', False, ''
running = True


def registration():
    global tool_message, tool_color, need_input1, need_input2, need_input3, input_text3, input_text2, input_text1, run
    global running
    tool_color, tool_message = "blue", ''
    need_input1, input_text1, need_input2, input_text2, need_input3, input_text3 = False, '', False, '', False, ''

    class Buttons:
        def __init__(self, wid1, hei1, osob=False, fs=40, in_c=(20, 17, 237), ac_c=(134, 132, 232)):
            self.width, self.height = wid1, hei1
            self.inactive_color = in_c
            self.active_color = ac_c
            self.osob = osob
            self.fs = fs

        def draw(self, x, y, message, xka=8, yka=12):
            global running
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if x < mouse[0] < x + self.width:
                if y < mouse[1] < y + self.height:
                    pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
                    if click[0] == 1 and self.osob:
                        conbd()
                    elif click[0] == 1:
                        running = False
                else:
                    pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
            else:
                pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

            print_text(message, x + xka, y + yka, font_size=self.fs)

    def conbd():
        global input_text1, input_text2, input_text3, tool_color, tool_message

        if not (input_text1 and input_text2 and input_text3):
            tool_color, tool_message = "red", "Некорректные данные!"
            return
        elif input_text2 != input_text3:
            tool_color, tool_message = "red", "Пароли не совпадают!"
            return

        con = sqlite3.connect("Information_about_player.db")
        cur = con.cursor()
        result = cur.execute(f"""select id from users 
        where login = '{input_text1}'""").fetchall()

        if result:
            tool_color, tool_message = "red", "Такой пользователь уже существует!"
            return

        cur.execute(f"""INSERT INTO users(login, password) VALUES('{input_text1}', '{input_text2}')""")
        con.commit()
        tool_color, tool_message = "green", "Данные успешно добавлены"

    def print_text(message, x, y, font_color=(255, 255, 255), font_size=40):
        font_type = pygame.font.Font(None, font_size)
        text = font_type.render(message, True, font_color)
        screen.blit(text, (x, y))

    def get_input():
        global need_input1, input_text1, need_input2, input_text2, need_input3, input_text3

        input_rect1 = pygame.Rect(143, 115, 230, 25)
        input_rect2 = pygame.Rect(143, 165, 230, 25)
        input_rect3 = pygame.Rect(143, 215, 230, 25)

        pygame.draw.rect(screen, (255, 255, 255), input_rect1)
        pygame.draw.rect(screen, (255, 86, 0), (143, 115, 230, 25), 2)

        pygame.draw.rect(screen, (255, 255, 255), input_rect2)
        pygame.draw.rect(screen, (255, 86, 0), (143, 165, 230, 25), 2)

        pygame.draw.rect(screen, (255, 255, 255), input_rect3)
        pygame.draw.rect(screen, (255, 86, 0), (143, 215, 230, 25), 2)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if input_rect1.collidepoint(mouse[0], mouse[1]) and click[0] and not (need_input2 or need_input3):
            need_input1 = True
        if input_rect2.collidepoint(mouse[0], mouse[1]) and click[0] and not (need_input3 or need_input1):
            need_input2 = True
        if input_rect3.collidepoint(mouse[0], mouse[1]) and click[0] and not (need_input2 or need_input1):
            need_input3 = True

        if need_input1:
            for event1 in pygame.event.get():
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_RETURN:
                        need_input1 = False
                    elif event1.key == pygame.K_BACKSPACE:
                        input_text1 = input_text1[:-1]
                    else:
                        if len(input_text1) < 21:
                            input_text1 += event1.unicode
        if need_input2:
            for event2 in pygame.event.get():
                if event2.type == pygame.KEYDOWN:
                    if event2.key == pygame.K_RETURN:
                        need_input2 = False
                    elif event2.key == pygame.K_BACKSPACE:
                        input_text2 = input_text2[:-1]
                    else:
                        if len(input_text2) < 21:
                            input_text2 += event2.unicode
        if need_input3:
            for event3 in pygame.event.get():
                if event3.type == pygame.KEYDOWN:
                    if event3.key == pygame.K_RETURN:
                        need_input3 = False
                    elif event3.key == pygame.K_BACKSPACE:
                        input_text3 = input_text3[:-1]
                    else:
                        if len(input_text3) < 21:
                            input_text3 += event3.unicode

        if len(input_text1):
            print_text(input_text1, input_rect1.x + 10, input_rect1.y + 4, font_color=(0, 0, 0), font_size=25)
        if len(input_text2):
            print_text(input_text2, input_rect2.x + 10, input_rect2.y + 4, font_color=(0, 0, 0), font_size=25)
        if len(input_text3):
            print_text(input_text3, input_rect3.x + 10, input_rect3.y + 4, font_color=(0, 0, 0), font_size=25)

    def draw(screen):
        # общие настройки + авторизация
        # screen.fill((217, 217, 217))
        font = pygame.font.SysFont('arial', 45)
        text = font.render("Регистрация", False, (0, 255, 0))
        text_x, text_y = 135, 20
        screen.blit(text, (text_x, text_y))

        # размещение текста про логин
        font = pygame.font.SysFont("Segoe UI black", 15)
        text = font.render("Создайте логин:", True, (255, 170, 0))
        text_x, text_y = 10, 120
        screen.blit(text, (text_x, text_y))

        # размещение текста про пароль
        font = pygame.font.SysFont("Segoe UI black", 15)
        text = font.render("Создайте пароль:", True, (255, 170, 0))
        text_x, text_y = 5, 170
        screen.blit(text, (text_x, text_y))

        # размещение текста про повтор пароля
        font = pygame.font.SysFont("Segoe UI black", 14)
        text = font.render("Повторите пароль:", True, (255, 170, 0))
        text_x, text_y = 3, 220
        screen.blit(text, (text_x, text_y))

    # кнопка
    pygame.init()

    my_icon = pygame.image.load('data/logo.png')
    pygame.display.set_icon(my_icon)

    button = Buttons(130, 45, True, 32)
    button2 = Buttons(40, 40, in_c=(247, 104, 164), ac_c=(252, 174, 207))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                run = False
        pygame.display.set_caption('Registration')
        size = width, height = 450, 350
        screen = pygame.display.set_mode(size)

        bg = pygame.image.load("data/fon.jpg")
        screen.blit(bg, (0, 0))

        draw(screen)
        # рисуем кнопку
        button.draw(185, 265, "Сохранить")
        button2.draw(25, 25, 'A', xka=10, yka=7)

        pygame.draw.rect(screen, (255, 255, 255), (185, 265, 130, 45), 2)
        pygame.draw.rect(screen, (255, 255, 255), (25, 25, 40, 40), 2)

        get_input()
        print_text(tool_message, 5, 320, tool_color, font_size=30)
        pygame.display.flip()
    pygame.quit()


def aftorization():
    global tool_message, tool_color, need_input1, need_input2, need_input3, input_text3, input_text2, input_text1, run
    tool_color, tool_message = "blue", ''
    global running
    need_input1, input_text1, need_input2, input_text2 = False, '', False, ''

    class Buttons:
        def __init__(self, wid1, hei1, osob=False, fs=40, in_c=(20, 17, 237), ac_c=(134, 132, 232)):
            self.width, self.height = wid1, hei1
            self.inactive_color = in_c
            self.active_color = ac_c
            self.osob = osob
            self.fs = fs

        def draw(self, x, y, message, xka=20, yka=10):
            global running
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if x < mouse[0] < x + self.width:
                if y < mouse[1] < y + self.height:
                    pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
                    if click[0] == 1 and self.osob:
                        conbd()
                    elif click[0] == 1:
                        running = False
                else:
                    pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
            else:
                pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

            print_text(message, x + xka, y + yka, font_size=self.fs)

    def conbd():
        global input_text1, input_text2, tool_color, tool_message
        con = sqlite3.connect("Information_about_player.db")
        cur = con.cursor()
        result = cur.execute(f"""select id from users 
        where login = '{input_text1}' and password = '{input_text2}'""").fetchall()
        if result:
            tool_color, tool_message = "green", "Выполняю вход..."
            ex = Game_process(input_text1)
        else:
            tool_color, tool_message = "red", "Неверные данные"

    def print_text(message, x, y, font_color=(255, 255, 255), font_size=40):
        font_type = pygame.font.Font(None, font_size)
        text = font_type.render(message, True, font_color)
        screen.blit(text, (x, y))

    def get_input():
        global need_input1, input_text1, need_input2, input_text2

        input_rect1 = pygame.Rect(135, 115, 230, 25)
        input_rect2 = pygame.Rect(135, 197, 230, 25)
        pygame.draw.rect(screen, (255, 255, 255), input_rect1)
        pygame.draw.rect(screen, (255, 86, 0), (135, 115, 230, 25), 2)

        pygame.draw.rect(screen, (255, 255, 255), input_rect2)
        pygame.draw.rect(screen, (255, 86, 0), (135, 197, 230, 25), 2)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if input_rect1.collidepoint(mouse[0], mouse[1]) and click[0] and not need_input2:
            need_input1 = True
        if input_rect2.collidepoint(mouse[0], mouse[1]) and click[0] and not need_input1:
            need_input2 = True

        if need_input1:
            for event1 in pygame.event.get():
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_RETURN:
                        need_input1 = False
                    elif event1.key == pygame.K_BACKSPACE:
                        input_text1 = input_text1[:-1]
                    else:
                        if len(input_text1) < 21:
                            input_text1 += event1.unicode
        if need_input2:
            for event2 in pygame.event.get():
                if event2.type == pygame.KEYDOWN:
                    if event2.key == pygame.K_RETURN:
                        need_input2 = False
                    elif event2.key == pygame.K_BACKSPACE:
                        input_text2 = input_text2[:-1]
                    else:
                        if len(input_text2) < 21:
                            input_text2 += event2.unicode
        if len(input_text1):
            print_text(input_text1, input_rect1.x + 10, input_rect1.y + 4, font_color=(0, 0, 0), font_size=25)
        if len(input_text2):
            print_text(input_text2, input_rect2.x + 10, input_rect2.y + 4, font_color=(0, 0, 0), font_size=25)

    def draw(screen):
        # общие настройки + авторизация
        # screen.fill((214, 214, 214))
        font = pygame.font.SysFont('arial', 45)
        text = font.render("Авторизация", False, (0, 255, 0))
        text_x, text_y = 130, 20
        screen.blit(text, (text_x, text_y))

        # размещение текста про логин
        font = pygame.font.SysFont("Segoe UI black", 15)
        text = font.render("Введите логин:", True, (255, 170, 0))
        text_x, text_y = 5, 117
        screen.blit(text, (text_x, text_y))

        # размещение текста про пароль
        font = pygame.font.SysFont("Segoe UI black", 15)
        text = font.render("Введите пароль:", True, (255, 170, 0))
        text_x, text_y = 3, 197
        screen.blit(text, (text_x, text_y))

    # кнопка
    pygame.init()
    my_icon = pygame.image.load('data/logo.png')
    pygame.display.set_icon(my_icon)
    button = Buttons(120, 45, True)
    button2 = Buttons(40, 40, in_c=(40, 212, 180), ac_c=(30, 247, 207))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                run = False

        pygame.display.set_caption('Aftorization')
        size = width, height = 450, 350
        screen = pygame.display.set_mode(size)
        bg = pygame.image.load("data/fon.jpg")
        screen.blit(bg, (0, 0))
        draw(screen)
        # рисуем кнопку
        button.draw(180, 260, "ВХОД")
        button2.draw(25, 25, 'R', xka=10, yka=8)

        pygame.draw.rect(screen, (255, 254, 255), (180, 260, 120, 45), 2)
        pygame.draw.rect(screen, (255, 254, 255), (25, 25, 40, 40), 2)

        get_input()
        print_text(tool_message, 5, 320, tool_color, font_size=30)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    while run:
        if kto == 1:
            aftorization()
        else:
            registration()
        kto = -kto
