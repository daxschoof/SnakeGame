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

# Adding Graphics
apple = pygame.image.load('Graphics/apple.png').convert_alpha()

# Classes for players and new fruit, along with main gameplay
class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_obj(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)
        self.add_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_obj(self):
        for index, block in enumerate(self.body):
            snake_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)

            if index == 0:
                head_relation = self.body[1] - self.body[0]
                if head_relation == Vector2(1, 0): self.head = self.head_left
                elif head_relation == Vector2(-1, 0): self.head = self.head_right
                elif head_relation == Vector2(0, 1): self.head = self.head_up
                elif head_relation == Vector2(0, -1): self.head = self.head_down
                screen.blit(self.head, snake_rect)
            elif index == len(self.body) - 1:
                tail_relation = self.body[-2] - self.body[-1]
                if tail_relation == Vector2(1, 0): self.tail = self.tail_left
                elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
                elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
                elif tail_relation == Vector2(0, -1): self.tail = self.tail_down
                screen.blit(self.tail, snake_rect)
            else:
                last = self.body[index + 1] - block
                next = self.body[index - 1] - block
                if last.x == next.x:
                    screen.blit(self.body_vertical, snake_rect)
                elif last.y == next.y:
                    screen.blit(self.body_horizontal, snake_rect)
                else:
                    if last.x == -1 and next.y == -1 or last.y == -1 and next.x == -1: screen.blit(self.body_tl, snake_rect)
                    elif last.x == -1 and next.y == 1 or last.y == 1 and next.x == -1: screen.blit(self.body_bl, snake_rect)
                    elif last.x == 1 and next.y == -1 or last.y == -1 and next.x == 1: screen.blit(self.body_tr, snake_rect)
                    elif last.x == 1 and next.y == 1 or last.y == 1 and next.x == 1: screen.blit(self.body_br, snake_rect)

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
        self.draw_grass()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for col in range(cell_number):
            for row in range(cell_number):
                grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, grass_color, grass_rect)

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