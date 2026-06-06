import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Particle Heart 💖")

clock = pygame.time.Clock()

NUM_PARTICLES = 5200

# Heart equation
def heart_function(t):
    x = 16 * (math.sin(t) ** 3)
    y = -(13 * math.cos(t)
          - 5 * math.cos(2 * t)
          - 2 * math.cos(3 * t)
          - math.cos(4 * t))
    return x, y

# Particle class
class Particle:
    def __init__(self):
        self.t = random.uniform(0, math.pi * 2)
        self.target_x, self.target_y = heart_function(self.t)

        self.target_x *= 20
        self.target_y *= 20

        self.target_x += WIDTH // 2
        self.target_y += HEIGHT // 2

        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)

        self.speed = random.uniform(0.02, 0.05)

    def update(self, pulse):
        dx = self.target_x - self.x
        dy = self.target_y - self.y

        self.x += dx * self.speed
        self.y += dy * self.speed

        # heartbeat movement
        self.draw_x = WIDTH // 2 + (self.x - WIDTH // 2) * pulse
        self.draw_y = HEIGHT // 2 + (self.y - HEIGHT // 2) * pulse

    def draw(self, surface):
        # glow effect (outer soft)
        pygame.draw.circle(surface, (255, 50, 100), (int(self.draw_x), int(self.draw_y)), 3)
        pygame.draw.circle(surface, (255, 0, 80), (int(self.draw_x), int(self.draw_y)), 2)
        pygame.draw.circle(surface, (255, 150, 200), (int(self.draw_x), int(self.draw_y)), 1)

particles = [Particle() for _ in range(NUM_PARTICLES)]

time = 0
running = True

while running:
    screen.fill((5, 0, 10))  # dark neon background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # heartbeat pulse (realistic double-beat feel)
    pulse = 1 + 0.06 * math.sin(time) + 0.02 * math.sin(time * 2)

    # draw particles
    for p in particles:
        p.update(pulse)
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)
    time += 0.05

pygame.quit()