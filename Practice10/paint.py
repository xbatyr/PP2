import pygame
pygame.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()


game_over = False
prev, cur = None, None
screen.fill(WHITE)
current_color = RED
mode = 'draw'  # 'draw', 'rect', 'circle', 'erase'

font = pygame.font.SysFont(None, 24)

def draw_toolbar():
    pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, 40))
    colors = [RED, GREEN, BLUE, BLACK]
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (10 + i * 50, 5, 40, 30))
    pygame.draw.rect(screen, WHITE, (210, 5, 40, 30))  # Eraser
    pygame.draw.rect(screen, WHITE, (260, 5, 40, 30))  # Rect
    pygame.draw.rect(screen, WHITE, (310, 5, 40, 30))  # Circle
    screen.blit(font.render("E", True, BLACK), (220, 10))
    screen.blit(font.render("R", True, BLACK), (270, 10))
    screen.blit(font.render("C", True, BLACK), (320, 10))

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y < 40:
                if 10 <= x < 50:
                    current_color, mode = RED, 'draw'
                elif 60 <= x < 100:
                    current_color, mode = GREEN, 'draw'
                elif 110 <= x < 150:
                    current_color, mode = BLUE, 'draw'
                elif 160 <= x < 200:
                    current_color, mode = BLACK, 'draw'
                elif 210 <= x < 250:
                    current_color, mode = WHITE, 'erase'
                elif 260 <= x < 300:
                    mode = 'rect'
                elif 310 <= x < 350:
                    mode = 'circle'
            else:
                prev = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if mode == 'rect' and prev:
                cur = event.pos
                x1, y1 = prev
                x2, y2 = cur
                pygame.draw.rect(screen, current_color, pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1)), 1)
            elif mode == 'circle' and prev:
                cur = event.pos
                x1, y1 = prev
                x2, y2 = cur
                radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                pygame.draw.circle(screen, current_color, (x1, y1), radius, 1)
            prev = None

        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0] and prev and mode in ['draw', 'erase']:
                cur = pygame.mouse.get_pos()
                pygame.draw.line(screen, current_color, prev, cur, 3)
                prev = cur

    draw_toolbar()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()