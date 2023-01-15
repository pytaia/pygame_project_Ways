import pygame
from labyrinth_generation import Cell, remove_walls, transferring_variables
import sys
from random import randrange
import sqlite3
import time
import os


class Game_process:
    def __init__(self, login):
        self.login = login
        self.global_game_state = True
        pygame.init()
        pygame.font.init()
        self.procedure_generation()
        self.screen = pygame.display.set_mode([700, 500])
        self.screen.fill(pygame.Color('white'))
        pygame.display.set_caption('Ways')
        self.graphics_loading()
        self.game_board_logic()

    def procedure_generation(self):
        self.Informational_console_open()
        self.abscissa_dimension = min(70, max(7, self.Information_base_console.execute(
            'SELECT level FROM users WHERE login like "{}"'.format(self.login)).fetchall()[0][0]))
        self.ordinate_dimension = self.abscissa_dimension

        self.labyrinth_field = [Cell(col, row) for row in range(self.ordinate_dimension) for col in
                           range(self.abscissa_dimension)]
        transferring_variables(self.abscissa_dimension, self.ordinate_dimension, self.labyrinth_field)
        current_cell = self.labyrinth_field[0]
        stack = []
        stack_count = 1

        while self.ordinate_dimension * self.abscissa_dimension != stack_count:
            current_cell.visited = True
            next_cell = current_cell.check_neighbors()
            if next_cell:
                next_cell.visited = True
                stack.append(current_cell)
                stack_count += 1
                remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif stack:
                current_cell = stack.pop()

        self.labyrinth_field = [
            [cell for cell in self.labyrinth_field[i * self.abscissa_dimension:(i + 1) * self.abscissa_dimension]]
            for i in range(self.ordinate_dimension)]
        self.Informational_console_close()

    def graphics_loading(self):
        self.Informational_console_open()
        self.screen.blit(self.load_image('fon_game.jpg'), (200, 0))
        pygame.draw.rect(self.screen, [255, 255, 255], [(530, 180), (145, 100)])
        pygame.draw.rect(self.screen, [0, 0, 0], [(540, 185), (125, 50)], 2)
        pygame.draw.rect(self.screen, [255, 255, 255], [(0, 0), (500, 500)])
        first_text = pygame.font.Font(None, 36)
        second_text = pygame.font.Font(None, 20)
        self.third_text = pygame.font.Font(None, 16)
        level_text = first_text.render('Level: {}'.format(self.Information_base_console.execute(
            'SELECT level FROM users WHERE login like "{}"'.format(self.login)).fetchall()[0][0]), True, (255, 0, 0))
        login_text = second_text.render('{}'.format(self.login), True, (0, 0, 0))
        self.screen.blit(level_text, (550, 200))
        self.screen.blit(login_text, (580, 250))
        self.Informational_console_close()

    def load_image(self, name):
        return pygame.image.load(os.path.join('data', name))

    def game_board_logic(self):
        pixel_dimensions = max(500 // self.abscissa_dimension, 500 // self.ordinate_dimension)
        start_positional = [self.ordinate_dimension // 2 + 1, self.abscissa_dimension // 2 + 1]
        keys_positional = [randrange(self.abscissa_dimension), randrange(self.ordinate_dimension)]
        permission = 1

        pygame.draw.rect(self.screen, [0, 0, 0], [(0, 0), (500, 500)], 3)
        time.perf_counter()
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                delta_walls = self.labyrinth_field[start_positional[1]][start_positional[0]].walls
                old_positional = start_positional.copy()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if keys[pygame.K_a] and not delta_walls[3] and permission:
                    start_positional[0] = max(0, start_positional[0] - 1)
                    permission -= 1
                if keys[pygame.K_d] and not delta_walls[1] and permission:
                    start_positional[0] = min(self.abscissa_dimension, start_positional[0] + 1)
                    permission -= 1
                if keys[pygame.K_w] and not delta_walls[0] and permission:
                    start_positional[1] = max(0, start_positional[1] - 1)
                    permission -= 1
                if keys[pygame.K_s] and not delta_walls[2] and permission:
                    start_positional[1] = min(self.ordinate_dimension, start_positional[1] + 1)
                    permission -= 1
                if start_positional == keys_positional:
                    self.Informational_console_open()

                    self.Information_base_cursore.execute(
                        'UPDATE users SET level = level + 1 WHERE login like "{}"'.format(self.login))

                    self.Informational_console_close()
                    start()

                pygame.draw.circle(self.screen, [255, 255, 255], [(0.5 + old_positional[0]) * pixel_dimensions,
                                                                  (0.5 + old_positional[1]) * pixel_dimensions],
                                   pixel_dimensions // 3)
            pygame.draw.circle(self.screen, [48, 213, 200], [(0.5 + start_positional[0]) * pixel_dimensions,
                                                             (0.5 + start_positional[1]) * pixel_dimensions],
                               pixel_dimensions // 3)
            pygame.draw.circle(self.screen, [0, 255, 0], [(0.5 + keys_positional[0]) * pixel_dimensions,
                                                          (0.5 + keys_positional[1]) * pixel_dimensions],
                               pixel_dimensions // 3)

            [cell.draw(self.screen, pixel_dimensions) for index_row, cell_row in enumerate(self.labyrinth_field) for
             index, cell in enumerate(cell_row) if max(0, start_positional[0] - 2) <= index <=
             max(0, start_positional[0] + 2) and max(0, start_positional[1] - 2) <= index_row <=
             max(0, start_positional[1] + 2)]
            permission = 1

            pygame.display.flip()

    def Informational_console_open(self):
        self.Information_base_console = sqlite3.connect("Information_about_player.db")
        self.Information_base_cursore = self.Information_base_console.cursor()

    def Informational_console_close(self):
        self.Information_base_console.commit()
        self.Information_base_cursore.close()


def start():
    ex = Game_process('admin')
