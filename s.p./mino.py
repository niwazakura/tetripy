import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
COLOR_MAP = [CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE]

# Tetromino shapes (each represented as a list of coordinates relative to the center)
SHAPES = [
    [[(0, 0), (1, 0), (0, 1), (1, 1)]],  # O
    [[(0, 0), (-1, 0), (1, 0), (2, 0)]],  # I
    [[(0, 0), (-1, 0), (1, 0), (1, -1)]], # T
    [[(0, 0), (0, -1), (1, 0), (1, 1)]],  # L
    [[(0, 0), (0, 1), (1, 0), (1, -1)]],  # J
    [[(0, 0), (1, 0), (1, -1), (2, -1)]], # S
    [[(0, 0), (0, -1), (-1, 0), (-1, 1)]],# Z
]

# Game grid dimensions
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Define the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Techmino")

# Create the game grid (empty initially)
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Tetromino class to represent falling pieces
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - 1  # Start in the middle of the grid
        self.y = 0  # Start at the top of the grid

    def rotate(self):
        # Rotate the shape 90 degrees clockwise
        self.shape = [[(y, -x) for x, y in shape] for shape in self.shape]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_blocks(self):
        return [(self.x + x, self.y + y) for x, y in self.shape[0]]

# Check if the current position is valid
def valid_position(tetromino):
    for x, y in tetromino.get_blocks():
        if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or grid[y][x]:
            return False
    return True

# Place tetromino in the grid
def place_tetromino(tetromino):
    for x, y in tetromino.get_blocks():
        grid[y][x] = tetromino.color

# Remove full lines
def remove_lines():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    new_grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT - len(new_grid))] + new_grid
    grid = new_grid

# Draw the game grid
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Draw the falling tetromino
def draw_tetromino(tetromino):
    for x, y in tetromino.get_blocks():
        pygame.draw.rect(screen, tetromino.color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    current_tetromino = Tetromino(random.choice(SHAPES), random.choice(COLOR_MAP))
    running = True
    while running:
        screen.fill((0, 0, 0))  # Fill the screen with black
        draw_grid()
        draw_tetromino(current_tetromino)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move(-1, 0)
                    if not valid_position(current_tetromino):
                        current_tetromino.move(1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.move(1, 0)
                    if not valid_position(current_tetromino):
                        current_tetromino.move(-1, 0)
                elif event.key == pygame.K_DOWN:
                    current_tetromino.move(0, 1)
                    if not valid_position(current_tetromino):
                        current_tetromino.move(0, -1)
                        place_tetromino(current_tetromino)
                        remove_lines()
                        current_tetromino = Tetromino(random.choice(SHAPES), random.choice(COLOR_MAP))
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if not valid_position(current_tetromino):
                        # Rotate back if the position is invalid
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                        current_tetromino.rotate()

        pygame.display.update()
        clock.tick(10)  # Adjust the game speed

# Run the game
if __name__ == "__main__":
    game_loop()
    pygame.quit()
