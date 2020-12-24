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

# Classes for players
class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_obj(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, black, fruit_rect)

fruit = Fruit()

# Main game loop
while True:
    # Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Setting background color
    screen.fill((89, 212, 154))

    fruit.draw_obj()

    # Updating display and setting frame rate
    pygame.display.update()
    clock.tick(60)