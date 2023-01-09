import sqlite3
import pygame

need_input, input_text = False, '|'
input_tick = 30


class Buttons:
    def __init__(self, wid1, hei1):
        self.width, self.height = wid1, hei1
        self.inactive_color = (20, 17, 237)
        self.active_color = (134, 132, 232)

    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
                if click[0] == 1 and action is not None:
                    action()
            else:
                pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        print_text(message, x + 20, y + 10)


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
    # pygame.draw.rect(screen, (0, 0, 0), (130, 115, 230, 25), 1)

    # изображение поля ввода 2 (пароль)
    screen.fill(pygame.Color("white"), (130, 165, 230, 25))
    pygame.draw.rect(screen, (0, 0, 0), (130, 165, 230, 25), 1)
    # рамка кнопки


def print_text(message, x, y, font_color=(255, 255, 255), font_size=40, bl=False):
    font_type = pygame.font.Font(None, font_size)
    text = font_type.render(message, bl, font_color)
    screen.blit(text, (x, y))


def get_input():
    # поле ввода 1(логин)
    global need_input, input_text, input_tick
    input_rect1 = pygame.Rect(130, 115, 230, 25)
    pygame.draw.rect(screen, (255, 255, 255), input_rect1)
    pygame.draw.rect(screen, (0, 0, 0), (130, 115, 230, 25), 1)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if input_rect1.collidepoint(mouse[0], mouse[1]) and click[0]:
        need_input = True
    if need_input:
        for event in pygame.event.get():
            if need_input and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    need_input = False
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    a = input_text[-1]
                    input_text = input_text[:-2]
                    input_text += a
                else:
                    if len(input_text) < 15:
                        a = input_text[-1]
                        input_text = input_text[:-1]
                        input_text += event.unicode + a
    if len(input_text):
        print_text(input_text, input_rect1.x + 10, input_rect1.y + 4, font_color=(0, 0, 0),  font_size=25, bl=True)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Aftorization')
    size = width, height = 450, 350
    screen = pygame.display.set_mode(size)
    draw(screen)
    pygame.display.flip()
    # кнопка
    button = Buttons(120, 45)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #рисуем кнопку
        button.draw(170, 230, "ВХОД")
        pygame.draw.rect(screen, (0, 0, 0), (170, 230, 120, 45), 2)

        get_input()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            need_input = True
        print_text(input_text, 500, 400)
        pygame.display.flip()
    pygame.quit()
