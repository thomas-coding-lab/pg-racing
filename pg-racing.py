import pygame
import math
import time
import random

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

ai_car_image_1 = pygame.image.load('car_sprite2.png')
ai_car_image_1 = pygame.transform.scale(ai_car_image_1, (50, 100))  # Resize AI car sprite

ai_car_image_2 = pygame.image.load('car_sprite3.png')
ai_car_image_2 = pygame.transform.scale(ai_car_image_2, (50, 100))  # Resize AI car sprite



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

class AICar:
    def __init__(self, x, y, waypoints, image):
        self.x = x
        self.y = y
        self.speed = 2
        self.angle = 0
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.image = image
        self.speedrange = [random.randint(4,7), random.randint(8,11)]

    def update(self):
        global run
        if self.current_waypoint >= len(self.waypoints):
            print("Game over: AI win")
            run = False
            return  # AI car completed the track

        waypoint_x, waypoint_y = self.waypoints[self.current_waypoint]
        angle_to_waypoint = math.atan2(waypoint_y - self.y, waypoint_x - self.x)+90
        self.angle = math.degrees(angle_to_waypoint)

        # Dynamic speed adjustment
        distance_to_waypoint = distance(self.x, self.y, waypoint_x, waypoint_y)
        self.speed = random.randint(self.speedrange[0], self.speedrange[1])

        # Move towards the waypoint with bounds checking
        new_x = self.x + ((waypoint_x - self.x)*self.speed) / math.sqrt((waypoint_x-self.x)**2 + (waypoint_y-self.y)**2)
        new_y = self.y + ((waypoint_y - self.y)*self.speed) / math.sqrt((waypoint_x-self.x)**2 + (waypoint_y-self.y)**2)

        if is_within_bounds(new_x, new_y):
            self.x = new_x
            self.y = new_y

            # Check if the waypoint is reached
            if distance_to_waypoint < 10:  # Adjust threshold as needed
                self.current_waypoint += 1

# Define waypoints for AI Cars (example waypoints)
ai_waypoints = [
    (353,122),
    (545,122),
    (689,137),
    (718,297),
    (669,488),
    (502,485),
    (193,450),
    (75,349),
    (74,220),
    (148,110),
    (276,142),
    (400,122)    
    ]*5  # Define a series of waypoints


# Initialize AI cars
ai_cars = [AICar(100, 150, ai_waypoints, ai_car_image_1), AICar(120, 150, ai_waypoints, ai_car_image_2)] 

# Helper functions
def is_within_bounds(x, y):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT

def is_on_start_line(x, y):
    return track_image.get_at((int(x), int(y))) == pygame.Color('red')

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

collision_count = 0

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

    if keys[pygame.K_SPACE]:
        print(car_x, car_y)
    
    # Calculate potential new position
    new_x = car_x + car_speed * math.sin(math.radians(car_angle))
    new_y = car_y + car_speed * math.cos(math.radians(car_angle))
    
    # Check for edge collision
    if not is_within_bounds(new_x, new_y):
        collision_count += 1
        print(f"Collision with edge detected! Collision count: {collision_count}")

        if collision_count >= 3:
            print("Game Over: Too many collisions with the edges.")
            run = False
        else:
            # Optionally, reset car position after collision
            car_x, car_y = 456, 100  # Reset to starting position
            car_speed = 0

    else:
        # Update car position if within bounds
        car_x, car_y = new_x, new_y

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
                    print(f"Your record: {lap_time:.2f} seconds")
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


    # Update AI cars
    for ai_car in ai_cars:
        ai_car.update()

    # Drawing
    win.blit(track_image, (0, 0))
    rotated_car = pygame.transform.rotate(car_image, car_angle)
    car_rect = rotated_car.get_rect(center=(car_x, car_y))
    win.blit(rotated_car, car_rect.topleft)



    # Draw AI cars
    for ai_car in ai_cars:
        rotated_ai_car = pygame.transform.rotate(ai_car.image, ai_car.angle)
        ai_car_rect = rotated_ai_car.get_rect(center=(ai_car.x, ai_car.y))
        win.blit(rotated_ai_car, ai_car_rect.topleft)

    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()
