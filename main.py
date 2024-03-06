import pygame
import random
import time
import asyncio

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Game")

# Define colors
BLACK = (0, 0, 0)  # background is black

# Define player properties
player_width, player_height = 30, 30
player_x = 385
player_y = 550
player_speed = 5
player_color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
obstacle_color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Define obstacle properties
obstacle_width, obstacle_height = 50, 50
obstacle_speed = 5
obstacle_list = []

# Define button properties
button_width, button_height = 100, 50
button_x = SCREEN_WIDTH // 4 - button_width // 2
button_y = SCREEN_HEIGHT - button_height - 20
button_color = (100, 100, 255)

# Define font
font = pygame.font.Font(None, 36)

# Set up the game loop
clock = pygame.time.Clock()
running = True
score = 0
score_timer = 0
score_interval = 1000  # Score updates every second (1000 milliseconds)

def draw_player(x, y):
    pygame.draw.rect(screen, player_color, (x, y, player_width, player_height))

def draw_obstacles():
    for obstacle in obstacle_list:
        pygame.draw.rect(screen, obstacle_color, obstacle)

def generate_obstacle():
    x = random.randint(0, SCREEN_WIDTH - obstacle_width)
    y = 0 - obstacle_height
    obstacle_list.append(pygame.Rect(x, y, obstacle_width, obstacle_height))

def move_obstacles():
    for obstacle in obstacle_list:
        obstacle.y += obstacle_speed

def check_collision():
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for obstacle in obstacle_list:
        if player_rect.colliderect(obstacle):
            return True
    return False

# Main game loop
async def main():
    global running, player_x, player_y, score, score_timer, game_over, player_color, obstacle_color
    while running:
        screen.fill(BLACK)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Check for keydown events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x -= player_speed
                elif event.key == pygame.K_RIGHT:
                    player_x += player_speed
                elif event.key == pygame.K_SPACE and game_over:
                    # Restart the game
                    obstacle_list = []
                    player_x = SCREEN_WIDTH // 2 - player_width // 2
                    player_y = SCREEN_HEIGHT - player_height - 20
                    score = 0
                    score_timer = 0
                    player_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    obstacle_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        # Draw player
        draw_player(player_x, player_y)

        # Draw buttons
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        text_restart = font.render("RESTART", True, (255, 255, 255))
        screen.blit(text_restart, (button_x + 20, button_y + 10))

        # Generate obstacles
        if random.randint(1, 100) < 10:
            generate_obstacle()

        # Move and draw obstacles
        move_obstacles()
        draw_obstacles()

        # Check for collision
        if check_collision():
            # Draw game over message and restart button
            game_over = True
            text_game_over = font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(text_game_over, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            time.sleep(0.5)

        # Update display
        pygame.display.update()
        clock.tick(60)  # Control the game speed
        await asyncio.sleep(0)

asyncio.run(main())
