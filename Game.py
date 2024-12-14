import pygame
import sys
from PIL import Image

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SCALE_FACTOR = 4  # Scale up the level display
PIXEL_SPEED = 32  # Movement speed in pixels per second
TILE_SIZE = 32  # Size of a logical tile

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Emoji Platformer")
clock = pygame.time.Clock()

# Load a PNG level
def load_level(png_file):
    img = Image.open(png_file)
    img = img.convert("RGB")
    width, height = img.size
    return img, width, height

# Draw the level
def draw_level(image, offset_x, offset_y):
    width, height = image.size
    for y in range(height):
        for x in range(width):
            color = image.getpixel((x, y))
            if color != BLACK:  # Draw non-black pixels
                rect = pygame.Rect(
                    (x * SCALE_FACTOR) - offset_x, (y * SCALE_FACTOR) - offset_y, SCALE_FACTOR, SCALE_FACTOR
                )
                pygame.draw.rect(screen, color, rect)

# Player class
class Player:
    def __init__(self, x, y, emoji):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.emoji = emoji
        self.velocity_y = 0
        self.is_on_ground = False

    def move(self, keys, level_image, dt):
        move_x = 0

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            move_x = -PIXEL_SPEED * dt
        if keys[pygame.K_RIGHT]:
            move_x = PIXEL_SPEED * dt

        self.x += move_x

        # Jumping
        if keys[pygame.K_SPACE] and self.is_on_ground:
            self.velocity_y = -15

        # Gravity
        self.velocity_y += 1
        self.y += self.velocity_y

        # Collision detection
        self.is_on_ground = False

        for tile_y in range(self.y // TILE_SIZE, (self.y + self.height) // TILE_SIZE + 1):
            for tile_x in range(self.x // TILE_SIZE, (self.x + self.width) // TILE_SIZE + 1):
                if 0 <= tile_x < level_image.size[0] and 0 <= tile_y < level_image.size[1]:
                    color = level_image.getpixel((tile_x, tile_y))
                    if color != BLACK:  # Collision with a platform
                        if self.velocity_y > 0:  # Landing on top
                            self.y = tile_y * TILE_SIZE - self.height
                            self.velocity_y = 0
                            self.is_on_ground = True

        # Prevent falling if not completely in black space
        for check_y in range(self.y, self.y + self.height, TILE_SIZE):
            for check_x in range(self.x, self.x + self.width, TILE_SIZE):
                tile_x = check_x // TILE_SIZE
                tile_y = check_y // TILE_SIZE
                if 0 <= tile_x < level_image.size[0] and 0 <= tile_y < level_image.size[1]:
                    if level_image.getpixel((tile_x, tile_y)) != BLACK:
                        return

        # Allow falling into black space
        if self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
            self.velocity_y = 0

    def draw(self):
        font = pygame.font.Font(None, self.width)
        text = font.render(self.emoji, True, WHITE)
        screen.blit(text, (self.x, self.y))

# Main game loop
level_file = "level.png"  # Replace with your level PNG file path
level_image, level_width, level_height = load_level(level_file)

# Pick an emoji character
player_emoji = input("Choose your emoji character: ")
player = Player(100, 100, player_emoji)

# Camera offset
offset_x, offset_y = 0, 0

while True:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Delta time for consistent speed
    dt = clock.get_time() / 1000.0

    # Move and draw player
    player.move(keys, level_image, dt)
    player.draw()

    # Update camera offset
    offset_x = player.x - SCREEN_WIDTH // 2
    offset_y = player.y - SCREEN_HEIGHT // 2

    # Draw the level
    draw_level(level_image, offset_x, offset_y)

    pygame.display.flip()
    clock.tick(FPS)
