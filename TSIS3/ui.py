import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT = (235, 235, 235)
BLUE = (90, 150, 255)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font, active=False):
        mouse = pygame.mouse.get_pos()
        color = BLUE if active else LIGHT
        if self.rect.collidepoint(mouse):
            color = (min(color[0] + 12, 255), min(color[1] + 12, 255), min(color[2] + 12, 255))
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)
        text = font.render(self.text, True, BLACK)
        screen.blit(text, text.get_rect(center=self.rect.center))


def draw_text(screen, text, font, color, x, y, center=False):
    image = font.render(str(text), True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)


def draw_box(screen, rect, fill=(245, 245, 245)):
    pygame.draw.rect(screen, fill, rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)
