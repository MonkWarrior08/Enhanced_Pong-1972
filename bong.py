import pygame
import sys
import random
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong-style Table Tennis")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90

# Ball dimensions
BALL_SIZE = 15

# Game objects
dimi_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
alice_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Ball speed
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))

# Paddle speed
paddle_speed = 12

# Scores
dimi_score = 0
alice_score = 0

# Font
font = pygame.font.Font(None, 36)

# Game state
game_active = False

# Generate a simple beep sound
sample_rate = 44100
duration = 0.1  # 100 ms
t = np.linspace(0, duration, int(sample_rate * duration), False)
beep = np.sin(2 * np.pi * 440 * t)
beep = np.repeat(beep.reshape(beep.shape[0], 1), 2, axis=1)
beep = (beep * 32767).astype(np.int16)
hit_sound = pygame.sndarray.make_sound(beep)

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x = 7 * random.choice((1, -1))
    ball_speed_y = 7 * random.choice((1, -1))

def show_score():
    dimi_text = font.render(f"Dimi: {dimi_score}", True, WHITE)
    alice_text = font.render(f"Alice: {alice_score}", True, WHITE)
    screen.blit(dimi_text, (WIDTH//4, 20))
    screen.blit(alice_text, (3*WIDTH//4 - alice_text.get_width(), 20))

def show_winner(winner):
    winner_text = font.render(f"{winner} is the sexy winner!", True, WHITE)
    screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before resetting

def show_start_message():
    start_text = font.render("Press SPACE to start", True, WHITE)
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True

    if game_active:
        # Move paddles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and dimi_paddle.top > 0:
            dimi_paddle.y -= paddle_speed
        if keys[pygame.K_s] and dimi_paddle.bottom < HEIGHT:
            dimi_paddle.y += paddle_speed
        if keys[pygame.K_UP] and alice_paddle.top > 0:
            alice_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and alice_paddle.bottom < HEIGHT:
            alice_paddle.y += paddle_speed

        # Move ball
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with top and bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
            hit_sound.play()  # Play sound on wall hit

        # Ball collision with paddles
        if ball.colliderect(dimi_paddle) or ball.colliderect(alice_paddle):
            ball_speed_x *= -1
            hit_sound.play()  # Play sound on paddle hit

        # Scoring
        if ball.left <= 0:
            alice_score += 1
            game_active = False
            reset_ball()
        if ball.right >= WIDTH:
            dimi_score += 1
            game_active = False
            reset_ball()

        # Check for winner
        if dimi_score == 10:
            show_winner("Dimi")
            dimi_score = alice_score = 0
        elif alice_score == 10:
            show_winner("Alice")
            dimi_score = alice_score = 0

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, dimi_paddle)
    pygame.draw.rect(screen, WHITE, alice_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    show_score()
    
    if not game_active:
        show_start_message()

    # Update display
    pygame.display.flip()

    # Control game speed
    pygame.time.Clock().tick(60)
