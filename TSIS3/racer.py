import os
import random

import pygame


# game sizes and colors
WIDTH = 400
HEIGHT = 650
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)
LIGHT_GRAY = (210, 210, 210)
GREEN = (60, 160, 70)
RED = (220, 70, 70)
YELLOW = (255, 210, 0)
BLUE = (90, 150, 255)
CYAN = (0, 220, 255)
PURPLE = (170, 110, 255)
ORANGE = (255, 150, 60)

ROAD_LEFT = 70
ROAD_RIGHT = 330
LANES = [113, 200, 287]

CAR_W = 50
CAR_H = 86

BASE_SPEED = {"easy": 6, "normal": 7, "hard": 8}
FINISH_DISTANCE = {"easy": 4200, "normal": 5400, "hard": 6800}
DIFF_BONUS = {"easy": 0, "normal": 10, "hard": 20}
DISTANCE_STEP = 0.28

CAR_COLORS = {
    "blue": BLUE,
    "red": (240, 80, 80),
    "green": (60, 190, 90),
    "yellow": (240, 210, 50),
}

BASE_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Practice11", "racer"))


def load_image(name, size):
    # load image if it exists
    path = os.path.join(ASSET_DIR, name)
    if os.path.exists(path):
        image = pygame.image.load(path)
        return pygame.transform.smoothscale(image, size)
    return None


ROAD_IMAGE = load_image("AnimatedStreet.png", (WIDTH, HEIGHT))
PLAYER_IMAGE = load_image("Player.png", (CAR_W, CAR_H))
ENEMY_IMAGE = load_image("Enemy.png", (CAR_W, CAR_H))
COIN_IMAGE = load_image("coin.png", (26, 26))


def draw_car_sprite(screen, x, y, color_name="blue", enemy=False):
    # draw car image or simple car
    image = ENEMY_IMAGE if enemy else PLAYER_IMAGE
    color = CAR_COLORS.get(color_name, BLUE)

    pygame.draw.ellipse(screen, (40, 40, 40), (x - 20, y + 28, 40, 14))

    if image:
        rect = image.get_rect(center=(int(x), int(y)))
        screen.blit(image, rect)
        stripe = pygame.Rect(rect.centerx - 12, rect.top + 10, 24, 10)
        pygame.draw.rect(screen, color, stripe, border_radius=4)
        pygame.draw.rect(screen, BLACK, stripe, 1, border_radius=4)
        return

    rect = pygame.Rect(x - 22, y - 38, 44, 76)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)
    pygame.draw.rect(screen, WHITE, (x - 14, y - 26, 28, 18), border_radius=6)
    pygame.draw.rect(screen, WHITE, (x - 14, y + 6, 28, 14), border_radius=6)


def draw_coin_sprite(screen, x, y, weight, font):
    # draw coin and value
    if COIN_IMAGE:
        rect = COIN_IMAGE.get_rect(center=(x, y))
        screen.blit(COIN_IMAGE, rect)
    else:
        pygame.draw.circle(screen, YELLOW, (x, y), 12)
        pygame.draw.circle(screen, BLACK, (x, y), 12, 2)

    text = font.render(str(weight), True, BLACK)
    badge = pygame.Rect(x + 6, y - 18, 14, 14)
    pygame.draw.ellipse(screen, WHITE, badge)
    pygame.draw.ellipse(screen, BLACK, badge, 1)
    screen.blit(text, text.get_rect(center=badge.center))


