import random
import pygame
from constants import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = self.generate_random_color()
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1),
                         random.randint(0, GRID_HEIGHT - 1))

    def generate_random_color(self):
        """Generate a bright, vibrant color"""
        # Ensure at least one component is bright (> 200)
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)

        # Make sure at least one component is very bright
        brightest = random.randint(0, 2)
        if brightest == 0:
            r = random.randint(200, 255)
        elif brightest == 1:
            g = random.randint(200, 255)
        else:
            b = random.randint(200, 255)

        return (r, g, b)

    def new_food(self):
        """Create new food with new color and position"""
        self.color = self.generate_random_color()
        self.randomize_position()

    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE,
                           self.position[1] * GRID_SIZE,
                           GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (min(255, self.color[0] + 50),
                                   min(255, self.color[1] + 50),
                                   min(255, self.color[2] + 50)), rect, 1)
