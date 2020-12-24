import pygame
import sys
import random
from pygame.math import Vector2

# Constants for colors, cell size and number
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
cell_size = 40
cell_number = 20

# Initializing pygame and naming display
pygame.init()
pygame.display.set_caption("Snake")

# Setting up clock and screen constants
clock = pygame.time.Clock()
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

# Classes for players and new fruit, along with main gameplay
class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_obj(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, black, fruit_rect)

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)
        self.add_block = False

    def draw_obj(self):
        for block in self.body:
            snake_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, black, snake_rect)

    def move_snake(self):
        if self.add_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.add_block = False
        else:
            if len(self.body) > 1:
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]
            else:
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[0]

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()

    def draw_objs(self):
        self.fruit.draw_obj()
        self.snake.draw_obj()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            while self.fruit.pos in self.snake.body:
                self.fruit.pos = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
            self.score += 1
            self.snake.add_block = True

        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


# Main game function creator and updating elements timer
main_loop = Main()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Main game loop
while True:
    # Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_loop.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_loop.snake.direction.y != 1:
                main_loop.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_loop.snake.direction.y != -1:
                main_loop.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT and main_loop.snake.direction.x != -1:
                main_loop.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT and main_loop.snake.direction.x != 1:
                main_loop.snake.direction = Vector2(-1, 0)

    # Setting background color
    screen.fill((89, 212, 154))

    # Draws the objects every iteration
    main_loop.draw_objs()

    # Updating display and setting frame rate
    pygame.display.update()
    clock.tick(60)