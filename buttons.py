import pygame


class Buttons:
    def __init__(self, wid1, hei1, go=None):
        self.width, self.height = wid1, hei1
        # цвет можно задать какой угодно
        self.inactive_color = (20, 17, 237)
        self.active_color = (134, 132, 232)

    def draw(self, x, y, message):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
                if click[0] == 1:
                    go()
            else:
                pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        print_text(message, x + 35, y + 14)


def print_text(message, x, y, font_color=(255, 255, 255), font_size=30):
    font_type = pygame.font.Font(None, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def draw(screen):
    # общие настройки + авторизация
    screen.fill((214, 214, 214))
    font = pygame.font.SysFont('arial', 45)
    text = font.render("Добро пожаловать!", True, (0, 0, 0))
    text_x, text_y = 60, 20
    screen.blit(text, (text_x, text_y))


if __name__ == '__main__':
    pygame.init()
    # кнопка
    button_continue = Buttons(210, 45)
    button_n_game = Buttons(210, 45)
    button_close = Buttons(150, 45)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.set_caption('Aftorization')
        size = width, height = 450, 350
        screen = pygame.display.set_mode(size)
        draw(screen)
        # рисуем кнопку 1
        button_continue.draw(20, 200, "ПРОДОЛЖИТЬ")
        pygame.draw.rect(screen, (0, 0, 0), (20, 200, 210, 45), 2)
        # рисуем кнопку 2
        button_n_game.draw(120, 110, "НОВАЯ ИГРА")
        pygame.draw.rect(screen, (0, 0, 0), (120, 110, 210, 45), 2)
        # рисуем кнопку 3
        button_close.draw(260, 200, "ВЫХОД")
        pygame.draw.rect(screen, (0, 0, 0), (260, 200, 150, 45), 2)
        pygame.display.flip()
    pygame.quit()
