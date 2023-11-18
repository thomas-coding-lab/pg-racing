import pygame
import math
import time

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Racing Game")

# Load game assets
track_image = pygame.image.load('track_image.png')
track_image = pygame.transform.scale(track_image, (WIDTH, HEIGHT))
car_image = pygame.image.load('car_sprite.png')
car_image = pygame.transform.scale(car_image, (50, 100))  # Resize car sprite

# Car properties
car_x, car_y = 100, 100  # Starting position
car_speed = 0
car_angle = 0
MAX_SPEED = 5
ACCELERATION = 0.1
ROTATION_SPEED = 5

# Lap counting and timing
lap_count = 0
race_started = False
start_time = None
last_lap_time = None
on_start_line = False
MAX_LAPS = 5

# Helper functions
def is_within_bounds(x, y):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT

def is_on_start_line(x, y):
    return track_image.get_at((int(x), int(y))) == pygame.Color('red')

# Main game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Get key states
    keys = pygame.key.get_pressed()

    # Car movement logic
    if keys[pygame.K_DOWN]:
        car_speed = max(car_speed + ACCELERATION, -MAX_SPEED)
    elif keys[pygame.K_UP]:
        car_speed = min(car_speed - ACCELERATION, MAX_SPEED)
    else:
        car_speed *= 0.9  # Friction effect

    if keys[pygame.K_LEFT]:
        car_angle += ROTATION_SPEED
    if keys[pygame.K_RIGHT]:
        car_angle -= ROTATION_SPEED

    # Calculate potential new position
    new_x = car_x + car_speed * math.sin(math.radians(car_angle))
    new_y = car_y + car_speed * math.cos(math.radians(car_angle))

    # Update car position if within bounds
    if is_within_bounds(new_x, new_y):
        car_x, car_y = new_x, new_y

        # Check for start/finish line crossing
        if is_on_start_line(car_x, car_y):
            if not race_started:
                race_started = True
                start_time = time.time()
                last_lap_time = start_time
                print("Race started!")
            elif not on_start_line:
                lap_count += 1
                lap_time = time.time() - last_lap_time
                last_lap_time = time.time()
                print(f"Lap {lap_count} completed in {lap_time:.2f} seconds")
                if lap_count == MAX_LAPS:
                    print("Race finished!")
                    run = False
            on_start_line = True
        else:
            on_start_line = False

    # Collision detection
    if track_image.get_at((int(car_x), int(car_y))) == pygame.Color('black'):
        print("Out of track! Game over.")
        run = False  # Stop game if car hits the black area

    # Drawing
    win.blit(track_image, (0, 0))
    rotated_car = pygame.transform.rotate(car_image, car_angle)
    car_rect = rotated_car.get_rect(center=(car_x, car_y))
    win.blit(rotated_car, car_rect.topleft)

    pygame.display.update()
    pygame.time.Clock().tick(60)  # 60 FPS

pygame.quit()
