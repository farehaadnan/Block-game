import pygame
import random

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 450
FPS = 60

# Color palette
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Block Game')
clock = pygame.time.Clock()

# Classes
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)  # Use SRCALPHA to enable transparency
        pygame.draw.circle(self.image, GREEN, (15, 15), 15)  # Draw a circle on the surface
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.x_speed = random.randint(-5, 5)
        self.y_speed = random.randint(3, 6)

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Bounce off walls
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.x_speed = -self.x_speed

        if self.rect.top <= 0:
            self.y_speed = -self.y_speed

        # Respawn the ball if it goes off the bottom of the screen
        if self.rect.y > SCREEN_HEIGHT + 10:
            global running
            running=False

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((130, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def update(self):
        self.move()

    def reset(self):
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT // 2
        self.speed_x = BALL_SPEED
        self.speed_y = -BALL_SPEED
class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 20))  # Adjusted size to fit the screen better
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Function to create a grid of bricks
def create_bricks():
    brick_colors = [RED, BLUE, YELLOW, CYAN, MAGENTA]
    bricks = pygame.sprite.Group()
    for row in range(5):  # Number of rows
        for col in range(10):  # Number of columns
            x = 5 + col * (50 + 5)  # 50 is the width of the brick, 5 is the space between bricks
            y = 5 + row * (20 + 5)  # 20 is the height of the brick, 5 is the space between bricks
            color = random.choice(brick_colors)
            brick = Brick(color, x, y)
            bricks.add(brick)
    return bricks

# Initialize the game
all_sprites = pygame.sprite.Group()
bricks = create_bricks()
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
paddle = Paddle()
all_sprites.add(ball)
all_sprites.add(paddle)
all_sprites.add(bricks)

# Game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Check for collision between ball and paddle
    if pygame.sprite.collide_rect(ball, paddle):
        ball.y_speed = -ball.y_speed
        ball.rect.y = paddle.rect.top - ball.rect.height

    # Check for collisions between ball and bricks
    brick_collisions = pygame.sprite.spritecollide(ball, bricks, True)
    if brick_collisions:
        ball.y_speed = -ball.y_speed

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
