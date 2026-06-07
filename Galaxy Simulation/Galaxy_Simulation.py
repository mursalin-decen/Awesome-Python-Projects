import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Simulation")

clock = pygame.time.Clock()

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

stars = []

# Create stars
for _ in range(1200):
    radius = random.uniform(20, 320)
    angle = random.uniform(0, 2 * math.pi)

    speed = 0.0005 + (320 - radius) * 0.00002

    size = random.randint(1, 3)

    stars.append({
        "radius": radius,
        "angle": angle,
        "speed": speed,
        "size": size
    })

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Trail effect
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.set_alpha(25)
    fade.fill((0, 0, 0))
    screen.blit(fade, (0, 0))

    # Galaxy center
    pygame.draw.circle(screen, (255, 255, 180), (CENTER_X, CENTER_Y), 8)

    for star in stars:
        star["angle"] += star["speed"]

        x = CENTER_X + math.cos(star["angle"]) * star["radius"]
        y = CENTER_Y + math.sin(star["angle"]) * star["radius"] * 0.5

        # Random star colors
        color = random.choice([
            (255, 255, 255),
            (180, 220, 255),
            (255, 220, 180)
        ])

        pygame.draw.circle(
            screen,
            color,
            (int(x), int(y)),
            star["size"]
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()