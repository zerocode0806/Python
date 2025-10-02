import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner with Shooting")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Clock for FPS
clock = pygame.time.Clock()

# Player settings
player_size = 50
player_x = 100
player_y = HEIGHT - player_size
player_velocity_y = 0
gravity = 1
jump_height = -15

# Obstacle settings
obstacle_width = 50
obstacle_height = 50
obstacle_velocity = 5
obstacle_list = []

# Bullet settings
bullet_width = 10
bullet_height = 5
bullet_velocity = 10
bullet_list = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Pause flag
paused = False

def create_obstacle():
    obstacle_x = WIDTH
    obstacle_y = HEIGHT - obstacle_height
    obstacle_hp = random.randint(1, 5)  # Assign random HP between 1 and 5
    return [obstacle_x, obstacle_y, obstacle_hp]

def move_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle[0] -= obstacle_velocity
    return [obs for obs in obstacles if obs[0] > -obstacle_width]  # Remove if off-screen

def move_bullets(bullets):
    for bullet in bullets:
        bullet[0] += bullet_velocity
    return [bul for bul in bullets if bul[0] < WIDTH]  # Remove if off-screen

def check_collision(player_rect, obstacles):
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if player_rect.colliderect(obstacle_rect):
            return True
    return False

def check_bullet_collision(bullets, obstacles):
    global score  # Declare score as global to modify it
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
            if bullet_rect.colliderect(obstacle_rect):
                obstacle[2] -= 1  # Decrease obstacle HP
                if obstacle[2] <= 0:
                    obstacles.remove(obstacle)  # Remove if HP <= 0
                    score += 5  # Increase score for shooting down an obstacle
                bullets.remove(bullet)  # Remove the bullet
                break

def draw_game(player_rect, obstacles, bullets, score):
    screen.fill(WHITE)
    
    # Draw player
    pygame.draw.rect(screen, BLUE, player_rect)
    
    # Draw obstacles with HP
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))
        hp_text = font.render(f"HP: {obstacle[2]}", True, BLACK)
        screen.blit(hp_text, (obstacle[0], obstacle[1] - 20))
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, GREEN, (bullet[0], bullet[1], bullet_width, bullet_height))
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

def pause_game():
    paused_font = pygame.font.Font(None, 48)
    paused_text = paused_font.render("Paused", True, BLACK)
    screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2 - paused_text.get_height() // 2))
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return  # Unpause the game

# Main game loop
def game_loop():
    global player_y, player_velocity_y, score, paused
    running = True
    obstacle_timer = 0
    bullet_list = []  # Initialize bullet list
    
    while running:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_y == HEIGHT - player_size:  # Jump if on the ground
                    player_velocity_y = jump_height
                if event.key == pygame.K_UP:  # Shoot by pressing up arrow
                    bullet_list.append([player_x + player_size, player_y + player_size // 2])
                if event.key == pygame.K_p:  # Pause or unpause the game
                    paused = not paused
                    if paused:
                        pause_game()  # Show pause screen
        
        if not paused:
            # Gravity effect and player movement
            player_velocity_y += gravity
            player_y += player_velocity_y
            
            # Prevent player from falling through the floor
            if player_y >= HEIGHT - player_size:
                player_y = HEIGHT - player_size
                player_velocity_y = 0
            
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            
            # Obstacle creation
            if obstacle_timer > 60:
                obstacle_list.append(create_obstacle())
                obstacle_timer = 0
            obstacle_timer += 1
            
            # Move bullets and obstacles
            bullet_list = move_bullets(bullet_list)
            obstacle_list[:] = move_obstacles(obstacle_list)
            
            # Check for collisions
            if check_collision(player_rect, obstacle_list):
                running = False  # End game if collision happens
            
            # Check bullet collisions with obstacles
            check_bullet_collision(bullet_list, obstacle_list)
            
            # Update score for passing obstacles
            for obstacle in obstacle_list:
                if obstacle[0] < 0 and obstacle not in obstacle_list:
                    score += 1  # Increase score for each obstacle that has been passed
            
        # Drawing
        draw_game(player_rect, obstacle_list, bullet_list, score)
    
    pygame.quit()

# Run the game
game_loop()
