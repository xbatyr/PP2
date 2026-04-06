import pygame
import datetime
import math
import os
import sys

pygame.init()

W, H = 600, 400
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mickey Clock")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (239, 228, 176)

font = pygame.font.SysFont("Arial", 28, bold=True)
clock = pygame.time.Clock()

base = os.path.dirname(__file__)
img_path = os.path.join(base, "images")
face = pygame.image.load(os.path.join(img_path, "clock_face.png")).convert_alpha()
face = pygame.transform.scale(face, (W, H))

cx, cy = W // 2, H // 2


def get_end(angle_deg, length):
    angle_rad = math.radians(angle_deg - 90)
    x = cx + length * math.cos(angle_rad)
    y = cy + length * math.sin(angle_rad)
    return x, y


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    now = datetime.datetime.now()

    h = now.hour % 12
    m = now.minute
    s = now.second

    # углы
    hour_angle = h * 30 + m * 0.5
    minute_angle = m * 6 + s * 0.1
    second_angle = s * 6

    screen.fill(WHITE)
    screen.blit(face, (0, 0))

    # часовая
    hx, hy = get_end(hour_angle, 70)
    pygame.draw.line(screen, BLACK, (cx, cy), (hx, hy), 6)

    # минутная
    mx, my = get_end(minute_angle, 100)
    pygame.draw.line(screen, (30, 30, 30), (cx, cy), (mx, my), 4)

    # секундная
    sx, sy = get_end(second_angle, 120)
    pygame.draw.line(screen, RED, (cx, cy), (sx, sy), 2)

    # центр
    pygame.draw.circle(screen, BLACK, (cx, cy), 6)

    text = font.render(now.strftime("%H:%M:%S"), True, RED, YELLOW)
    screen.blit(text, (430, 350))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()