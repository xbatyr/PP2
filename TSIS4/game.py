import random

import pygame


WIDTH = 800
HEIGHT = 600
CELL = 20
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL
FPS = 60
GRID_COLOR = (30, 30, 30)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (45, 45, 45)
LIGHT = (90, 90, 90)
GREEN = (0, 220, 120)
RED = (240, 80, 80)
YELLOW = (255, 210, 0)
ORANGE = (255, 160, 60)
PURPLE = (170, 110, 255)
CYAN = (80, 220, 255)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

COLOR_OPTIONS = [
    [0, 220, 120],
    [70, 160, 255],
    [255, 180, 60],
    [220, 90, 200],
]


class SnakeGame:
    def __init__(self, settings, username, personal_best):
        self.settings = settings
        self.username = username or "Player"
        self.personal_best = personal_best
        self.reset()

    def reset(self):
        self.snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2 - 2, ROWS // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.level = 1
        self.foods = 0
        self.over = False
        self.shield = False
        self.effect = ""
        self.effect_end = 0
        self.last_move = 0
        self.message = ""
        self.message_end = 0
        self.last_power_spawn = 0
        self.obstacles = set()

        self.food = self.make_food()
        self.poison = self.make_poison()
        self.power = None

    def move_delay(self):
        delay = 170 - (self.level - 1) * 10
        if self.effect == "speed":
            delay -= 50
        elif self.effect == "slow":
            delay += 50
        return max(70, delay)

    def free_cell(self, extra=()):
        blocked = set(self.snake) | self.obstacles | set(extra)
        while True:
            cell = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))
            if cell not in blocked:
                return cell

    def make_food(self):
        # normal food from practice 11
        cell = self.free_cell()
        weight = random.choices([1, 2, 3], weights=[50, 35, 15])[0]
        color = RED if weight == 1 else ORANGE if weight == 2 else YELLOW
        return {"cell": cell, "weight": weight, "color": color, "end": pygame.time.get_ticks() + random.randint(5000, 9000)}

    def make_poison(self):
        return {"cell": self.free_cell([self.food["cell"]]), "color": (120, 0, 0)}

    def make_power(self):
        kind = random.choice(["speed", "slow", "shield"])
        color = CYAN if kind == "speed" else PURPLE if kind == "slow" else WHITE
        return {"cell": self.free_cell([self.food["cell"], self.poison["cell"]]), "kind": kind, "color": color, "end": pygame.time.get_ticks() + 8000}

    def set_message(self, text):
        if self.settings["sound"]:
            print("\a", end="")
        self.message = text
        self.message_end = pygame.time.get_ticks() + 1200

    def change_direction(self, direction):
        if direction[0] != -self.direction[0] or direction[1] != -self.direction[1]:
            self.next_direction = direction

    def next_head(self):
        x, y = self.snake[0]
        dx, dy = self.next_direction
        return x + dx, y + dy

    def use_shield(self):
        if self.shield:
            self.shield = False
            self.set_message("Shield used")
            return True
        return False

    def make_obstacles(self):
        if self.level < 3:
            self.obstacles = set()
            return

        head = self.snake[0]
        safe = {
            head,
            (head[0] + 1, head[1]),
            (head[0] - 1, head[1]),
            (head[0], head[1] + 1),
            (head[0], head[1] - 1),
        }
        walls = set()
        count = min(6 + self.level, 18)

        while len(walls) < count:
            cell = (random.randint(2, COLS - 3), random.randint(2, ROWS - 3))
            if cell not in self.snake and cell not in safe:
                walls.add(cell)

        self.obstacles = walls
        self.food = self.make_food()
        self.poison = self.make_poison()
        self.power = None

    def eat_food(self):
        self.score += self.food["weight"] * 10
        self.foods += 1
        self.personal_best = max(self.personal_best, self.score)
        self.food = self.make_food()

        if self.foods % 4 == 0:
            self.level += 1
            self.make_obstacles()
            self.set_message(f"Level {self.level}")

    def eat_poison(self):
        for _ in range(2):
            if len(self.snake) > 1:
                self.snake.pop()
        self.poison = self.make_poison()
        self.set_message("Poison")
        if len(self.snake) <= 1:
            self.over = True

    def eat_power(self):
        if self.power["kind"] == "shield":
            self.shield = True
            self.effect = ""
            self.effect_end = 0
            self.set_message("Shield")
        else:
            self.effect = self.power["kind"]
            self.effect_end = pygame.time.get_ticks() + 5000
            self.set_message("Speed up" if self.effect == "speed" else "Slow motion")
        self.power = None

    def power_text(self):
        if self.shield:
            return "Power: shield"
        if self.effect:
            left = max(0, (self.effect_end - pygame.time.get_ticks()) // 1000 + 1)
            return f"Power: {self.effect} {left}s"
        return "Power: none"

    def update(self):
        now = pygame.time.get_ticks()
        if self.over:
            return

        # timers for food and power-ups
        if now > self.food["end"]:
            self.food = self.make_food()
        if self.power and now > self.power["end"]:
            self.power = None
        if not self.power and now - self.last_power_spawn > 10000:
            self.power = self.make_power()
            self.last_power_spawn = now
        if self.effect and now > self.effect_end:
            self.effect = ""

        if now - self.last_move < self.move_delay():
            return

        self.last_move = now
        self.direction = self.next_direction
        head = self.next_head()

        hit_wall = head[0] < 0 or head[0] >= COLS or head[1] < 0 or head[1] >= ROWS
        hit_self = head in self.snake
        hit_block = head in self.obstacles

        if hit_wall or hit_self or hit_block:
            if self.use_shield():
                return
            self.over = True
            return

        self.snake.insert(0, head)

        if head == self.food["cell"]:
            self.eat_food()
        else:
            self.snake.pop()

        if head == self.poison["cell"]:
            self.eat_poison()

        if self.power and head == self.power["cell"]:
            self.eat_power()

    def draw_cell(self, screen, cell, color, border=None):
        rect = pygame.Rect(cell[0] * CELL, cell[1] * CELL, CELL, CELL)
        pygame.draw.rect(screen, color, rect)
        if border:
            pygame.draw.rect(screen, border, rect, 2)

    def draw(self, screen, font, small_font):
        screen.fill(BLACK)

        if self.settings["grid"]:
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL):
                pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

        for cell in self.obstacles:
            self.draw_cell(screen, cell, LIGHT, WHITE)

        for i, cell in enumerate(self.snake):
            color = tuple(self.settings["snake_color"])
            self.draw_cell(screen, cell, color if i else WHITE, BLACK if i else color)

        self.draw_cell(screen, self.food["cell"], self.food["color"], WHITE)
        self.draw_cell(screen, self.poison["cell"], self.poison["color"], WHITE)

        if self.power:
            self.draw_cell(screen, self.power["cell"], self.power["color"], BLACK)
            letter = "S" if self.power["kind"] == "shield" else "+" if self.power["kind"] == "speed" else "-"
            txt = small_font.render(letter, True, BLACK)
            screen.blit(txt, txt.get_rect(center=(self.power["cell"][0] * CELL + CELL // 2, self.power["cell"][1] * CELL + CELL // 2)))

        hud = [
            f"User: {self.username}",
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Best: {self.personal_best}",
        ]
        for i, text in enumerate(hud):
            screen.blit(font.render(text, True, WHITE), (12, 10 + i * 30))

        screen.blit(font.render(self.power_text(), True, CYAN), (12, 132))

        if self.message and pygame.time.get_ticks() < self.message_end:
            msg = font.render(self.message, True, YELLOW)
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, 26)))
