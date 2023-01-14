from random import choice


abscissa_dimension, ordinate_dimension, labyrinth_field = 0, 0, []


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


def labyrinth_recoding():
    return [[cell.recoding() for cell in labyrinth_field[i * abscissa_dimension:(i + 1) * abscissa_dimension]]
            for i in range(ordinate_dimension)]


def transferring_variables(abscissa, ordinate, labyrinth):
    global abscissa_dimension, ordinate_dimension, labyrinth_field
    abscissa_dimension, ordinate_dimension, labyrinth_field = abscissa, ordinate, labyrinth


def remove_walls(current, next):
    delta_x = current.x - next.x
    if delta_x == 1:
        current.walls[3] = 0
        next.walls[1] = 0
    elif delta_x == -1:
        current.walls[1] = 0
        next.walls[3] = 0
    delta_y = current.y - next.y
    if delta_y == 1:
        current.walls[0] = 0
        next.walls[2] = 0
    elif delta_y == -1:
        current.walls[2] = 0
        next.walls[0] = 0
