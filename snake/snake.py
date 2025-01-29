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
        BODY: "█",
        HEAD: "█",
        APPLE: "o",
    }

    DIR_UP = (0, 1)
    DIR_DOWN = (0, -1)
    DIR_LEFT = (-1, 0)
    DIR_RIGHT = (1, 0)

    INPUT_CHAR_UP = 119
    INPUT_CHAR_DOWN = 115
    INPUT_CHAR_LEFT = 97
    INPUT_CHAR_RIGHT = 100

    GAME_SPEED = 170
    GAME_SCORE = 0

    def __init__(self, width, height):
        self.height = height
        self.width = width

        # initialize snake position
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
        try:
            curses.wrapper(self.curses_play)
        except KeyboardInterrupt:
            exit(0)

    def curses_play(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(self.GAME_SPEED)

        # Initialize color pairs
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Green color pair for snake

        self.stdscr = stdscr
        self.regenerate_apple()
        self.render()

        while True:
            ch = stdscr.getch()
            if ch != -1:
            # Handle both letter keys and arrow keys
                if ch == curses.KEY_UP and self.snake.direction != self.DIR_DOWN:
                    self.snake.set_direction(self.DIR_UP)
                elif ch == curses.KEY_DOWN and self.snake.direction != self.DIR_UP:
                    self.snake.set_direction(self.DIR_DOWN)
                elif ch == curses.KEY_LEFT and self.snake.direction != self.DIR_RIGHT:
                    self.snake.set_direction(self.DIR_LEFT)
                elif ch == curses.KEY_RIGHT and self.snake.direction != self.DIR_LEFT:
                    self.snake.set_direction(self.DIR_RIGHT)

                elif ch == self.INPUT_CHAR_UP and self.snake.direction != self.DIR_DOWN:
                    self.snake.set_direction(self.DIR_UP)
                elif ch == self.INPUT_CHAR_DOWN and self.snake.direction != self.DIR_UP:
                    self.snake.set_direction(self.DIR_DOWN)
                elif ch == self.INPUT_CHAR_LEFT and self.snake.direction != self.DIR_RIGHT:
                    self.snake.set_direction(self.DIR_LEFT)
                elif ch == self.INPUT_CHAR_RIGHT and self.snake.direction != self.DIR_LEFT:
                    self.snake.set_direction(self.DIR_RIGHT)



            next_position = self.next_position(self.snake.head(), self.snake.direction)
            # check if the snake hits the wall
            if next_position[0] < 0 or next_position[0] >= self.width or next_position[1] < 0 or next_position[1] >= self.height:
                print("\nGame Over!")
                print(f"Final Score: {self.GAME_SCORE}")
                break
            # check if the snake hits itself
            if next_position in self.snake.body:
                print("\nGame Over!")
                print(f"Final Score: {self.GAME_SCORE}")
                break

            # check if the snake eats the apple
            if next_position == self.current_apple.location:
                self.snake.extend_body(next_position)
                self.regenerate_apple()
                self.GAME_SCORE += 10
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
        self.stdscr.clear()
        matrix = self.board_matrix()

        WALL_VERTICAL = "│"
        WALL_HORIZONTAL = "─"

        TOP_BOTTOM_BORDER = "+" + WALL_HORIZONTAL * self.width + "+" 
        TOP_BORDER = "┌" + WALL_HORIZONTAL * self.width + "┐"
        BOTTOM_BORDER = "└" + WALL_HORIZONTAL * self.width + "┘"

        # Get terminal size
        term_height, term_width = self.stdscr.getmaxyx()

        start_y = (term_height - (self.height + 2)) // 2
        start_x = (term_width - (self.width + 2)) // 2

        # Add game score
        self.stdscr.addstr(start_y - 1, start_x, ("SCORE:" + str(self.GAME_SCORE)))

        # Draw top border
        self.stdscr.addstr(start_y, start_x, TOP_BORDER)

        # Draw game area with side borders
        for y in range(self.height):
            self.stdscr.addch(start_y + y + 1, start_x, WALL_VERTICAL)
            for x in range(self.width):
                cell_val = matrix[x][self.height-1-y]
                if cell_val == self.APPLE:
                    self.stdscr.addch(start_y + y + 1, start_x + x + 1, self.DISPLAY_CHARS[cell_val], curses.color_pair(1))
                elif cell_val in (self.BODY, self.HEAD):
                    self.stdscr.addch(start_y + y + 1, start_x + x + 1, self.DISPLAY_CHARS[cell_val], curses.color_pair(2))
                else:
                    self.stdscr.addch(start_y + y + 1, start_x + x + 1, self.DISPLAY_CHARS[cell_val])
            self.stdscr.addch(start_y + y + 1, start_x + self.width + 1, WALL_VERTICAL)

        # Draw bottom border
        self.stdscr.addstr(start_y + self.height + 1, start_x, BOTTOM_BORDER)
        self.stdscr.addstr(start_y + self.height + 2, start_x, "CONTROLS: W/↑ S/↓ A/← D/→")

        self.stdscr.refresh()

    def next_position(self, position, step):
        return (
            position[0] + step[0],
            position[1] + step[1],
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
print(f"Game Over! Your Score: {game.GAME_SCORE}")