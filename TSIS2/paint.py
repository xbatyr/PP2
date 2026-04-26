import os

import pygame

from tools import *


pygame.init()

# main window
WIDTH = 1100
HEIGHT = 740
TOOLBAR_HEIGHT = 120

# basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
LIGHT_GRAY = (230, 230, 230)
BLUE = (90, 150, 255)
BG = (245, 245, 245)

# color palette
COLORS = [
    BLACK,
    WHITE,
    (255, 0, 0),
    (0, 180, 0),
    (0, 100, 255),
    (255, 200, 0),
    (255, 120, 0),
    (255, 100, 180),
    (140, 0, 255),
    (0, 170, 170),
    (120, 120, 120),
]

TOOL_DATA = [
    (TOOL_PENCIL, "Pencil", 16, 72),
    (TOOL_LINE, "Line", 94, 62),
    (TOOL_RECTANGLE, "Rect", 162, 62),
    (TOOL_SQUARE, "Square", 230, 72),
    (TOOL_CIRCLE, "Circle", 308, 68),
    (TOOL_RIGHT_TRIANGLE, "R-Tri", 382, 84),
    (TOOL_EQUILATERAL_TRIANGLE, "E-Tri", 472, 84),
    (TOOL_RHOMBUS, "Rhombus", 562, 84),
    (TOOL_ERASER, "Eraser", 652, 72),
    (TOOL_FILL, "Fill", 730, 62),
    (TOOL_TEXT, "Text", 798, 62),
]

SIZE_DATA = [(2, "1: 2px", 16, 66), (5, "2: 5px", 88, 74), (10, "3: 10px", 168, 82)]

KEY_SIZES = {pygame.K_1: 2, pygame.K_2: 5, pygame.K_3: 10}


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font, active=False):
        color = BLUE if active else LIGHT_GRAY
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=6)
        text_surface = font.render(self.text, True, BLACK)
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))


