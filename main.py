import sqlite3
import pygame

tool_color, tool_message = "blue", ''
need_input1, input_text1, need_input2, input_text2 = False, '', False, ''
class Buttons:
    def __init__(self, wid1, hei1):
        self.width, self.height = wid1, hei1
        self.inactive_color = (20, 17, 237)
        self.active_color = (134, 132, 232)

    def draw(self, x, y, message):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
                if click[0] == 1:
                    conbd()
            else:
                pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        print_text(message, x + 20, y + 10)


def conbd():
    global input_text1, input_text2, tool_color, tool_message
    con = sqlite3.connect("data_meny1.db")
    cur = con.cursor()
    result = cur.execute(f"""select id from users 
    where login = '{input_text1}' and password = '{input_text2}'""").fetchall()
    if result:
        tool_color, tool_message = "green", "Выполняю вход..."
    else:
        tool_color, tool_message = "red", "Неверные данные"


def print_text(message, x, y, font_color=(255, 255, 255), font_size=40):
    font_type = pygame.font.Font(None, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def get_input():
    # поле ввода 1(логин)
    global need_input1, input_text1, need_input2, input_text2

    input_rect1 = pygame.Rect(130, 115, 230, 25)
    input_rect2 = pygame.Rect(130, 165, 230, 25)
    pygame.draw.rect(screen, (255, 255, 255), input_rect1)
    pygame.draw.rect(screen, (0, 0, 0), (130, 115, 230, 25), 1)

    pygame.draw.rect(screen, (255, 255, 255), input_rect2)
    pygame.draw.rect(screen, (0, 0, 0), (130, 165, 230, 25), 1)

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
         print_text(input_text1, input_rect1.x + 10, input_rect1.y + 4, font_color=(0, 0, 0),  font_size=25)
    if len(input_text2):
         print_text(input_text2, input_rect2.x + 10, input_rect2.y + 4, font_color=(0, 0, 0), font_size=25)


def draw(screen):
    # общие настройки + авторизация
    screen.fill((214, 214, 214))
    font = pygame.font.SysFont('arial', 45)
    text = font.render("Авторизация", True, (0, 0, 0))
    text_x, text_y = 100, 20
    screen.blit(text, (text_x, text_y))

    # размещение текста про логин
    font = pygame.font.Font(None, 20)
    text = font.render("Введите логин:", True, (0, 0, 0))
    text_x, text_y = 10, 120
    screen.blit(text, (text_x, text_y))

    #размещение текста про пароль
    font = pygame.font.Font(None, 20)
    text = font.render("Введите пароль:", True, (0, 0, 0))
    text_x, text_y = 7, 170
    screen.blit(text, (text_x, text_y))

    # изображение поля ввода 1 (логин)
   # screen.fill(pygame.Color("white"), (130, 115, 230, 25))
  #  pygame.draw.rect(screen, (0, 0, 0), (130, 115, 230, 25), 1)

    # изображение поля ввода 2 (пароль)
  #  screen.fill(pygame.Color("white"), (130, 165, 230, 25))
  #  pygame.draw.rect(screen, (0, 0, 0), (130, 165, 230, 25), 1)


if __name__ == '__main__':
    pygame.init()
    # кнопка
    button = Buttons(120, 45)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.set_caption('Aftorization')
        size = width, height = 450, 350
        screen = pygame.display.set_mode(size)
        draw(screen)
        #рисуем кнопку
        button.draw(170, 230, "ВХОД")
        pygame.draw.rect(screen, (0, 0, 0), (170, 230, 120, 45), 2)
        get_input()
        print_text(tool_message, 5, 320, tool_color, font_size=30)
        pygame.display.flip()
    pygame.quit()
