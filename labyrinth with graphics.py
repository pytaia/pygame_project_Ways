import pygame
from random import choice, randrange


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = [1, 1, 1, 1]
        self.visited = False

    def draw_current_cell(self):
        x, y = self.x * pixel_dimensions, self.y * pixel_dimensions
        pygame.draw.rect(sc, pygame.Color('saddlebrown'), (x + 2, y + 2, pixel_dimensions - 2, pixel_dimensions - 2))

    def draw(self):
        x, y = self.x * pixel_dimensions, self.y * pixel_dimensions
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, pixel_dimensions, pixel_dimensions))

        if self.walls[0]:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + pixel_dimensions, y), 3)
        if self.walls[1]:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + pixel_dimensions, y),
                             (x + pixel_dimensions, y + pixel_dimensions), 3)
        if self.walls[2]:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + pixel_dimensions, y + pixel_dimensions),
                             (x, y + pixel_dimensions), 3)
        if self.walls[3]:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + pixel_dimensions), (x, y), 3)

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * abscissa_dimension
        if x < 0 or x > abscissa_dimension - 1 or y < 0 or y > ordinate_dimension - 1:
            return False
        return labyrinth_field[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

    def recoding(self):
        return int(''.join(map(str, self.walls)), 2)


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls[3] = 0
        next.walls[1] = 0
    elif dx == -1:
        current.walls[1] = 0
        next.walls[3] = 0
    dy = current.y - next.y
    if dy == 1:
        current.walls[0] = 0
        next.walls[2] = 0
    elif dy == -1:
        current.walls[2] = 0
        next.walls[0] = 0


abscissa_dimension, ordinate_dimension = list(map(int, input().split()))
pixel_dimensions = 30

pygame.init()
sc = pygame.display.set_mode(pixel_dimensions * abscissa_dimension + 2, pixel_dimensions * ordinate_dimension + 2)
clock = pygame.time.Clock()

labyrinth_field = [Cell(col, row) for row in range(ordinate_dimension) for col in range(abscissa_dimension)]
current_cell = labyrinth_field[randrange(abscissa_dimension * ordinate_dimension)]
stack = []
color = [255, 255, 255]
stack_count = 1
sch = True

while True:
    if ordinate_dimension * abscissa_dimension == stack_count and sch:
        print([[cell.recoding() for cell in labyrinth_field[i * abscissa_dimension:(i + 1) * abscissa_dimension]]
               for i in range(ordinate_dimension)])
        sch = False

    sc.fill(pygame.Color('darkslategray'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [cell.draw() for cell in labyrinth_field]
    current_cell.visited = True
    current_cell.draw_current_cell()
    [pygame.draw.rect(sc, color, (cell.x * pixel_dimensions + 2, cell.y * pixel_dimensions + 2,
                                      pixel_dimensions - 4, pixel_dimensions - 4)) for i, cell in enumerate(stack)]

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        stack_count += 1
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    pygame.display.flip()
    clock.tick(30)
