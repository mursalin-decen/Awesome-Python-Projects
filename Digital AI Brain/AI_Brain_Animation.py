import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Digital AI Brain")

clock = pygame.time.Clock()

# Colors
BG = (5, 5, 15)
BLUE = (0, 220, 255)
WHITE = (220, 240, 255)

# Create nodes
nodes = []

for _ in range(120):
    angle = random.uniform(0, math.pi * 2)

    r = random.uniform(40, 250)

    x = WIDTH//2 + math.cos(angle) * r * 1.4
    y = HEIGHT//2 + math.sin(angle) * r

    nodes.append([x, y])

time = 0

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG)

    # Draw connections
    for i in range(len(nodes)):
        x1, y1 = nodes[i]

        for j in range(i + 1, len(nodes)):
            x2, y2 = nodes[j]

            dist = math.hypot(x2 - x1, y2 - y1)

            if dist < 90:
                alpha = max(20, 120 - int(dist))

                line_surface = pygame.Surface(
                    (WIDTH, HEIGHT),
                    pygame.SRCALPHA
                )

                pygame.draw.line(
                    line_surface,
                    (0, 200, 255, alpha),
                    (x1, y1),
                    (x2, y2),
                    1
                )

                screen.blit(line_surface, (0, 0))

    # Draw nodes
    for index, node in enumerate(nodes):

        x, y = node

        pulse = 2 + abs(
            math.sin(time + index * 0.2)
        ) * 4

        pygame.draw.circle(
            screen,
            (0, 120, 255),
            (int(x), int(y)),
            int(pulse + 4)
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(x), int(y)),
            int(pulse)
        )

    # Brain center glow
    glow = 25 + abs(math.sin(time * 2)) * 15

    pygame.draw.circle(
        screen,
        BLUE,
        (WIDTH//2, HEIGHT//2),
        int(glow)
    )

    pygame.display.flip()

    time += 0.03

    clock.tick(60)

pygame.quit()