import sys

import pygame

from persistence import add_score, load_leaderboard, load_settings, save_settings
from racer import BLACK, BLUE, CAR_COLORS, FPS, HEIGHT, RacerGame, WHITE, WIDTH, draw_car_sprite
from ui import Button, draw_box, draw_text


# main window setup
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 RACER")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("verdana", 34, bold=True)
font = pygame.font.SysFont("verdana", 22)
small_font = pygame.font.SysFont("verdana", 18)

settings = load_settings()
leaderboard = load_leaderboard()

state = "menu"
name = ""
game = None
result = None
saved_result = False

# menu buttons
menu_buttons = [
    ("play", Button(120, 180, 160, 45, "Play")),
    ("leaderboard", Button(120, 240, 160, 45, "Leaderboard")),
    ("settings", Button(120, 300, 160, 45, "Settings")),
    ("quit", Button(120, 360, 160, 45, "Quit")),
]

name_buttons = [("start", Button(90, 360, 100, 42, "Start")), ("back", Button(210, 360, 100, 42, "Back"))]
over_buttons = [("retry", Button(90, 430, 100, 42, "Retry")), ("menu", Button(210, 430, 100, 42, "Main Menu"))]
back_button = Button(140, 575, 120, 42, "Back")
sound_button = Button(125, 175, 150, 40, "Sound")

color_buttons = [
    ("blue", Button(60, 275, 70, 40, "Blue")),
    ("red", Button(145, 275, 70, 40, "Red")),
    ("green", Button(230, 275, 70, 40, "Green")),
    ("yellow", Button(315, 275, 70, 40, "Yellow")),
]

difficulty_buttons = [
    ("easy", Button(70, 385, 80, 40, "Easy")),
    ("normal", Button(160, 385, 80, 40, "Normal")),
    ("hard", Button(250, 385, 80, 40, "Hard")),
]


def open_game():
    # start new race
    global game, state, saved_result
    player_name = name.strip() or "Player"
    game = RacerGame(settings, player_name)
    saved_result = False
    state = "game"


