import json
import os
import sys

import pygame

from db import get_db_error, get_personal_best, get_top_scores, init_db, save_result
from game import BLACK, COLOR_OPTIONS, DOWN, FPS, HEIGHT, LEFT, ORANGE, PURPLE, RED, RIGHT, SnakeGame, UP, WHITE, WIDTH


pygame.init()

BASE_DIR = os.path.dirname(__file__)
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

DEFAULT_SETTINGS = {
    "snake_color": [0, 220, 120],
    "grid": True,
    "sound": True,
}

BLUE = (90, 150, 255)


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=2)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font, active=False):
        color = BLUE if active else (235, 235, 235)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = (245, 245, 245) if not active else (110, 180, 255)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)
        text = font.render(self.text, True, BLACK)
        screen.blit(text, text.get_rect(center=self.rect.center))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 SNAKE")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("verdana", 36, bold=True)
font = pygame.font.SysFont("verdana", 24)
small_font = pygame.font.SysFont("verdana", 18)

settings = load_settings()
db_ready = init_db()

state = "menu"
username = ""
game = None
result_saved = False
top_scores = []

menu_buttons = [
    ("play", Button(310, 260, 180, 44, "Play")),
    ("leaderboard", Button(310, 320, 180, 44, "Leaderboard")),
    ("settings", Button(310, 380, 180, 44, "Settings")),
    ("quit", Button(310, 440, 180, 44, "Quit")),
]
over_buttons = [("retry", Button(265, 420, 120, 42, "Retry")), ("menu", Button(415, 420, 120, 42, "Main Menu"))]
back_button = Button(330, 530, 140, 42, "Back")
save_back_button = Button(300, 520, 200, 42, "Save & Back")
grid_button = Button(330, 210, 150, 40, "Grid")
sound_button = Button(330, 280, 150, 40, "Sound")
color_buttons = [(color, Button(245 + i * 80, 390, 60, 40, "")) for i, color in enumerate(COLOR_OPTIONS)]


def start_game():
    global game, state, result_saved
    name = username.strip() or "Player"
    best = get_personal_best(name)
    game = SnakeGame(settings, name, best)
    result_saved = False
    state = "game"


def draw_text(text, x, y, color=BLACK, center=False, use_small=False, use_title=False):
    current_font = title_font if use_title else small_font if use_small else font
    image = current_font.render(str(text), True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)


def draw_panel(rect):
    pygame.draw.rect(screen, (242, 246, 248), rect, border_radius=12)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=12)


def draw_menu():
    screen.fill((224, 236, 228))
    draw_panel(pygame.Rect(150, 40, 500, 110))
    draw_text("TSIS 4 SNAKE", WIDTH // 2, 90, center=True, use_title=True)
    draw_text("Username", 240, 170)
    draw_panel(pygame.Rect(240, 200, 320, 46))
    draw_text(username or "Type name here...", 258, 212, PURPLE if username else (120, 120, 120), use_small=not username)
    draw_text("Press Enter or click Play", WIDTH // 2, 250, center=True, use_small=True)
    for _, button in menu_buttons:
        button.draw(screen, font)


def draw_settings_screen():
    screen.fill((233, 239, 248))
    draw_text("Settings", WIDTH // 2, 80, center=True, use_title=True)
    draw_text(f"Grid: {'On' if settings['grid'] else 'Off'}", 250, 170)
    grid_button.draw(screen, font, settings["grid"])
    draw_text(f"Sound: {'On' if settings['sound'] else 'Off'}", 240, 240)
    sound_button.draw(screen, font, settings["sound"])
    draw_text("Snake Color", WIDTH // 2, 340, center=True)

    for color, button in color_buttons:
        active = settings["snake_color"] == color
        pygame.draw.rect(screen, color, button.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE if active else BLACK, button.rect, 3, border_radius=8)

    save_back_button.draw(screen, font)


def draw_leaderboard():
    screen.fill((247, 239, 230))
    draw_text("Leaderboard", WIDTH // 2, 65, center=True, use_title=True)
    draw_panel(pygame.Rect(55, 100, 690, 400))
    draw_text("Rank", 75, 120, ORANGE)
    draw_text("User", 145, 120, ORANGE)
    draw_text("Score", 300, 120, ORANGE)
    draw_text("Level", 430, 120, ORANGE)
    draw_text("Date", 530, 120, ORANGE)

    y = 155
    if top_scores:
        for i, row in enumerate(top_scores, start=1):
            date_text = row[3].strftime("%Y-%m-%d") if row[3] else "-"
            draw_text(i, 85, y, use_small=True)
            draw_text(row[0], 135, y, use_small=True)
            draw_text(row[1], 305, y, use_small=True)
            draw_text(row[2], 440, y, use_small=True)
            draw_text(date_text, 530, y, use_small=True)
            y += 30
    else:
        error_text = get_db_error()
        if error_text:
            draw_text("Database problem:", WIDTH // 2, 260, center=True)
            draw_text(error_text[:70], WIDTH // 2, 300, center=True, use_small=True)
        else:
            draw_text("Database is empty", WIDTH // 2, 290, center=True)

    back_button.draw(screen, font)


def draw_game_over():
    screen.fill((245, 229, 229))
    draw_text("Game Over", WIDTH // 2, 100, RED, True, use_title=True)
    draw_panel(pygame.Rect(220, 160, 360, 190))
    draw_text(f"User: {game.username}", 250, 200)
    draw_text(f"Score: {game.score}", 250, 235)
    draw_text(f"Level: {game.level}", 250, 270)
    draw_text(f"Best: {game.personal_best}", 250, 305)
    if get_db_error():
        draw_text("DB save failed", WIDTH // 2, 370, RED, center=True, use_small=True)
    for _, button in over_buttons:
        button.draw(screen, font)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    start_game()
                elif event.unicode.isprintable() and len(username) < 12:
                    username += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for action, button in menu_buttons:
                    if button.rect.collidepoint(event.pos):
                        if action == "play":
                            start_game()
                        elif action == "leaderboard":
                            top_scores = get_top_scores()
                            state = "leaderboard"
                        elif action == "settings":
                            state = "settings"
                        else:
                            running = False

        elif state == "settings":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if grid_button.rect.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]
                elif sound_button.rect.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                else:
                    for color, button in color_buttons:
                        if button.rect.collidepoint(event.pos):
                            settings["snake_color"] = color

                if save_back_button.rect.collidepoint(event.pos):
                    save_settings(settings)
                    state = "menu"

        elif state == "leaderboard":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back_button.rect.collidepoint(event.pos):
                state = "menu"

        elif state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    game.change_direction(UP)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    game.change_direction(DOWN)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    game.change_direction(LEFT)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    game.change_direction(RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    state = "menu"

        elif state == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for action, button in over_buttons:
                    if button.rect.collidepoint(event.pos):
                        if action == "retry":
                            start_game()
                        else:
                            state = "menu"

    if state == "menu":
        draw_menu()

    elif state == "settings":
        draw_settings_screen()

    elif state == "leaderboard":
        draw_leaderboard()

    elif state == "game":
        game.update()
        game.draw(screen, font, small_font)
        if game.over and not result_saved:
            save_result(game.username, game.score, game.level)
            result_saved = True
            state = "game_over"

    elif state == "game_over":
        draw_game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
