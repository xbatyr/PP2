import math
import pygame


pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
TOOLBAR_HEIGHT = 80

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

MODE_BRUSH = "brush"
MODE_LINE = "line"
MODE_RECT = "rect"
MODE_SQUARE = "square"
MODE_CIRCLE = "circle"
MODE_RIGHT_TRIANGLE = "r_tri"
MODE_EQUILATERAL = "e_tri"
MODE_RHOMBUS = "rhombus"
MODE_ERASER = "eraser"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint Program")
clock = pygame.time.Clock()


class Button:
    def __init__(self, x, y, w, h, color, text="", text_color=BLACK):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 18)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        if self.text:
            image = self.font.render(self.text, True, self.text_color)
            surface.blit(image, image.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class ColorPalette:
    def __init__(self, x, y):
        self.colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, PURPLE, GRAY]
        self.selected_color = BLACK
        self.color_rects = []

        for i, color in enumerate(self.colors):
            rect = pygame.Rect(x + i * 35, y, 30, 30)
            self.color_rects.append((rect, color))

    def draw(self, surface):
        for rect, color in self.color_rects:
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
            if color == self.selected_color:
                pygame.draw.rect(surface, WHITE, rect, 3)

    def check_click(self, pos):
        for rect, color in self.color_rects:
            if rect.collidepoint(pos):
                self.selected_color = color
                return True
        return False


