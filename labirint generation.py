from random import choice, randrange


abscissa_dimension, ordinate_dimension = list(map(int, input().split()))


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = [1, 1, 1, 1]
        self.visited = False

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


labyrinth_field = [Cell(col, row) for row in range(ordinate_dimension) for col in range(abscissa_dimension)]
current_cell = labyrinth_field[randrange(abscissa_dimension * ordinate_dimension)]
stack = []
stack_count = 1

while ordinate_dimension * abscissa_dimension != stack_count:
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

print([[cell.recoding() for cell in labyrinth_field[i * abscissa_dimension:(i + 1) * abscissa_dimension]]
       for i in range(ordinate_dimension)])