class RacerGame:
    def __init__(self, settings, username):
        self.settings = settings
        self.username = username or "Player"
        self.reset()

    def reset(self):
        # reset all game data
        self.player_lane = 1
        self.player_x = LANES[1]
        self.target_x = LANES[1]
        self.player_y = 545
        self.road_y = 0

        # score and progress
        self.coins = 0
        self.coin_value = 0
        self.bonus = 0
        self.score = 0
        self.progress = 0
        self.distance = 0
        self.finish_distance = FINISH_DISTANCE[self.settings["difficulty"]]

        # game state
        self.done = False
        self.win = False
        self.extra_hit = 0
        self.active_power = ""
        self.power_time = 0
        self.slow_time = 0
        self.strip_time = 0
        self.hit_cooldown = 60
        self.message = "GO!"
        self.message_time = 70

        # objects on road
        self.coins_list = []
        self.traffic = []
        self.hazards = []
        self.events = []
        self.powerups = []

        # spawn timers
        self.coin_timer = 0
        self.traffic_timer = 0
        self.hazard_timer = 0
        self.event_timer = 0
        self.power_timer = 0

    def beep(self):
        # make beep if sound is on
        if self.settings.get("sound"):
            print("\a", end="")

    def say(self, text, time=70):
        self.message = text
        self.message_time = time

    def player_rect(self):
        return pygame.Rect(self.player_x - 21, self.player_y - 36, 42, 72)

    def handle_event(self, event):
        # move left or right
        if event.type != pygame.KEYDOWN:
            return

        if event.key in (pygame.K_LEFT, pygame.K_a) and self.player_lane > 0:
            self.player_lane -= 1
            self.target_x = LANES[self.player_lane]
        elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.player_lane < 2:
            self.player_lane += 1
            self.target_x = LANES[self.player_lane]

    def lane_busy(self, lane):
        # stop overlap at start
        for items in [self.coins_list, self.traffic, self.hazards, self.powerups]:
            for item in items:
                if item["lane"] == lane and item["y"] < 140:
                    return True
        return False

    def moving_barrier_active(self):
        for item in self.events:
            if item["kind"] == "moving_barrier" and -40 < item["y"] < 320:
                return True
        return False

    def blocked_lanes(self):
        # bad lanes now
        blocked = set()

        for item in self.traffic:
            if -80 < item["y"] < 320:
                blocked.add(item["lane"])

        for item in self.hazards:
            if item["kind"] in ["barrier", "pothole"] and -60 < item["y"] < 320:
                blocked.add(item["lane"])

        return blocked

    def spawn_lane(self, avoid_player=True):
        blocked = self.blocked_lanes()
        lanes = [0, 1, 2]
        random.shuffle(lanes)

        for lane in lanes:
            if avoid_player and lane == self.player_lane:
                continue
            if lane in blocked:
                continue
            if self.lane_busy(lane):
                continue
            return lane

        return None

    def pick_lane(self, avoid_player=True):
        lanes = [0, 1, 2]
        random.shuffle(lanes)

        for lane in lanes:
            if avoid_player and lane == self.player_lane:
                continue
            if not self.lane_busy(lane):
                return lane

        return random.choice(lanes)

    def speed_now(self):
        # speed gets higher
        level = 1 + self.progress // 700
        speed = BASE_SPEED[self.settings["difficulty"]]
        speed += level * 0.28
        speed += self.coin_value * 0.015

        if self.active_power == "nitro":
            speed += 3
        if self.strip_time > 0:
            speed += 2
        if self.slow_time > 0:
            speed -= 2

        return max(4, speed)

    def spawn_coin(self):
        # coin can be in any lane
        lane = self.pick_lane(False)
        weight = random.choices([1, 2, 3], weights=[50, 30, 20])[0]
        self.coins_list.append({"lane": lane, "x": LANES[lane], "y": -30, "weight": weight})

    def spawn_traffic(self):
        # keep one free lane
        if self.moving_barrier_active() or len(self.blocked_lanes()) >= 2:
            return

        lane = self.spawn_lane(True)
        if lane is None:
            return

        color_name = random.choice(list(CAR_COLORS.keys()))
        self.traffic.append({"lane": lane, "x": LANES[lane], "y": -90, "color_name": color_name})

    def spawn_hazards(self):
        # hazards must not block all lanes
        if self.moving_barrier_active():
            return

        blocked = self.blocked_lanes()
        free_lanes = []
        for lane in [0, 1, 2]:
            if lane not in blocked and not self.lane_busy(lane):
                free_lanes.append(lane)

        if len(free_lanes) <= 1:
            return

        random.shuffle(free_lanes)
        safe_lane = free_lanes[0]
        for lane in free_lanes[1:]:
            kind = random.choice(["barrier", "oil", "pothole"])
            self.hazards.append({"lane": lane, "x": LANES[lane], "y": -40, "kind": kind})

            # add one more hazard only
            if blocked or random.random() < 0.5:
                break

    def spawn_event(self):
        kind = random.choice(["moving_barrier", "speed_bump", "boost_strip"])
        if kind == "moving_barrier":
            if self.moving_barrier_active() or self.blocked_lanes():
                return
            self.events.append({"kind": kind, "x": ROAD_LEFT + 30, "y": -25, "dx": 4})
            return

        lane = self.spawn_lane(False)
        if lane is None:
            return
        self.events.append({"kind": kind, "lane": lane, "x": LANES[lane], "y": -20})

    def spawn_powerup(self):
        if self.powerups:
            return
        lane = self.spawn_lane(True)
        if lane is None:
            return
        kind = random.choice(["nitro", "shield", "repair"])
        self.powerups.append({"lane": lane, "x": LANES[lane], "y": -30, "kind": kind, "time": 360})

    def use_protection(self):
        if self.active_power == "shield":
            self.active_power = ""
            self.power_time = 0
            self.hit_cooldown = 70
            self.bonus += 30
            self.say("Shield used")
            return True

        if self.extra_hit > 0:
            self.extra_hit -= 1
            self.hit_cooldown = 70
            self.bonus += 20
            self.say("Repair saved you")
            return True

        return False

    def hit_player(self):
        if self.hit_cooldown > 0:
            return
        self.beep()
        if not self.use_protection():
            self.done = True

    def update_power(self):
        if self.active_power == "nitro":
            self.power_time -= 1
            if self.power_time <= 0:
                self.active_power = ""
                self.say("Nitro ended", 45)

        if self.slow_time > 0:
            self.slow_time -= 1
        if self.strip_time > 0:
            self.strip_time -= 1
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
        if self.message_time > 0:
            self.message_time -= 1

    def update_spawns(self, level, diff):
        # more progress means more objects
        self.coin_timer += 1
        self.traffic_timer += 1
        self.hazard_timer += 1
        self.event_timer += 1
        self.power_timer += 1

        if self.coin_timer > max(18, 45 - level):
            self.spawn_coin()
            self.coin_timer = 0
        if self.traffic_timer > max(42, 116 - level * 4 - diff):
            self.spawn_traffic()
            self.traffic_timer = 0
        if self.hazard_timer > max(95, 205 - level * 7 - diff):
            self.spawn_hazards()
            self.hazard_timer = 0
        if self.event_timer > max(190, 350 - level * 9 - diff):
            self.spawn_event()
            self.event_timer = 0
        if self.power_timer > 300:
            self.spawn_powerup()
            self.power_timer = 0

    def update_coins(self, player, speed):
        for item in self.coins_list[:]:
            item["y"] += speed
            rect = pygame.Rect(item["x"] - 12, item["y"] - 12, 24, 24)

            if player.colliderect(rect):
                self.beep()
                self.coins += 1
                self.coin_value += item["weight"]
                self.bonus += item["weight"] * 10
                self.say(f"+{item['weight']} coin", 35)
                self.coins_list.remove(item)
            elif item["y"] > HEIGHT + 40:
                self.coins_list.remove(item)

    def update_traffic(self, player, speed):
        for item in self.traffic[:]:
            item["y"] += speed + 1
            rect = pygame.Rect(item["x"] - 21, item["y"] - 36, 42, 72)

            if player.colliderect(rect):
                self.hit_player()
                self.traffic.remove(item)
            elif item["y"] > HEIGHT + 80:
                self.traffic.remove(item)

    def update_hazards(self, player, speed):
        for item in self.hazards[:]:
            item["y"] += speed
            rect = pygame.Rect(item["x"] - 20, item["y"] - 15, 40, 30)

            if player.colliderect(rect):
                if item["kind"] == "oil":
                    self.slow_time = 55
                    self.bonus += 5
                    self.say("Oil spill", 40)
                else:
                    self.hit_player()
                self.hazards.remove(item)
            elif item["y"] > HEIGHT + 40:
                self.hazards.remove(item)

    def update_events(self, player, speed):
        for item in self.events[:]:
            item["y"] += speed

            if item["kind"] == "moving_barrier":
                item["x"] += item["dx"]
                if item["x"] < ROAD_LEFT + 25 or item["x"] > ROAD_RIGHT - 25:
                    item["dx"] *= -1
                rect = pygame.Rect(item["x"] - 60, item["y"] - 8, 120, 16)
            else:
                rect = pygame.Rect(item["x"] - 28, item["y"] - 8, 56, 16)

            if player.colliderect(rect):
                if item["kind"] == "boost_strip":
                    self.strip_time = 95
                    self.bonus += 20
                    self.say("Boost strip!", 50)
                elif item["kind"] == "speed_bump":
                    self.slow_time = 35
                    self.say("Speed bump", 40)
                else:
                    self.hit_player()
                self.events.remove(item)
            elif item["y"] > HEIGHT + 30:
                self.events.remove(item)

    def update_powerups(self, player, speed):
        for item in self.powerups[:]:
            item["y"] += speed
            item["time"] -= 1
            rect = pygame.Rect(item["x"] - 14, item["y"] - 14, 28, 28)

            if player.colliderect(rect):
                self.beep()
                self.bonus += 40

                if item["kind"] == "nitro":
                    self.active_power = "nitro"
                    self.power_time = 240
                    self.say("Nitro!", 60)
                elif item["kind"] == "shield":
                    self.active_power = "shield"
                    self.power_time = 0
                    self.say("Shield ready", 60)
                else:
                    if self.extra_hit == 0:
                        self.extra_hit = 1
                    elif self.hazards:
                        self.hazards.pop(0)
                    elif self.traffic:
                        self.traffic.pop(0)
                    self.say("Repair collected", 60)

                self.powerups.remove(item)
            elif item["y"] > HEIGHT + 30 or item["time"] <= 0:
                self.powerups.remove(item)

    def update(self):
        if self.done:
            return

        speed = self.speed_now()
        level = 1 + self.progress // 700
        diff = DIFF_BONUS[self.settings["difficulty"]]

        self.road_y = (self.road_y + speed) % HEIGHT
        self.progress += speed
        self.distance += speed * DISTANCE_STEP
        self.player_x += (self.target_x - self.player_x) * 0.38
        self.update_power()
        self.update_spawns(level, diff)

        player = self.player_rect()
        self.update_coins(player, speed)
        self.update_traffic(player, speed)
        self.update_hazards(player, speed)
        self.update_events(player, speed)
        self.update_powerups(player, speed)

        self.score = int(self.coin_value * 20 + self.distance + self.bonus)
        if self.distance >= self.finish_distance:
            self.done = True
            self.win = True
            self.say("Finish!", 90)

    def result(self):
        return {
            "name": self.username,
            "score": self.score,
            "distance": int(self.distance),
            "coins": self.coins,
            "win": self.win,
        }

    def power_text(self):
        if self.active_power == "nitro":
            return f"Power: nitro {self.power_time // FPS + 1}s"
        if self.active_power == "shield":
            return "Power: shield"
        if self.extra_hit > 0:
            return "Power: repair"
        return "Power: none"

    def draw_road(self, screen):
        # draw moving road
        if ROAD_IMAGE:
            y = int(self.road_y)
            screen.blit(ROAD_IMAGE, (0, y - HEIGHT))
            screen.blit(ROAD_IMAGE, (0, y))
        else:
            screen.fill(GREEN)
            pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

        pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
        pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)

        for x in [157, 243]:
            for y in range(-60, HEIGHT, 60):
                pygame.draw.rect(screen, WHITE, (x, y + int(self.road_y % 60), 6, 32), border_radius=3)

    def draw_hud(self, screen, font, small_font):
        pygame.draw.rect(screen, WHITE, (8, 8, 230, 118), border_radius=10)
        pygame.draw.rect(screen, BLACK, (8, 8, 230, 118), 2, border_radius=10)

        left_text = max(0, int(self.finish_distance - self.distance))
        screen.blit(font.render(f"Score: {self.score}", True, BLACK), (18, 16))
        screen.blit(font.render(f"Coins: {self.coins}  Value: {self.coin_value}", True, BLACK), (18, 40))
        screen.blit(font.render(f"Distance: {int(self.distance)}", True, BLACK), (18, 64))
        screen.blit(font.render(f"Left: {left_text}", True, BLACK), (18, 88))
        screen.blit(small_font.render(self.power_text(), True, BLUE), (250, 16))

        # draw finish line
        pygame.draw.rect(screen, LIGHT_GRAY, (250, 44, 130, 12), border_radius=6)
        fill = int(130 * min(1, self.distance / self.finish_distance))
        pygame.draw.rect(screen, GREEN, (250, 44, fill, 12), border_radius=6)
        pygame.draw.rect(screen, BLACK, (250, 44, 130, 12), 1, border_radius=6)
        screen.blit(small_font.render(self.settings["difficulty"], True, BLACK), (250, 64))

        if self.message_time > 0:
            image = font.render(self.message, True, WHITE)
            box = image.get_rect(center=(WIDTH // 2, 145))
            box.inflate_ip(20, 12)
            pygame.draw.rect(screen, BLACK, box, border_radius=10)
            screen.blit(image, image.get_rect(center=box.center))

    def draw_hazards(self, screen):
        for item in self.hazards:
            x = item["x"]
            y = int(item["y"])

            if item["kind"] == "barrier":
                pygame.draw.rect(screen, ORANGE, (x - 20, y - 12, 40, 24), border_radius=6)
                pygame.draw.rect(screen, BLACK, (x - 20, y - 12, 40, 24), 2, border_radius=6)
            elif item["kind"] == "oil":
                pygame.draw.ellipse(screen, BLACK, (x - 20, y - 10, 40, 20))
                pygame.draw.ellipse(screen, LIGHT_GRAY, (x - 8, y - 4, 14, 6))
            else:
                pygame.draw.circle(screen, (70, 40, 20), (x, y), 14)
                pygame.draw.circle(screen, BLACK, (x, y), 14, 2)

    def draw_events(self, screen):
        for item in self.events:
            x = int(item["x"])
            y = int(item["y"])

            if item["kind"] == "moving_barrier":
                pygame.draw.rect(screen, PURPLE, (x - 60, y - 8, 120, 16), border_radius=5)
            elif item["kind"] == "speed_bump":
                pygame.draw.rect(screen, ORANGE, (x - 28, y - 6, 56, 12), border_radius=4)
            else:
                pygame.draw.rect(screen, CYAN, (x - 28, y - 6, 56, 12), border_radius=4)

    def draw_powerups(self, screen, small_font):
        letters = {"nitro": "N", "shield": "S", "repair": "R"}
        colors = {"nitro": CYAN, "shield": PURPLE, "repair": GREEN}

        for item in self.powerups:
            x = item["x"]
            y = int(item["y"])
            pygame.draw.rect(screen, colors[item["kind"]], (x - 14, y - 14, 28, 28), border_radius=8)
            pygame.draw.rect(screen, BLACK, (x - 14, y - 14, 28, 28), 2, border_radius=8)
            text = small_font.render(letters[item["kind"]], True, BLACK)
            screen.blit(text, text.get_rect(center=(x, y)))

    def draw(self, screen, font, small_font):
        self.draw_road(screen)

        for item in self.coins_list:
            draw_coin_sprite(screen, item["x"], int(item["y"]), item["weight"], small_font)

        for item in self.traffic:
            draw_car_sprite(screen, item["x"], int(item["y"]), item["color_name"], True)

        self.draw_hazards(screen)
        self.draw_events(screen)
        self.draw_powerups(screen, small_font)

        # blink after hit
        if self.hit_cooldown > 0 and self.hit_cooldown % 8 < 4:
            pygame.draw.circle(screen, CYAN, (int(self.player_x), self.player_y), 34, 3)

        draw_car_sprite(screen, int(self.player_x), self.player_y, self.settings["car_color"])
        self.draw_hud(screen, font, small_font)
