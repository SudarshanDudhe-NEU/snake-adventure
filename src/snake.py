import pygame
from constants import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, GREEN


class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.length = 1
        self.direction = pygame.K_RIGHT
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, new_direction):
        # Prevent the snake from reversing direction
        if (new_direction == pygame.K_UP and self.direction == pygame.K_DOWN) or \
           (new_direction == pygame.K_DOWN and self.direction == pygame.K_UP) or \
           (new_direction == pygame.K_LEFT and self.direction == pygame.K_RIGHT) or \
           (new_direction == pygame.K_RIGHT and self.direction == pygame.K_LEFT):
            return
        self.direction = new_direction

    def move(self):
        head_x, head_y = self.positions[0]

        if self.direction == pygame.K_UP:
            new_head = (head_x, head_y - 1)
        elif self.direction == pygame.K_DOWN:
            new_head = (head_x, head_y + 1)
        elif self.direction == pygame.K_LEFT:
            new_head = (head_x - 1, head_y)
        else:  # self.direction == pygame.K_RIGHT
            new_head = (head_x + 1, head_y)

        # Wrap around if the snake goes off the screen
        new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)

        # Check if snake collides with itself
        if new_head in self.positions[1:]:
            return True  # Game over

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

        return False  # Game continues

    def grow(self):
        self.length += 1
        self.score += 10

    def draw(self, surface):
        # Draw the body segments
        for i, position in enumerate(self.positions):
            if i == 0:  # This is the head
                # Draw a rounded rectangle for the head
                rect = pygame.Rect(
                    position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)

                # First draw the basic rectangle
                pygame.draw.rect(surface, self.color, rect)

                # Determine which side to round based on direction
                radius = GRID_SIZE // 2
                head_center = (position[0] * GRID_SIZE + GRID_SIZE // 2,
                               position[1] * GRID_SIZE + GRID_SIZE // 2)

                if self.direction == pygame.K_RIGHT:
                    pygame.draw.circle(surface, self.color,
                                       (position[0] * GRID_SIZE + GRID_SIZE,
                                        position[1] * GRID_SIZE + GRID_SIZE // 2),
                                       GRID_SIZE // 2)
                elif self.direction == pygame.K_LEFT:
                    pygame.draw.circle(surface, self.color,
                                       (position[0] * GRID_SIZE,
                                        position[1] * GRID_SIZE + GRID_SIZE // 2),
                                       GRID_SIZE // 2)
                elif self.direction == pygame.K_UP:
                    pygame.draw.circle(surface, self.color,
                                       (position[0] * GRID_SIZE + GRID_SIZE // 2,
                                        position[1] * GRID_SIZE),
                                       GRID_SIZE // 2)
                elif self.direction == pygame.K_DOWN:
                    pygame.draw.circle(surface, self.color,
                                       (position[0] * GRID_SIZE + GRID_SIZE // 2,
                                        position[1] * GRID_SIZE + GRID_SIZE),
                                       GRID_SIZE // 2)

                # Draw outline for head
                pygame.draw.rect(surface, (0, 200, 0), rect, 1)
            else:
                # Draw regular rectangles for the body
                rect = pygame.Rect(
                    position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, self.color, rect)
                pygame.draw.rect(surface, (0, 200, 0), rect, 1)
