import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Smooth Move with Box Collider")

# Define initial variables
player_color = (255, 0, 0)  # Red color
player_size = 50  # Size of the player square
player_x, player_y = width // 2, height // 2  # Start at the center
speed = 1000  # Speed in pixels per second

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Calculate delta time (time between frames)
    dt = clock.get_time() / 1000.0  # Convert milliseconds to seconds

    screen.fill((0, 0, 0))  # Fill the screen with black background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Change color to red
                player_color = (255, 0, 0)
            if event.key == pygame.K_g:  # Change color to green
                player_color = (0, 255, 0)
            if event.key == pygame.K_b:  # Change color to blue
                player_color = (0, 0, 255)
            if event.key == pygame.K_c:  # Change color to cyan
                player_color = (0, 255, 255)
            if event.key == pygame.K_y:  # Change color to yellow
                player_color = (255, 255, 0)

    # Movement with WASD and arrow keys (smooth)
    keys = pygame.key.get_pressed()

    # Calculate potential new position based on key input
    move_x = 0
    move_y = 0

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        move_x = -speed * dt  # Move left
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        move_x = speed * dt  # Move right
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        move_y = -speed * dt  # Move up
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        move_y = speed * dt  # Move down

    # Calculate new player position
    new_x = player_x + move_x
    new_y = player_y + move_y

    # Prevent the player from moving off-screen (keep the player inside the screen bounds)
    if new_x < 0:
        new_x = 0
    elif new_x + player_size > width:
        new_x = width - player_size

    if new_y < 0:
        new_y = 0
    elif new_y + player_size > height:
        new_y = height - player_size

    # Update the player position
    player_x = new_x
    player_y = new_y

    # Draw the player square using the updated position
    pygame.draw.rect(screen, player_color, pygame.Rect(player_x, player_y, player_size, player_size))

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(240)

# Quit pygame
pygame.quit()
sys.exit()