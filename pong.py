import pygame
import sys
import random
import numpy as np
from collections import deque

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong-style Table Tennis")

# Colors
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 40)
RED = (255, 50, 50)  # Brighter red
DIMI_AURA = (0, 255, 255)  # Cyan
ALICE_AURA = (255, 0, 255)  # Magenta

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90

# Ball dimensions
BALL_SIZE = 15

# Game objects
dimi_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
alice_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Ball physics
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
ball_spin = 0
MAX_BALL_SPEED = 15
SPIN_DECAY = 0.98
SPIN_EFFECT = 0.2

# Paddle speed and movement
paddle_speed = 12
dimi_paddle_movement = 0
alice_paddle_movement = 0

# Scores
dimi_score = 0
alice_score = 0
WINNING_SCORE = 5  # Changed from 10 to 5

# Font
font = pygame.font.Font(None, 36)

# Game state
game_active = False
game_over = False

# Generate sounds
def generate_beep(frequency, duration):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    beep = np.sin(2 * np.pi * frequency * t)
    beep = np.repeat(beep.reshape(beep.shape[0], 1), 2, axis=1)
    beep = (beep * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(beep)

hit_sound = generate_beep(440, 0.1)  # 440 Hz, 100 ms
lose_sound = generate_beep(220, 0.3)  # 220 Hz, 300 ms

# Ball trail
trail_length = 15
ball_trail = deque(maxlen=trail_length)

# Colorful trail
def get_rainbow_color(i, max_i):
    r = int(255 * (1 - i / max_i))
    g = int(255 * (0.5 - abs(0.5 - i / max_i)))
    b = int(255 * (i / max_i))
    return (r, g, b)

# Animated background
star_field = []
for _ in range(100):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speed = random.uniform(0.1, 0.5)
    star_field.append([x, y, speed])

# Paddle effects
shake_time = 0
shake_duration = 60  # 1 second at 60 FPS
paddle_trail = deque(maxlen=5)
losing_paddle = None

# Fireworks
fireworks = []

def reset_ball():
    global ball_speed_x, ball_speed_y, ball_spin
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x = 7 * random.choice((1, -1))
    ball_speed_y = 7 * random.choice((1, -1))
    ball_spin = 0
    ball_trail.clear()

def show_score():
    dimi_text = font.render(f"Dimi: {dimi_score}", True, WHITE)
    alice_text = font.render(f"Alice: {alice_score}", True, WHITE)
    screen.blit(dimi_text, (WIDTH//4, 20))
    screen.blit(alice_text, (3*WIDTH//4 - alice_text.get_width(), 20))

def show_winner(winner):
    winner_text = font.render(f"{winner} is the sexy winner!", True, WHITE)
    screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2))
    create_fireworks(20)  # Create 20 fireworks

def show_start_message():
    start_text = font.render("Press SPACE to start", True, WHITE)
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))

def update_star_field():
    for star in star_field:
        star[0] -= star[2]
        if star[0] < 0:
            star[0] = WIDTH
            star[1] = random.randint(0, HEIGHT)

def draw_star_field():
    for star in star_field:
        pygame.draw.circle(screen, WHITE, (int(star[0]), int(star[1])), 1)

def draw_paddle_with_effects(paddle, color, aura_color):
    global shake_time, losing_paddle
    
    # Draw aura
    for i in range(5):
        aura_rect = paddle.inflate(i*4, i*4)
        alpha = 100 - i * 20
        aura_surf = pygame.Surface(aura_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(aura_surf, (*aura_color, alpha), aura_surf.get_rect())
        screen.blit(aura_surf, aura_rect)
    
    # Draw paddle
    if losing_paddle == paddle and shake_time > 0:
        shake_offset = random.randint(-4, 4)  # Increased shake range
        shake_rect = paddle.inflate(8, 8).move(shake_offset, 0)  # Bigger paddle during shake
        pygame.draw.rect(screen, RED, shake_rect)
        shake_time -= 1
        if shake_time == 0:
            losing_paddle = None
    else:
        pygame.draw.rect(screen, color, paddle)
    
    # Draw trail effect (smaller and more transparent)
    for i, pos in enumerate(paddle_trail):
        alpha = 100 - i * 20  # More transparent
        trail_rect = pygame.Rect(pos[0], pos[1], PADDLE_WIDTH, PADDLE_HEIGHT // 2)  # Smaller height
        trail_surf = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT // 2), pygame.SRCALPHA)
        pygame.draw.rect(trail_surf, (*color, alpha), trail_surf.get_rect())
        screen.blit(trail_surf, trail_rect)

def apply_ball_physics():
    global ball_speed_x, ball_speed_y, ball_spin

    # Apply spin effect
    ball_speed_y += ball_spin * SPIN_EFFECT

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Decay spin
    ball_spin *= SPIN_DECAY

    # Cap ball speed
    speed = (ball_speed_x**2 + ball_speed_y**2)**0.5
    if speed > MAX_BALL_SPEED:
        factor = MAX_BALL_SPEED / speed
        ball_speed_x *= factor
        ball_speed_y *= factor

def create_fireworks(num_fireworks):
    for _ in range(num_fireworks):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT // 2)
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        fireworks.append({'pos': [x, y], 'vel': [random.uniform(-2, 2), random.uniform(-2, 2)], 'color': color, 'lifetime': 100})

def update_fireworks():
    for fw in fireworks:
        fw['pos'][0] += fw['vel'][0]
        fw['pos'][1] += fw['vel'][1]
        fw['lifetime'] -= 1

    fireworks[:] = [fw for fw in fireworks if fw['lifetime'] > 0]

def draw_fireworks():
    for fw in fireworks:
        pygame.draw.circle(screen, fw['color'], (int(fw['pos'][0]), int(fw['pos'][1])), 3)

def draw_dashed_line():
    dash_length = 10
    gap_length = 5
    y = 0
    while y < HEIGHT:
        start_pos = (WIDTH // 2, y)
        end_pos = (WIDTH // 2, min(y + dash_length, HEIGHT))
        pygame.draw.line(screen, WHITE, start_pos, end_pos, 2)
        y += dash_length + gap_length

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_over:
                dimi_score = alice_score = 0
                game_over = False
            game_active = True

    if game_active and not game_over:
        # Move paddles
        keys = pygame.key.get_pressed()
        dimi_paddle_movement = 0
        alice_paddle_movement = 0
        
        if keys[pygame.K_w] and dimi_paddle.top > 0:
            dimi_paddle.y -= paddle_speed
            dimi_paddle_movement = -paddle_speed
            paddle_trail.appendleft(dimi_paddle.topleft)
        if keys[pygame.K_s] and dimi_paddle.bottom < HEIGHT:
            dimi_paddle.y += paddle_speed
            dimi_paddle_movement = paddle_speed
            paddle_trail.appendleft(dimi_paddle.topleft)
        if keys[pygame.K_UP] and alice_paddle.top > 0:
            alice_paddle.y -= paddle_speed
            alice_paddle_movement = -paddle_speed
            paddle_trail.appendleft(alice_paddle.topleft)
        if keys[pygame.K_DOWN] and alice_paddle.bottom < HEIGHT:
            alice_paddle.y += paddle_speed
            alice_paddle_movement = paddle_speed
            paddle_trail.appendleft(alice_paddle.topleft)

        # Apply ball physics
        apply_ball_physics()

        # Update ball trail
        ball_trail.appendleft(ball.center)

        # Ball collision with top and bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
            hit_sound.play()  # Play sound on wall hit

        # Ball collision with paddles
        if ball.colliderect(dimi_paddle):
            ball_speed_x = abs(ball_speed_x)  # Ensure the ball moves right
            ball_speed_x += 1  # Accelerate the ball
            ball_spin = dimi_paddle_movement * 0.2  # Apply spin based on paddle movement
            hit_sound.play()
        elif ball.colliderect(alice_paddle):
            ball_speed_x = -abs(ball_speed_x)  # Ensure the ball moves left
            ball_speed_x -= 1  # Accelerate the ball
            ball_spin = alice_paddle_movement * 0.2  # Apply spin based on paddle movement
            hit_sound.play()

        # Scoring
        if ball.left <= 0:
            alice_score += 1
            losing_paddle = dimi_paddle
            shake_time = shake_duration
            lose_sound.play()  # Play lose sound
            reset_ball()
        if ball.right >= WIDTH:
            dimi_score += 1
            losing_paddle = alice_paddle
            shake_time = shake_duration
            lose_sound.play()  # Play lose sound
            reset_ball()

        # Check for winner
        if dimi_score == WINNING_SCORE:
            show_winner("Dimi")
            game_over = True
            game_active = False
        elif alice_score == WINNING_SCORE:
            show_winner("Alice")
            game_over = True
            game_active = False

    # Update star field and fireworks
    update_star_field()
    update_fireworks()

    # Drawing
    screen.fill(DARK_BLUE)
    draw_star_field()
    draw_dashed_line()
    
    draw_paddle_with_effects(dimi_paddle, WHITE, DIMI_AURA)
    draw_paddle_with_effects(alice_paddle, WHITE, ALICE_AURA)
    
    # Draw ball trail (smaller, thinner, and colorful)
    for i, pos in enumerate(ball_trail):
        alpha = 200 - int(200 * (i / trail_length))
        trail_color = (*get_rainbow_color(i, trail_length), alpha)
        trail_size = max(1, BALL_SIZE // 2 - int(BALL_SIZE // 2 * (i / trail_length)))
        pygame.draw.circle(screen, trail_color, pos, trail_size)
    
    pygame.draw.ellipse(screen, WHITE, ball)
    
    show_score()
    
    if game_over:
        draw_fireworks()
        show_start_message()
    elif not game_active:
        show_start_message()

    # Update display
    pygame.display.flip()

    # Control game speed
    pygame.time.Clock().tick(60)