def draw_square(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    size = max(abs(x2 - x1), abs(y2 - y1))
    if x2 < x1:
        x1 -= size
    if y2 < y1:
        y1 -= size
    pygame.draw.rect(surface, color, (x1, y1, size, size), width)


def draw_right_triangle(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    pygame.draw.polygon(surface, color, [(x1, y1), (x1, y2), (x2, y2)], width)


def draw_equilateral_triangle(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    size = abs(x2 - x1)
    height = size * math.sqrt(3) / 2
    if y2 < y1:
        height = -height
    points = [(x1, y2), (x2, y2), ((x1 + x2) // 2, y2 - height)]
    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    pygame.draw.polygon(surface, color, [(cx, y1), (x2, cy), (cx, y2), (x1, cy)], width)


def draw_shape(surface, mode, color, start, end, width):
    if mode == MODE_LINE:
        pygame.draw.line(surface, color, start, end, width)
    elif mode == MODE_RECT:
        rect = pygame.Rect(start[0], start[1], end[0] - start[0], end[1] - start[1])
        pygame.draw.rect(surface, color, rect, width)
    elif mode == MODE_SQUARE:
        draw_square(surface, color, start, end, width)
    elif mode == MODE_CIRCLE:
        radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
        pygame.draw.circle(surface, color, start, radius, width)
    elif mode == MODE_RIGHT_TRIANGLE:
        draw_right_triangle(surface, color, start, end, width)
    elif mode == MODE_EQUILATERAL:
        draw_equilateral_triangle(surface, color, start, end, width)
    elif mode == MODE_RHOMBUS:
        draw_rhombus(surface, color, start, end, width)


def main():
    canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    current_mode = MODE_BRUSH
    current_color = BLACK
    brush_size = 5
    line_width = 3
    eraser_size = 20

    drawing = False
    start_pos = None
    current_pos = None

    buttons = [
        Button(10, 5, 60, 25, GRAY, "Brush"),
        Button(75, 5, 60, 25, GRAY, "Line"),
        Button(140, 5, 60, 25, GRAY, "Rect"),
        Button(205, 5, 60, 25, GRAY, "Square"),
        Button(270, 5, 60, 25, GRAY, "Circle"),
        Button(335, 5, 70, 25, GRAY, "R-Tri"),
        Button(410, 5, 70, 25, GRAY, "E-Tri"),
        Button(485, 5, 70, 25, GRAY, "Rhombus"),
        Button(560, 5, 60, 25, GRAY, "Eraser"),
        Button(625, 5, 60, 25, WHITE, "Clear"),
    ]

    palette = ColorPalette(10, 40)
    size_up_btn = Button(700, 5, 25, 25, GRAY, "+")
    size_down_btn = Button(730, 5, 25, 25, GRAY, "-")
    size_font = pygame.font.Font(None, 18)

    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        canvas_y = mouse_y - TOOLBAR_HEIGHT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if y < TOOLBAR_HEIGHT:
                    # toolbar clicks
                    if buttons[0].is_clicked(event.pos):
                        current_mode = MODE_BRUSH
                    elif buttons[1].is_clicked(event.pos):
                        current_mode = MODE_LINE
                    elif buttons[2].is_clicked(event.pos):
                        current_mode = MODE_RECT
                    elif buttons[3].is_clicked(event.pos):
                        current_mode = MODE_SQUARE
                    elif buttons[4].is_clicked(event.pos):
                        current_mode = MODE_CIRCLE
                    elif buttons[5].is_clicked(event.pos):
                        current_mode = MODE_RIGHT_TRIANGLE
                    elif buttons[6].is_clicked(event.pos):
                        current_mode = MODE_EQUILATERAL
                    elif buttons[7].is_clicked(event.pos):
                        current_mode = MODE_RHOMBUS
                    elif buttons[8].is_clicked(event.pos):
                        current_mode = MODE_ERASER
                    elif buttons[9].is_clicked(event.pos):
                        canvas.fill(WHITE)

                    if size_up_btn.is_clicked(event.pos):
                        brush_size = min(50, brush_size + 2)
                        line_width = min(20, line_width + 1)
                        eraser_size = min(50, eraser_size + 2)
                    elif size_down_btn.is_clicked(event.pos):
                        brush_size = max(1, brush_size - 2)
                        line_width = max(1, line_width - 1)
                        eraser_size = max(5, eraser_size - 2)

                    palette.check_click(event.pos)
                    current_color = palette.selected_color
                else:
                    drawing = True
                    start_pos = (x, canvas_y)
                    current_pos = start_pos

                    if current_mode == MODE_BRUSH:
                        pygame.draw.circle(canvas, current_color, start_pos, brush_size)
                    elif current_mode == MODE_ERASER:
                        pygame.draw.circle(canvas, WHITE, start_pos, eraser_size)

            elif event.type == pygame.MOUSEMOTION:
                if canvas_y >= 0:
                    current_pos = (mouse_x, canvas_y)

                # freehand drawing
                if drawing and current_mode in [MODE_BRUSH, MODE_ERASER] and canvas_y >= 0:
                    new_pos = (mouse_x, canvas_y)
                    if current_mode == MODE_BRUSH:
                        pygame.draw.circle(canvas, current_color, new_pos, brush_size)
                        pygame.draw.line(canvas, current_color, start_pos, new_pos, brush_size * 2)
                    else:
                        pygame.draw.circle(canvas, WHITE, new_pos, eraser_size)
                        pygame.draw.line(canvas, WHITE, start_pos, new_pos, eraser_size * 2)
                    start_pos = new_pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing and canvas_y >= 0 and current_mode not in [MODE_BRUSH, MODE_ERASER]:
                    end_pos = (mouse_x, canvas_y)
                    draw_shape(canvas, current_mode, current_color, start_pos, end_pos, line_width)

                drawing = False
                start_pos = None
                current_pos = None

        screen.fill(GRAY)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # preview for shapes
        if drawing and current_mode not in [MODE_BRUSH, MODE_ERASER] and start_pos and current_pos:
            preview = screen.copy()
            draw_shape(preview, current_mode, LIGHT_GRAY, start_pos, current_pos, line_width)
            screen.blit(preview, (0, 0))

        pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, SCREEN_WIDTH, TOOLBAR_HEIGHT))
        pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (SCREEN_WIDTH, TOOLBAR_HEIGHT), 2)

        for button in buttons:
            button.draw(screen)

        palette.draw(screen)
        size_up_btn.draw(screen)
        size_down_btn.draw(screen)

        size_text = size_font.render(f"Size: {line_width}", True, BLACK)
        screen.blit(size_text, (770, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
