import math
import os
from datetime import datetime

import pygame


# tool names
TOOL_PENCIL = "pencil"
TOOL_LINE = "line"
TOOL_RECTANGLE = "rectangle"
TOOL_SQUARE = "square"
TOOL_CIRCLE = "circle"
TOOL_RIGHT_TRIANGLE = "right_triangle"
TOOL_EQUILATERAL_TRIANGLE = "equilateral_triangle"
TOOL_RHOMBUS = "rhombus"
TOOL_ERASER = "eraser"
TOOL_FILL = "fill"
TOOL_TEXT = "text"

# tools that need start and end point
SHAPE_TOOLS = [
    TOOL_LINE,
    TOOL_RECTANGLE,
    TOOL_SQUARE,
    TOOL_CIRCLE,
    TOOL_RIGHT_TRIANGLE,
    TOOL_EQUILATERAL_TRIANGLE,
    TOOL_RHOMBUS,
]


def clamp_to_canvas(point, canvas):
    # keep mouse inside canvas
    x = max(0, min(canvas.get_width() - 1, point[0]))
    y = max(0, min(canvas.get_height() - 1, point[1]))
    return x, y


def get_rectangle(start, end):
    # rectangle should work in any direction
    x1, y1 = start
    x2, y2 = end
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return pygame.Rect(left, top, width, height)


def draw_square(surface, color, start, end, width):
    # square uses the bigger side
    x1, y1 = start
    x2, y2 = end
    side = max(abs(x2 - x1), abs(y2 - y1))

    if x2 >= x1:
        left = x1
    else:
        left = x1 - side

    if y2 >= y1:
        top = y1
    else:
        top = y1 - side

    pygame.draw.rect(surface, color, (left, top, side, side), width)


def draw_right_triangle(surface, color, start, end, width):
    # 3 simple points
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, color, start, end, width):
    # height comes from sqrt(3)
    x1, _ = start
    x2, y2 = end

    left = min(x1, x2)
    right = max(x1, x2)
    side = right - left
    middle = (left + right) // 2
    height = int(side * math.sqrt(3) / 2)

    if end[1] <= start[1]:
        top_y = y2 - height
    else:
        top_y = y2 + height

    points = [(left, y2), (right, y2), (middle, top_y)]
    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, color, start, end, width):
    # rhombus inside dragged area
    x1, y1 = start
    x2, y2 = end
    middle_x = (x1 + x2) // 2
    middle_y = (y1 + y2) // 2
    points = [(middle_x, y1), (x2, middle_y), (middle_x, y2), (x1, middle_y)]
    pygame.draw.polygon(surface, color, points, width)


def draw_shape(surface, tool, color, start, end, width):
    # one function for all shapes
    if tool == TOOL_LINE:
        pygame.draw.line(surface, color, start, end, width)

    elif tool == TOOL_RECTANGLE:
        rect = get_rectangle(start, end)
        pygame.draw.rect(surface, color, rect, width)

    elif tool == TOOL_SQUARE:
        draw_square(surface, color, start, end, width)

    elif tool == TOOL_CIRCLE:
        radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
        if radius > 0:
            pygame.draw.circle(surface, color, start, radius, width)

    elif tool == TOOL_RIGHT_TRIANGLE:
        draw_right_triangle(surface, color, start, end, width)

    elif tool == TOOL_EQUILATERAL_TRIANGLE:
        draw_equilateral_triangle(surface, color, start, end, width)

    elif tool == TOOL_RHOMBUS:
        draw_rhombus(surface, color, start, end, width)


def flood_fill(surface, start, new_color):
    # fill until border color changes
    x, y = start

    if x < 0 or y < 0 or x >= surface.get_width() or y >= surface.get_height():
        return

    old_color = surface.get_at((x, y))
    new_color = pygame.Color(*new_color)

    if old_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        x, y = stack.pop()

        if x < 0 or y < 0 or x >= surface.get_width() or y >= surface.get_height():
            continue

        if surface.get_at((x, y)) != old_color:
            continue

        surface.set_at((x, y), new_color)
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))


def save_canvas(surface, folder):
    # save with current time in file name
    os.makedirs(folder, exist_ok=True)
    time_text = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"paint_{time_text}.png"
    full_path = os.path.join(folder, file_name)
    pygame.image.save(surface, full_path)
    return full_path
