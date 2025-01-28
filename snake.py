import curses
import random

class Snake:
    def __init__(self, init_body, init_direction):
        self.body = init_body
        self.direction = init_direction

    def take_step(self, position):
        self.body = self.body[1:] + [position]

    def set_direction(self, direction):
        self.direction = direction

    def head(self):
        return self.body[-1]

class Apple:
    pass

class Game:
    DIR_UP = (0, 1)
    DIR_DOWN = (0, -1)
    DIR_LEFT = (-1, 0)
    DIR_RIGHT = (1, 0)

    INPUT_CHAR_UP = 'W'
    INPUT_CHAR_DOWN = 'S'
    INPUT_CHAR_LEFT = 'A'
    INPUT_CHAR_RIGHT = 'D'

    def __init__(self, width, height):
        self.height = height
        self.width = width

        snake_body = [
            (5, 5),
            (4, 5),
            (3, 5),
            (2, 5),
            (1, 5),
        ]

        self.snake = Snake(snake_body, self.DIR_UP)
    
    def play(self):
        self.render()
        while True:
            ch = input("").upper()

            if ch == self.INPUT_CHAR_UP and self.snake.direction != self.DIR_DOWN:
                self.snake.set_direction(self.DIR_UP)

    def board_matrix(self):
        return [[None for _ in range(self.width)] for _ in range(self.height)]

    def render(self):
        print(f"Height: {self.height}")
        print(f"Width: {self.width}")
        matrix = self.board_matrix()

        # Print top border
        print("+" + "-" * (self.width) + "+")

        for i, segment in enumerate(self.snake.body):
            x, y = segment
            if i == 0:
                matrix[y][x] = 'X'
            else:
                matrix[y][x] = 'O'

        # Print matrix row by row with formatted elements and side borders
        for row in matrix:
            # print("|" + " ".join(f"{str(cell):4}" for cell in row) + "|")
            print("|" + "".join(f"{' ' if cell is None else str(cell)}" for cell in row) + "|")

        # Print bottom border
        print("+" + "-" * (self.width) + "+")

game = Game(30, 10)
game.render()

