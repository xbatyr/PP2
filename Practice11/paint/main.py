import pygame
import sys
import math

pygame.init()

# Screen settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
TOOLBAR_HEIGHT = 80

# Colors
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

# Drawing modes
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


# Button class for UI
class Button:
    def __init__(self, x, y, width, height, color, text="", text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 18)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Color palette class
class ColorPalette:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, 
                      CYAN, MAGENTA, ORANGE, PURPLE, GRAY]
        self.color_rects = []
        self.selected_color = BLACK
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


# Helper drawing functions
def draw_square(surface, color, start, end, width=2):
    x1, y1 = start
    x2, y2 = end
    size = max(abs(x2 - x1), abs(y2 - y1))
    if x2 < x1:
        x1 = x1 - size
    if y2 < y1:
        y1 = y1 - size
    rect = pygame.Rect(x1, y1, size, size)
    pygame.draw.rect(surface, color, rect, width)

def draw_right_triangle(surface, color, start, end, width=2):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, width)

def draw_equilateral_triangle(surface, color, start, end, width=2):
    x1, y1 = start
    x2, y2 = end
    base_width = abs(x2 - x1)
    height = base_width * math.sqrt(3) / 2
    if y2 < y1:
        height = -height
    points = [(x1, y2), (x2, y2), ((x1 + x2) // 2, y2 - height)]
    pygame.draw.polygon(surface, color, points, width)

def draw_rhombus(surface, color, start, end, width=2):
    x1, y1 = start
    x2, y2 = end
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    points = [(center_x, y1), (x2, center_y), (center_x, y2), (x1, center_y)]
    pygame.draw.polygon(surface, color, points, width)

def draw_preview(surface, mode, color, start, end, width=2):
    if mode == MODE_LINE:
        pygame.draw.line(surface, LIGHT_GRAY, start, end, width)
    elif mode == MODE_RECT:
        rect = pygame.Rect(start[0], start[1], end[0] - start[0], end[1] - start[1])
        pygame.draw.rect(surface, LIGHT_GRAY, rect, width)
    elif mode == MODE_SQUARE:
        x1, y1 = start
        x2, y2 = end
        size = max(abs(x2 - x1), abs(y2 - y1))
        if x2 < x1:
            x1 = x1 - size
        if y2 < y1:
            y1 = y1 - size
        rect = pygame.Rect(x1, y1, size, size)
        pygame.draw.rect(surface, LIGHT_GRAY, rect, width)
    elif mode == MODE_CIRCLE:
        center = start
        radius = int(((end[0] - center[0])**2 + (end[1] - center[1])**2)**0.5)
        pygame.draw.circle(surface, LIGHT_GRAY, center, radius, width)
    elif mode == MODE_RIGHT_TRIANGLE:
        x1, y1 = start
        x2, y2 = end
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, LIGHT_GRAY, points, width)
    elif mode == MODE_EQUILATERAL:
        x1, y1 = start
        x2, y2 = end
        base_width = abs(x2 - x1)
        height = base_width * math.sqrt(3) / 2
        if y2 < y1:
            height = -height
        points = [(x1, y2), (x2, y2), ((x1 + x2) // 2, y2 - height)]
        pygame.draw.polygon(surface, LIGHT_GRAY, points, width)
    elif mode == MODE_RHOMBUS:
        x1, y1 = start
        x2, y2 = end
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        points = [(center_x, y1), (x2, center_y), (center_x, y2), (x1, center_y)]
        pygame.draw.polygon(surface, LIGHT_GRAY, points, width)

def main():
    canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)
    
    drawing = False
    start_pos = None
    current_pos = None
    current_mode = MODE_BRUSH
    brush_size = 5
    line_width = 3
    current_color = BLACK
    eraser_size = 20
    
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
        Button(625, 5, 60, 25, WHITE, "Clear")
    ]
    
    color_palette = ColorPalette(10, 40)
    size_up_btn = Button(700, 5, 25, 25, GRAY, "+")
    size_down_btn = Button(730, 5, 25, 25, GRAY, "-")
    size_text_font = pygame.font.Font(None, 18)
    
    running = True
    
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        canvas_mouse_y = mouse_y - TOOLBAR_HEIGHT
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                if y < TOOLBAR_HEIGHT:
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
                    
                    color_palette.check_click(event.pos)
                    current_color = color_palette.selected_color
                
                else:
                    drawing = True
                    start_pos = (x, canvas_mouse_y)
                    current_pos = start_pos
                    if current_mode == MODE_BRUSH:
                        pygame.draw.circle(canvas, current_color, start_pos, brush_size)
                    elif current_mode == MODE_ERASER:
                        pygame.draw.circle(canvas, WHITE, start_pos, eraser_size)
            
            elif event.type == pygame.MOUSEMOTION:
                if canvas_mouse_y >= 0:
                    current_pos = (mouse_x, canvas_mouse_y)
                
                if drawing and current_mode in [MODE_BRUSH, MODE_ERASER]:
                    if canvas_mouse_y >= 0:
                        canvas_pos = (mouse_x, canvas_mouse_y)
                        if current_mode == MODE_BRUSH:
                            pygame.draw.circle(canvas, current_color, canvas_pos, brush_size)
                            if start_pos:
                                pygame.draw.line(canvas, current_color, start_pos, canvas_pos, brush_size * 2)
                                start_pos = canvas_pos
                        else:
                            pygame.draw.circle(canvas, WHITE, canvas_pos, eraser_size)
                            if start_pos:
                                pygame.draw.line(canvas, WHITE, start_pos, canvas_pos, eraser_size * 2)
                                start_pos = canvas_pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing and canvas_mouse_y >= 0:
                    end_pos = (mouse_x, canvas_mouse_y)
                    if current_mode == MODE_LINE:
                        pygame.draw.line(canvas, current_color, start_pos, end_pos, line_width)
                    elif current_mode == MODE_RECT:
                        rect = pygame.Rect(start_pos[0], start_pos[1], 
                                         end_pos[0] - start_pos[0], 
                                         end_pos[1] - start_pos[1])
                        pygame.draw.rect(canvas, current_color, rect, line_width)
                    elif current_mode == MODE_SQUARE:
                        draw_square(canvas, current_color, start_pos, end_pos, line_width)
                    elif current_mode == MODE_CIRCLE:
                        center = start_pos
                        radius = int(((end_pos[0] - center[0])**2 + 
                                    (end_pos[1] - center[1])**2)**0.5)
                        pygame.draw.circle(canvas, current_color, center, radius, line_width)
                    elif current_mode == MODE_RIGHT_TRIANGLE:
                        draw_right_triangle(canvas, current_color, start_pos, end_pos, line_width)
                    elif current_mode == MODE_EQUILATERAL:
                        draw_equilateral_triangle(canvas, current_color, start_pos, end_pos, line_width)
                    elif current_mode == MODE_RHOMBUS:
                        draw_rhombus(canvas, current_color, start_pos, end_pos, line_width)
                
                drawing = False
                start_pos = None
                current_pos = None
        
        screen.fill(GRAY)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))
        
        if drawing and current_mode not in [MODE_BRUSH, MODE_ERASER] and current_pos:
            preview_surface = screen.copy()
            if start_pos and current_pos:
                draw_preview(preview_surface, current_mode, current_color, start_pos, current_pos, line_width)
            screen.blit(preview_surface, (0, 0))
        
        pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, SCREEN_WIDTH, TOOLBAR_HEIGHT))
        pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (SCREEN_WIDTH, TOOLBAR_HEIGHT), 2)
        
        for button in buttons:
            button.draw(screen)
        
        color_palette.draw(screen)
        size_up_btn.draw(screen)
        size_down_btn.draw(screen)
        
        # Size/width indicator
        if current_mode == MODE_LINE:
            size_text = size_text_font.render(f"Width: {line_width}", True, BLACK)
        elif current_mode in [MODE_BRUSH, MODE_ERASER]:
            size_text = size_text_font.render(f"Size: {brush_size}", True, BLACK)
        else:
            size_text = size_text_font.render(f"Width: {line_width}", True, BLACK)
        screen.blit(size_text, (760, 55))
        
        # Mode indicator - moved to right side
        mode_text = size_text_font.render(f"Mode: {current_mode.upper()}", True, BLACK)
        screen.blit(mode_text, (760, 35))
        
        # Color preview icon
        preview_x = 850
        preview_y = 35
        if current_mode == MODE_ERASER:
            pygame.draw.circle(screen, WHITE, (preview_x, preview_y), 8)
            pygame.draw.circle(screen, BLACK, (preview_x, preview_y), 8, 1)
        elif current_mode == MODE_LINE:
            pygame.draw.line(screen, current_color, (preview_x-10, preview_y-5), 
                           (preview_x+10, preview_y+5), 2)
        else:
            pygame.draw.circle(screen, current_color, (preview_x, preview_y), 8)
            pygame.draw.circle(screen, BLACK, (preview_x, preview_y), 8, 1)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()