def draw_toolbar(screen, font, small_font, tool_buttons, size_buttons, color_rects, mode, size, color, canvas_rect, clear_button):
    # top panel
    pygame.draw.rect(screen, BG, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, GRAY, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    for tool_name, button in tool_buttons:
        button.draw(screen, font, tool_name == mode)

    for brush_size, button in size_buttons:
        button.draw(screen, font, brush_size == size)

    clear_button.draw(screen, font)

    # colors
    for palette_color, rect in color_rects:
        pygame.draw.rect(screen, palette_color, rect, border_radius=4)
        pygame.draw.rect(screen, BLACK, rect, 1, border_radius=4)
        if palette_color == color:
            pygame.draw.rect(screen, BLUE, rect, 3, border_radius=4)

    info1 = f"Tool: {mode}   Size: {size}px"
    info2 = "1/2/3 size   Ctrl+S save   Enter OK   Esc cancel"
    screen.blit(small_font.render(info1, True, BLACK), (560, 88))
    screen.blit(small_font.render(info2, True, BLACK), (560, 104))

    pygame.draw.rect(screen, BLACK, canvas_rect, 2)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS2 Paint")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 21)
    small_font = pygame.font.SysFont(None, 19)
    text_font = pygame.font.SysFont(None, 30)

    canvas_rect = pygame.Rect(10, TOOLBAR_HEIGHT + 10, WIDTH - 20, HEIGHT - TOOLBAR_HEIGHT - 20)
    canvas = pygame.Surface((canvas_rect.width, canvas_rect.height))
    canvas.fill(WHITE)

    # toolbar buttons
    tool_buttons = [(tool, Button(x, 10, w, 30, text)) for tool, text, x, w in TOOL_DATA]
    size_buttons = [(size, Button(x, 50, w, 28, text)) for size, text, x, w in SIZE_DATA]
    color_rects = [(color, pygame.Rect(16 + i * 38, 86, 32, 24)) for i, color in enumerate(COLORS)]

    clear_button = Button(866, 10, 70, 30, "Clear")

    # current state
    mode = TOOL_PENCIL
    current_color = BLACK
    brush_size = 5

    drawing = False
    start_pos = None
    end_pos = None
    prev_pos = None

    text_mode = False
    text_value = ""
    text_pos = (0, 0)
    cursor_tick = 0

    save_folder = os.path.join(os.path.dirname(__file__), "saves")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # brush size by keyboard
                if event.key in KEY_SIZES:
                    brush_size = KEY_SIZES[event.key]
                # save image
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    filename = save_canvas(canvas, save_folder)
                    print("Saved:", filename)
                # typing text
                elif text_mode:
                    if event.key == pygame.K_RETURN:
                        if text_value != "":
                            text_surface = text_font.render(text_value, True, current_color)
                            canvas.blit(text_surface, text_pos)
                        text_mode = False
                        text_value = ""
                    elif event.key == pygame.K_ESCAPE:
                        text_mode = False
                        text_value = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_value = text_value[:-1]
                    elif event.unicode.isprintable():
                        text_value += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos

                # clicks on toolbar
                if mouse_y < TOOLBAR_HEIGHT:
                    if clear_button.rect.collidepoint(event.pos):
                        canvas.fill(WHITE)
                        text_mode = False
                        text_value = ""

                    for tool_name, button in tool_buttons:
                        if button.rect.collidepoint(event.pos):
                            mode = tool_name
                            if mode != TOOL_TEXT:
                                text_mode = False
                                text_value = ""

                    for size_value, button in size_buttons:
                        if button.rect.collidepoint(event.pos):
                            brush_size = size_value

                    for palette_color, rect in color_rects:
                        if rect.collidepoint(event.pos):
                            current_color = palette_color

                # clicks on canvas
                elif canvas_rect.collidepoint(event.pos):
                    x = mouse_x - canvas_rect.left
                    y = mouse_y - canvas_rect.top
                    x, y = clamp_to_canvas((x, y), canvas)

                    if mode == TOOL_FILL:
                        flood_fill(canvas, (x, y), current_color)

                    elif mode == TOOL_TEXT:
                        text_mode = True
                        text_value = ""
                        text_pos = (x, y)

                    elif mode == TOOL_PENCIL or mode == TOOL_ERASER:
                        drawing = True
                        prev_pos = (x, y)
                        draw_color = WHITE if mode == TOOL_ERASER else current_color
                        pygame.draw.line(canvas, draw_color, prev_pos, prev_pos, brush_size)

                    elif mode in SHAPE_TOOLS:
                        drawing = True
                        start_pos = (x, y)
                        end_pos = (x, y)

            elif event.type == pygame.MOUSEMOTION:
                if drawing and canvas_rect.collidepoint(event.pos):
                    x = event.pos[0] - canvas_rect.left
                    y = event.pos[1] - canvas_rect.top
                    x, y = clamp_to_canvas((x, y), canvas)

                    if mode == TOOL_PENCIL or mode == TOOL_ERASER:
                        draw_color = WHITE if mode == TOOL_ERASER else current_color
                        pygame.draw.line(canvas, draw_color, prev_pos, (x, y), brush_size)
                        prev_pos = (x, y)

                    elif mode in SHAPE_TOOLS:
                        end_pos = (x, y)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # draw final shape
                if drawing and mode in SHAPE_TOOLS and start_pos and end_pos:
                    draw_shape(canvas, mode, current_color, start_pos, end_pos, brush_size)

                drawing = False
                start_pos = None
                end_pos = None
                prev_pos = None

        screen.fill(WHITE)

        # live preview for line and shapes
        if drawing and mode in SHAPE_TOOLS and start_pos and end_pos:
            preview = canvas.copy()
            draw_shape(preview, mode, current_color, start_pos, end_pos, brush_size)
            screen.blit(preview, canvas_rect.topleft)
        else:
            screen.blit(canvas, canvas_rect.topleft)

        # text preview before Enter
        if text_mode:
            cursor_tick = (cursor_tick + 1) % 60
            preview_text = text_value
            if cursor_tick < 30:
                preview_text += "|"
            text_surface = text_font.render(preview_text, True, current_color)
            screen.blit(text_surface, (canvas_rect.left + text_pos[0], canvas_rect.top + text_pos[1]))

        draw_toolbar(
            screen,
            font,
            small_font,
            tool_buttons,
            size_buttons,
            color_rects,
            mode,
            brush_size,
            current_color,
            canvas_rect,
            clear_button,
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
