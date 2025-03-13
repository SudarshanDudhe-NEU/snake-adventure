import pygame
import math
from constants import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT


class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.length = 1
        self.direction = pygame.K_RIGHT
        self.color = (0, 255, 0)  # Start with green
        self.score = 0

    def change_color(self, new_color):
        """Update the snake color"""
        self.color = new_color

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

    def draw_eyes(self, surface, head_pos, direction):
        """Draw eyes on the snake's head based on direction"""
        # Calculate eye positions based on direction
        left_eye_pos = None
        right_eye_pos = None
        eye_radius = max(2, GRID_SIZE // 6)
        pupil_radius = max(1, eye_radius // 2)

        # Base eye positions depend on direction
        if direction == pygame.K_RIGHT:
            # Eyes on the right side
            eye_y = head_pos[1] * GRID_SIZE + GRID_SIZE // 3
            left_eye_pos = (head_pos[0] * GRID_SIZE +
                            GRID_SIZE - eye_radius, eye_y)
            right_eye_pos = (
                head_pos[0] * GRID_SIZE + GRID_SIZE - eye_radius, eye_y + GRID_SIZE // 3)
        elif direction == pygame.K_LEFT:
            # Eyes on the left side
            eye_y = head_pos[1] * GRID_SIZE + GRID_SIZE // 3
            left_eye_pos = (head_pos[0] * GRID_SIZE + eye_radius, eye_y)
            right_eye_pos = (head_pos[0] * GRID_SIZE +
                             eye_radius, eye_y + GRID_SIZE // 3)
        elif direction == pygame.K_UP:
            # Eyes on the top
            eye_x = head_pos[0] * GRID_SIZE + GRID_SIZE // 3
            left_eye_pos = (eye_x, head_pos[1] * GRID_SIZE + eye_radius)
            right_eye_pos = (eye_x + GRID_SIZE // 3,
                             head_pos[1] * GRID_SIZE + eye_radius)
        elif direction == pygame.K_DOWN:
            # Eyes on the bottom
            eye_x = head_pos[0] * GRID_SIZE + GRID_SIZE // 3
            left_eye_pos = (
                eye_x, head_pos[1] * GRID_SIZE + GRID_SIZE - eye_radius)
            right_eye_pos = (eye_x + GRID_SIZE // 3,
                             head_pos[1] * GRID_SIZE + GRID_SIZE - eye_radius)

        # Draw the eyes (white part)
        if left_eye_pos and right_eye_pos:
            # Make eyes white with a slight color tint from snake
            eye_color = (220, 220, 220)
            pygame.draw.circle(surface, eye_color, left_eye_pos, eye_radius)
            pygame.draw.circle(surface, eye_color, right_eye_pos, eye_radius)

            # Draw pupils (black dot in the center of each eye)
            pupil_color = (0, 0, 0)
            pygame.draw.circle(surface, pupil_color,
                               left_eye_pos, pupil_radius)
            pygame.draw.circle(surface, pupil_color,
                               right_eye_pos, pupil_radius)

    def draw_scales(self, surface, position, i):
        """Draw scales on the snake body segment"""
        rect = pygame.Rect(position[0] * GRID_SIZE,
                           position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)

        # Base color for the segment
        pygame.draw.rect(surface, self.color, rect)

        # Slightly lighter color for scales
        scale_color = (
            min(255, self.color[0] + 30),
            min(255, self.color[1] + 30),
            min(255, self.color[2] + 30)
        )

        # Slightly darker outline color
        outline_color = (
            max(0, self.color[0] - 50),
            max(0, self.color[1] - 50),
            max(0, self.color[2] - 50)
        )

        # Draw scales differently based on position in the snake
        scale_pattern = (i // 2) % 2  # Alternating pattern
        x = position[0] * GRID_SIZE
        y = position[1] * GRID_SIZE

        # Scale size
        scale_size = max(3, GRID_SIZE // 4)

        # Draw scales in a pattern
        if scale_pattern == 0:
            # Pattern A: diagonal scales
            pygame.draw.ellipse(surface, scale_color,
                                (x + GRID_SIZE // 4, y + GRID_SIZE // 4,
                                 scale_size, scale_size))
            pygame.draw.ellipse(surface, scale_color,
                                (x + GRID_SIZE // 2, y + GRID_SIZE // 2,
                                 scale_size, scale_size))
        else:
            # Pattern B: alternate diagonal
            pygame.draw.ellipse(surface, scale_color,
                                (x + GRID_SIZE // 2, y + GRID_SIZE // 4,
                                 scale_size, scale_size))
            pygame.draw.ellipse(surface, scale_color,
                                (x + GRID_SIZE // 4, y + GRID_SIZE // 2,
                                 scale_size, scale_size))

        # Draw outline
        pygame.draw.rect(surface, outline_color, rect, 1)

    def draw_tail(self, surface, position, prev_position):
        """Draw a tapered tail at the end of the snake"""
        # Get the position of the tail segment
        x = position[0] * GRID_SIZE
        y = position[1] * GRID_SIZE

        # Determine the direction of the tail based on the previous segment
        direction = None
        if prev_position[0] > position[0]:  # Tail is to the left of prev segment
            direction = "right"  # Tail points right
        elif prev_position[0] < position[0]:  # Tail is to the right of prev segment
            direction = "left"  # Tail points left
        elif prev_position[1] > position[1]:  # Tail is above prev segment
            direction = "down"  # Tail points down
        else:  # Tail is below prev segment
            direction = "up"  # Tail points up

        # Draw the base of the tail (attaches to the previous segment)
        rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)

        # Draw the tapered part of the tail
        if direction == "right":
            # Draw a triangle pointing right
            points = [
                (x + GRID_SIZE, y),                     # Top right
                (x + GRID_SIZE, y + GRID_SIZE),         # Bottom right
                (x + GRID_SIZE // 2, y + GRID_SIZE // 2)  # Middle left
            ]
            pygame.draw.polygon(surface, self.color, points)
        elif direction == "left":
            # Draw a triangle pointing left
            points = [
                (x, y),                     # Top left
                (x, y + GRID_SIZE),         # Bottom left
                (x + GRID_SIZE // 2, y + GRID_SIZE // 2)  # Middle right
            ]
            pygame.draw.polygon(surface, self.color, points)
        elif direction == "up":
            # Draw a triangle pointing up
            points = [
                (x, y),                     # Top left
                (x + GRID_SIZE, y),         # Top right
                (x + GRID_SIZE // 2, y + GRID_SIZE // 2)  # Middle bottom
            ]
            pygame.draw.polygon(surface, self.color, points)
        elif direction == "down":
            # Draw a triangle pointing down
            points = [
                (x, y + GRID_SIZE),             # Bottom left
                (x + GRID_SIZE, y + GRID_SIZE),  # Bottom right
                (x + GRID_SIZE // 2, y + GRID_SIZE // 2)  # Middle top
            ]
            pygame.draw.polygon(surface, self.color, points)

        # Draw outline for tail - slightly darker than the main color
        outline_color = (
            max(0, self.color[0] - 50),
            max(0, self.color[1] - 50),
            max(0, self.color[2] - 50)
        )
        pygame.draw.rect(surface, outline_color, rect, 1)

        # Draw some scales on the tail base
        scale_color = (
            min(255, self.color[0] + 30),
            min(255, self.color[1] + 30),
            min(255, self.color[2] + 30)
        )

        # Draw a single scale near the center
        scale_size = max(3, GRID_SIZE // 4)
        pygame.draw.ellipse(surface, scale_color,
                            (x + GRID_SIZE // 3, y + GRID_SIZE // 3,
                             scale_size, scale_size))

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

                # Draw outline for head - slightly darker than the main color
                outline_color = (max(0, self.color[0] - 50),
                                 max(0, self.color[1] - 50),
                                 max(0, self.color[2] - 50))
                pygame.draw.rect(surface, outline_color, rect, 1)

                # Draw the eyes
                self.draw_eyes(surface, position, self.direction)
            elif i == len(self.positions) - 1 and len(self.positions) > 1:  # This is the tail
                # Draw a tapered tail, pointing away from the previous segment
                prev_position = self.positions[i - 1]
                self.draw_tail(surface, position, prev_position)
            else:
                # Draw body segments with scales
                self.draw_scales(surface, position, i)