def draw_menu():
    # draw menu screen
    screen.fill((216, 228, 242))
    draw_box(screen, pygame.Rect(40, 35, 320, 88), (238, 244, 250))
    draw_text(screen, "TSIS 3 RACER", title_font, BLACK, WIDTH // 2, 79, True)
    draw_car_sprite(screen, 108, 520, settings["car_color"])
    draw_car_sprite(screen, 292, 230, "red", True)
    draw_text(screen, "Use arrows or A/D to change lanes", small_font, BLACK, WIDTH // 2, 560, True)
    for _, button in menu_buttons:
        button.draw(screen, font)


def draw_name_screen():
    # screen for player name
    screen.fill((235, 240, 245))
    draw_text(screen, "Enter Your Name", title_font, BLACK, WIDTH // 2, 120, True)
    draw_box(screen, pygame.Rect(70, 220, 260, 55))
    draw_text(screen, name or "Type here...", font, BLUE if name else (120, 120, 120), 90, 235)
    draw_text(screen, "Press Enter or click Start", small_font, BLACK, WIDTH // 2, 305, True)
    draw_text(screen, "Goal: survive, collect coins and reach finish", small_font, BLACK, WIDTH // 2, 330, True)
    for _, button in name_buttons:
        button.draw(screen, font)


def draw_settings():
    # show settings and car
    screen.fill((232, 239, 231))
    draw_text(screen, "Settings", title_font, BLACK, WIDTH // 2, 85, True)

    draw_text(screen, f"Sound: {'On' if settings['sound'] else 'Off'}", font, BLACK, 120, 145)
    sound_button.draw(screen, font, settings["sound"])

    draw_text(screen, "Car Color", font, BLACK, 145, 240)
    for color_name, button in color_buttons:
        button.draw(screen, small_font, settings["car_color"] == color_name)

    draw_text(screen, "Difficulty", font, BLACK, 145, 350)
    for diff_name, button in difficulty_buttons:
        button.draw(screen, small_font, settings["difficulty"] == diff_name)

    draw_text(screen, "Preview", small_font, BLACK, WIDTH // 2, 450, True)
    draw_car_sprite(screen, WIDTH // 2, 525, settings["car_color"])
    back_button.draw(screen, font)


def draw_leaderboard():
    # show best results
    screen.fill((245, 238, 228))
    draw_text(screen, "Top 10 Leaderboard", title_font, BLACK, WIDTH // 2, 65, True)
    draw_box(screen, pygame.Rect(30, 110, 340, 430))

    y = 135
    if leaderboard:
        for i, item in enumerate(leaderboard, start=1):
            text = f"{i}. {item['name']}  Score:{item['score']}  Dist:{item['distance']}  Coins:{item['coins']}"
            draw_text(screen, text, small_font, BLACK, 45, y)
            y += 36
    else:
        draw_text(screen, "No scores yet", font, BLACK, WIDTH // 2, 260, True)

    back_button.draw(screen, font)


def draw_game_over():
    # end screen
    screen.fill((245, 230, 230) if not result["win"] else (228, 245, 228))
    title = "Finished!" if result["win"] else "Game Over"
    draw_text(screen, title, title_font, BLACK, WIDTH // 2, 115, True)
    draw_box(screen, pygame.Rect(70, 180, 260, 180))
    draw_text(screen, f"Name: {result['name']}", font, BLACK, 95, 210)
    draw_text(screen, f"Score: {result['score']}", font, BLACK, 95, 245)
    draw_text(screen, f"Distance: {result['distance']}", font, BLACK, 95, 280)
    draw_text(screen, f"Coins: {result['coins']}", font, BLACK, 95, 315)
    draw_text(screen, "Result was saved to leaderboard", small_font, BLACK, WIDTH // 2, 385, True)
    draw_car_sprite(screen, 200, 520, settings["car_color"])
    for _, button in over_buttons:
        button.draw(screen, font)


running = True
while running:
    # handle input by screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for action, button in menu_buttons:
                    if button.rect.collidepoint(event.pos):
                        if action == "play":
                            state = "name"
                        elif action == "leaderboard":
                            leaderboard = load_leaderboard()
                            state = "leaderboard"
                        elif action == "settings":
                            state = "settings"
                        else:
                            running = False

        elif state == "name":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    open_game()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable() and len(name) < 12:
                    name += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for action, button in name_buttons:
                    if button.rect.collidepoint(event.pos):
                        if action == "start":
                            open_game()
                        else:
                            state = "menu"

        elif state == "settings":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if sound_button.rect.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                for color_name, button in color_buttons:
                    if button.rect.collidepoint(event.pos):
                        settings["car_color"] = color_name
                        save_settings(settings)

                for diff_name, button in difficulty_buttons:
                    if button.rect.collidepoint(event.pos):
                        settings["difficulty"] = diff_name
                        save_settings(settings)

                if back_button.rect.collidepoint(event.pos):
                    state = "menu"

        elif state == "leaderboard":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back_button.rect.collidepoint(event.pos):
                state = "menu"

        elif state == "game":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "menu"
            else:
                game.handle_event(event)

        elif state == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for action, button in over_buttons:
                    if button.rect.collidepoint(event.pos):
                        if action == "retry":
                            open_game()
                        else:
                            state = "menu"

    if state == "menu":
        draw_menu()

    elif state == "name":
        draw_name_screen()

    elif state == "settings":
        draw_settings()

    elif state == "leaderboard":
        draw_leaderboard()

    elif state == "game":
        # update race and save once
        game.update()
        game.draw(screen, font, small_font)

        if game.done and not saved_result:
            result = game.result()
            leaderboard = add_score(result["name"], result["score"], result["distance"], result["coins"])
            saved_result = True
            state = "game_over"

    elif state == "game_over":
        draw_game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
