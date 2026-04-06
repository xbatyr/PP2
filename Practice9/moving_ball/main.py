import pygame
import sys

pygame.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Moving Ball Game")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

x = 100
y = 100
r = 25
step = 20

clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if y - step - r >= 0:
                    y -= step

            elif event.key == pygame.K_DOWN:
                if y + step + r <= H:
                    y += step

            elif event.key == pygame.K_LEFT:
                if x - step - r >= 0:
                    x -= step

            elif event.key == pygame.K_RIGHT:
                if x + step + r <= W:
                    x += step

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x, y), r)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()