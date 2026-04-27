import os
import random
import sys

import pygame


pygame.init()

FPS = 60
clock = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
speed = 5
score = 0
coins_collected = 0
coin_weight_total = 0
coins_for_speedup = 5

big_font = pygame.font.SysFont("Verdana", 60)
medium_font = pygame.font.SysFont("Verdana", 30)
small_font = pygame.font.SysFont("Verdana", 20)
tiny_font = pygame.font.SysFont("Verdana", 15)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street Racer - Weighted Coins")


def load_image(filename, fallback, width, height):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, filename)

    try:
        image = pygame.image.load(path if os.path.exists(path) else filename)
        return pygame.transform.scale(image, (width, height))
    except:
        image = pygame.Surface((width, height))
        image.fill(fallback)
        return image


background_img = load_image("AnimatedStreet.png", GRAY, SCREEN_WIDTH, SCREEN_HEIGHT)
player_img = load_image("Player.png", BLUE, 50, 80)
enemy_img = load_image("Enemy.png", RED, 50, 80)


class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        self.speed = 7

    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Enemy:
    def __init__(self):
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.base_speed = speed
        self.reset()

    def reset(self):
        self.rect.x = random.randint(40, SCREEN_WIDTH - 40)
        self.rect.y = 0

    def current_speed(self):
        multiplier = 1 + (coins_collected // coins_for_speedup) * 0.2
        return self.base_speed * multiplier

    def move(self):
        global score
        self.rect.y += self.current_speed()
        if self.rect.y > SCREEN_HEIGHT:
            score += 1
            self.reset()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Coin:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 25, 25)
        self.active = False
        self.delay = 0
        self.weight = 1
        self.reset()

    def create_image(self):
        size = 25 + self.weight * 3
        color = BRONZE if self.weight == 1 else SILVER if self.weight == 2 else GOLD
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        pygame.draw.circle(self.image, WHITE, (size // 2, size // 2), size // 2, 2)
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

    def reset(self):
        self.rect.x = random.randint(30, SCREEN_WIDTH - 30)
        self.rect.y = random.randint(-500, -100)
        self.weight = random.choices([1, 2, 3], weights=[50, 30, 20])[0]
        self.create_image()
        self.active = True

    def move(self):
        if not self.active:
            self.delay -= 1
            if self.delay <= 0:
                self.active = True
                self.delay = random.randint(120, 300)
            return

        self.rect.y += speed // 2
        if self.rect.y > SCREEN_HEIGHT:
            self.reset()

    def draw(self, surface):
        if self.active:
            surface.blit(self.image, self.rect)
            image = tiny_font.render(str(self.weight), True, BLACK)
            surface.blit(image, image.get_rect(center=self.rect.center))


def show_game_over():
    screen.fill(RED)
    screen.blit(big_font.render("GAME OVER", True, BLACK), (SCREEN_WIDTH // 2 - 150, 150))
    screen.blit(medium_font.render(f"Score: {score}", True, WHITE), (SCREEN_WIDTH // 2 - 70, 250))
    screen.blit(medium_font.render(f"Coins: {coins_collected}", True, YELLOW), (SCREEN_WIDTH // 2 - 70, 290))
    screen.blit(small_font.render(f"Total Weight: {coin_weight_total}", True, WHITE), (SCREEN_WIDTH // 2 - 75, 330))
    screen.blit(small_font.render("SPACE to restart", True, GREEN), (SCREEN_WIDTH // 2 - 80, 400))
    screen.blit(small_font.render("ESC to quit", True, GREEN), (SCREEN_WIDTH // 2 - 55, 440))


def reset_game():
    global score, coins_collected, speed, coin_weight_total
    score = 0
    coins_collected = 0
    coin_weight_total = 0
    speed = 5
    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
    enemy.reset()
    coin.reset()


def draw_ui():
    score_text = small_font.render(f"Score: {score}", True, BLACK)
    coins_text = small_font.render(f"Coins: {coins_collected}", True, BLACK)
    weight_text = small_font.render(f"Weight: {coin_weight_total}", True, BLACK)
    speed_text = small_font.render(f"Speed: {enemy.current_speed():.1f}x", True, RED)
    next_text = tiny_font.render(f"Next: {(coins_collected // coins_for_speedup + 1) * coins_for_speedup} coins", True, RED)

    pygame.draw.rect(screen, WHITE, (5, 5, 180, 115))
    pygame.draw.rect(screen, BLACK, (5, 5, 180, 115), 2)
    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (10, 35))
    screen.blit(weight_text, (10, 60))
    screen.blit(speed_text, (10, 80))
    screen.blit(next_text, (10, 100))


player = Player()
enemy = Enemy()
coin = Coin()

game_over = False
speed_timer = 0
background_y = 0

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                reset_game()
                game_over = False
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    if not game_over:
        # update game state
        player.move()
        enemy.move()
        coin.move()

        speed_timer += 1
        if speed_timer > 300:
            speed = min(speed + 0.2, 12)
            speed_timer = 0

        if coin.active and player.rect.colliderect(coin.rect):
            coins_collected += 1
            coin_weight_total += coin.weight
            score += coin.weight * 10
            coin.reset()

        if player.rect.colliderect(enemy.rect):
            game_over = True

        background_y = (background_y + 2) % SCREEN_HEIGHT
        screen.blit(background_img, (0, background_y - SCREEN_HEIGHT))
        screen.blit(background_img, (0, background_y))

        player.draw(screen)
        enemy.draw(screen)
        coin.draw(screen)
        draw_ui()
    else:
        show_game_over()

    pygame.display.update()
