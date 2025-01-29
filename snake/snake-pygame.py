import pygame
from pygame.math import Vector2
import random
import sys

CELL_SIZE = 30
CELL_ROW, CELL_COL = 16, 16
SCREEN_WIDTH, SCREEN_HEIGHT = (CELL_SIZE * CELL_ROW), (CELL_SIZE * CELL_COL)

DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)

class Snake():
    def __init__(self):
        self.direction = Vector2(DIR_RIGHT)
        self.body = [
            Vector2(9, 10),
            Vector2(8, 10),
            Vector2(7, 10),
            Vector2(6, 10),
            Vector2(5, 10)
        ]
        self.new_block = False
    
    def draw(self):
        for index, block in enumerate(self.body):
            x_pos = (block.x * CELL_SIZE)
            y_pos = (block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            if index == 0:
                pygame.draw.rect(screen, (0, 255, 0), block_rect)
            else:
                pygame.draw.rect(screen, (0, 0, 255), block_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False 
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def extend(self):
        self.new_block = True


class Fruit():
    def __init__(self, snake):
        self.snake = snake
        self.regenerate()

    def draw(self):
        fruit_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

    def regenerate(self):
        while True:
            self.pos = Vector2(random.randint(0, CELL_ROW - 1), random.randint(0, CELL_COL - 1))
            if self.pos not in self.snake.body:
                break


class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit(self.snake)  # Pass the snake to Fruit

    def update(self):
        self.snake.move_snake()
        self.check_apple()
        self.check_collision()

    def draw_elements(self):
        self.fruit.draw()
        self.snake.draw()
    
    def check_apple(self):
        if self.fruit.pos == self.snake.body[0]:
            print("YUM")
            self.fruit.regenerate()
            self.snake.extend()

    def check_collision(self):
        # Check if snake hits the wall
        if not 0 <= self.snake.body[0].x < CELL_ROW or not 0 <= self.snake.body[0].y < CELL_COL:
            self.game_over()

        # Check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TEST")
clock = pygame.time.Clock()


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game = Game()

def draw_checkerboard():
    colors = [(255, 255, 255), (0, 0, 0)]
    for row in range(SCREEN_HEIGHT // CELL_SIZE):
        for col in range(SCREEN_WIDTH // CELL_SIZE):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if game.snake.direction.y != 1:
                    game.snake.direction = Vector2(DIR_UP)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if game.snake.direction.y != -1:
                    game.snake.direction = Vector2(DIR_DOWN)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if game.snake.direction.x != -1:
                    game.snake.direction = Vector2(DIR_RIGHT)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if game.snake.direction.x != 1:
                    game.snake.direction = Vector2(DIR_LEFT)



    draw_checkerboard()
    game.draw_elements()
    pygame.display.update()

    clock.tick(60)
