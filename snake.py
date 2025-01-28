import curses
import random

class Snake(object):
    def __init__(self, init_body, init_direction):
        self.body = init_body
        self.direction = init_direction

    def head(self):
        return self.body[-1]
    
    def take_step(self, position):
        self.body = self.body[1:] + [position]

    def extend_body(self, position):
        self.body.append(position)

    def set_direction(self, direction):
        self.direction = direction

class Apple(object):
    def __init__(self, location):
        self.location = location

class Game:
    EMPTY = 0
    BODY = 1
    HEAD = 2
    APPLE = 3

    DISPLAY_CHARS = {
        EMPTY: " ",
        BODY: "O",
        HEAD: "X",
        APPLE: "*",
    }

    DIR_UP = (0, 1)
    DIR_DOWN = (0, -1)
    DIR_LEFT = (-1, 0)
    DIR_RIGHT = (1, 0)

    INPUT_CHAR_UP = "W"
    INPUT_CHAR_DOWN = "S"
    INPUT_CHAR_LEFT = "A"
    INPUT_CHAR_RIGHT = "D"

    def __init__(self, width, height):
        self.height = height
        self.width = width

        snake_body = [
            (0, 5),
            (1, 5),
            (2, 5),
            (3, 5),
            (4, 5),
        ]

        self.snake = Snake(snake_body, self.DIR_RIGHT)
        self.current_apple = None
        self.regenerate_apple()
    
    def play(self):
        self.regenerate_apple
        self.render()
        while True:
            ch = input("").upper()

            if ch == self.INPUT_CHAR_UP and self.snake.direction != self.DIR_DOWN:
                self.snake.set_direction(self.DIR_UP)
            elif ch == self.INPUT_CHAR_DOWN and self.snake.direction != self.DIR_UP:
                self.snake.set_direction(self.DIR_DOWN)
            elif ch == self.INPUT_CHAR_LEFT and self.snake.direction != self.DIR_RIGHT:
                self.snake.set_direction(self.DIR_LEFT)
            elif ch == self.INPUT_CHAR_RIGHT and self.snake.direction != self.DIR_LEFT:
                self.snake.set_direction(self.DIR_RIGHT)

            next_position = self.next_position(self.snake.head(), self.snake.direction)
            if next_position in self.snake.body:
                break

            if next_position == self.current_apple.location:
                self.snake.extend_body(next_position)
                self.regenerate_apple()
            else:
                self.snake.take_step(next_position)
            
            self.render()

    def board_matrix(self):
        matrix = [[self.EMPTY for _ in range(self.height)] for _ in range(self.width)]
        for co in self.snake.body:
            matrix[co[0]][co[1]] = self.BODY

        head = self.snake.head()
        matrix[head[0]][head[1]] = self.HEAD

        apple_location = self.current_apple.location
        matrix[apple_location[0]][apple_location[1]] = self.APPLE

        return matrix
    
    def render(self):
        matrix = self.board_matrix()

        top_bottom_border = "+" + "-" * (self.width) + "+"
        print(top_bottom_border)
        for y in range(0, self.height):
            line = "|"
            for x in range(0, self.width):
                cell_val = matrix[x][self.height-1-y]
                line += self.DISPLAY_CHARS[cell_val]
            line += "|"
            print(line)
        print(top_bottom_border)

        # Print matrix row by row with formatted elements and side borders

    def next_position(self, position, step):
        return (
            (position[0] + step[0]) % self.width,
            (position[1] + step[1]) % self.height
        )
    
    def regenerate_apple(self):
        while True:
            new_apple_location = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
            )
            if new_apple_location not in self.snake.body:
                break
        
        self.current_apple = Apple(new_apple_location)

game = Game(30, 10)
game.play()