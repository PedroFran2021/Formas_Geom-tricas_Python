import pygame
import random

BLACK = (0, 0, 0)
WHITTE = (255, 255, 255)

pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Particle System")

class Particle:
    def __init__(self, pos):
        self.pos = pos
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.radius = random.randint(10, 20)
        self.velocity = [random.randint(-5, -5), random.randint(-5, -5)]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        if self.pos[0] < 0 or self.pos[0] > size[0]:
            self.velocity[0] = -self.velocity[0]
        if self.pos[1] < 0 or self.pos[1] > size[1]:
            self.velocity[1] = -self.velocity[1]

particles = []

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            particles.append(Particle(list(event.pos)))

    for particle in particles:
        particle.update()

    screen.fill(BLACK)

    for particle in particles:
        particle.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()